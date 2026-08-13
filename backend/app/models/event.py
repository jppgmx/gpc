"""
    Módulo com models para eventos do Google Calendar.
    A materialização para esses models, assim como Calendar, foi feita com base:
    - No JSON completo retornado pela API do Google Calendar
    - Na tabela que descreve os campos retornados pela API do Google Calendar
    - Na realidade que se recebeu em testes

    O que mais impactou nos models foi a realidade dos testes.
    Por exemplo, a API retornou o seguinte para um calendário do CodeForces:
    {
      'kind': 'calendar#events',
      'etag': '"ETAG"',
      'summary': 'Misc Codeforces Calendar',
      'description': '',
      'updated': 'RFC3339 DATETIME',
      'timeZone': 'TIMEZONE',
      'accessRole': 'reader',
      'defaultReminders': [],
      'items': [
          {
              'kind': 'calendar#event',
              'etag': '"ETAG"',
              'id': 'ID',
              'status': 'confirmed',
              'htmlLink': 'LINK',
              'created': 'RFC3339 DATETIME',
              'updated': 'RFC3339 DATETIME',
              'summary': 'SUMMARY',
              'description': 'DESCRIPTION',
              'location': 'LOCATION',
              'creator': {
                  'email': 'EMAIL'
              },
              'organizer': {
                  'email': 'EMAIL',
                  'displayName': 'DISPLAY NAME',
                  'self': False
              },
              'start': {
                  'dateTime': 'RFC3339 DATETIME',
                  'timeZone': 'TIMEZONE'
              },
              'end': {
                  'dateTime': 'RFC3339 DATETIME',
                  'timeZone': 'TIMEZONE'
              },
              'iCalUID': 'UID',
              'sequence': 0,
              'reminders': {'useDefault': True},
              'eventType': 'default'
          },
          ...
      ]
    }
"""

from datetime import datetime, date as dt
from zoneinfo import ZoneInfo
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator

from models.gapi import GoogleResourceGet, GoogleResourceList, make_request_proxy

# region Eventos

class Person(BaseModel):
    """
        Representa uma pessoa envolvida em um evento do Google Calendar.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    email: str
    display_name: Optional[str] = Field(default=None, alias="displayName")
    self: Optional[bool] = False

class EventDateTime(BaseModel):
    """
        Representa a data e hora de início ou fim de um evento do Google Calendar.
        Na API do Google Calendar, se o evento é o dia todo, "date" é sempre usado,
        caso contrário, "dateTime" é usado. A API não retorna ambos ao mesmo tempo.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    date: Optional[dt] = None
    date_time: Optional[datetime] = Field(default=None, alias="dateTime")
    time_zone: Optional[str] = Field(default=None, alias="timeZone")

    @model_validator(mode="after")
    def ensure_at_least_one_field(self):
        """
            Valida se pelo menos um dos campos "date" ou "date_time" está presente.
        """
        if not self.date and not self.date_time:
            raise ValueError("'date' ou 'date_time' deve estar presente.")
        return self

    @property
    def type(self) -> Literal["fullday", "datetime"]:
        """
            Retorna o tipo de evento, considerando se é um evento de dia inteiro ou não.
        """
        return "fullday" if self.date else "datetime"

    @property
    def data_real(self) -> dt | datetime:
        """
            Retorna a data e hora do evento, considerando se é um evento de dia inteiro ou não.        
        """
        return self.date if self.type == "fullday" else self.date_time

    @property
    def tzone(self) -> ZoneInfo | None:
        """
            Retorna o fuso horário do evento relacionado, se disponível.
        """

        # pylint: disable=no-member
        if self.type == "datetime" and self.date_time.tzinfo:
            return self.date_time.tzinfo

        # Fallback
        return ZoneInfo(self.time_zone) if self.time_zone else None

    @property
    def data_real_tz(self) -> datetime | None:
        """
            Retorna a data e hora do evento, considerando se é um evento de dia inteiro ou não,
            e ajustando para o fuso horário do evento.
        """
        if self.type == "fullday":
            return datetime.combine(self.date, datetime.min.time(), tzinfo=self.tzone)

        # pylint: disable=no-member
        return self.date_time.astimezone(self.tzone)

    def __str__(self) -> str:
        """
            Retorna uma representação em string do objeto EventDateTime.
        """
        return self.data_real_tz.strftime("%Y-%m-%d %H:%M:%S %Z")

class Reminder(BaseModel):
    """
        Representa um lembrete de evento do Google Calendar.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    method: Literal["email", "popup"]
    minutes: int

class Reminders(BaseModel):
    """
        Representa um conjunto de lembretes de evento do Google Calendar.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    use_default: bool = Field(alias="useDefault")
    overrides: Optional[list[Reminder]] = Field(default=None, alias="overrides")

class Event(BaseModel):
    """
        Representa um evento do Google Calendar.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Campos que sempre retornam
    kind: Literal["calendar#event"] = "calendar#event"
    etag: str
    id: str
    status: Literal["confirmed", "tentative", "cancelled"]
    html_link: str = Field(alias="htmlLink")
    created: datetime
    updated: datetime
    summary: str

    # A resposta real tem location e description em todos os itens.
    # Mas como podem vir vazios no futuro, é mais seguro manter Optional.
    description: Optional[str] = None
    location: Optional[str] = None

    # Objetos essenciais que sempre vieram na resposta
    creator: Person
    organizer: Person
    start: EventDateTime
    end: EventDateTime

    # Metadados menores
    i_cal_uid: str = Field(alias="iCalUID")
    sequence: int
    reminders: Reminders
    event_type: Literal["default", "birthday", "focusTime",
                        "fromGmail", "outOfOffice", "workingLocation"] = Field(alias="eventType")


class EventList(BaseModel):
    """
        Representa uma lista de eventos do Google Calendar, retornada por events.list().
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    kind: Literal["calendar#events"] = "calendar#events"
    etag: str
    summary: str
    description: str # Mantemos como str obrigatória, pois vimos que retorna "" (string vazia)
    updated: datetime
    time_zone: str = Field(alias="timeZone")
    access_role: Literal["none", "freeBusyReader", "reader",
                         "writerWithoutPrivateAccess", "writer", "owner"] = Field(alias="accessRole")

    # defaultReminders sempre retornou, mas vazio na prática.
    default_reminders: list[Reminder] = Field(default=[], alias="defaultReminders")

    # Só aparecem se houver mais de 250 eventos ou sync
    next_page_token: Optional[str] = Field(default=None, alias="nextPageToken")
    next_sync_token: Optional[str] = Field(default=None, alias="nextSyncToken")

    items: list[Event] = []

# endregion

class GoogleEventsResource(GoogleResourceGet[Event], GoogleResourceList[EventList]):
    """
        Abstrai o recurso de eventos do Google Calendar API v3.
    """

class GoogleEventsResourceImpl(GoogleEventsResource):
    """
        Implementa o recurso calendar.events() da Google Calendar API v3.
    """
    def __init__(self, resource: GoogleEventsResource):
        super().__init__()
        self._resource = resource

    def get(self, **kwargs) -> GoogleResourceGet[Event]:
        return make_request_proxy(self._resource.get(**kwargs), Event)

    def list(self, **kwargs) -> GoogleResourceList[EventList]:
        return make_request_proxy(self._resource.list(**kwargs), EventList)
