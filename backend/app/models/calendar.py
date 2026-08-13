"""
    Módulo com model Calendar, que representa um calendário do Google Calendar.
    A materialização para esse model foi feita com base:
    - No JSON completo retornado pela API do Google Calendar
    - Na tabela que descreve os campos retornados pela API do Google Calendar
    - Na realidade que se recebeu em testes

    O que mais impactou nos models foi a realidade dos testes.
    Por exemplo, a API retornou o seguinte para um calendário do CodeForces:
    {
      'kind': 'calendar#calendar',
      'etag': '"ETAG"',
      'id': 'CALENDAR_ID',
      'summary': 'Programming Contests Calendar',
      'timeZone': 'TIMEZONE'
    }
"""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

from models.gapi import GoogleResourceGet, make_request_proxy

# region Calendário

class Calendar(BaseModel):
    """
        Representa um calendário do Google Calendar.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    kind: Literal["calendar#calendar"] = "calendar#calendar"
    etag: str
    id: str
    summary: str
    time_zone: str = Field(alias="timeZone")

# endregion

class GoogleCalendarsResource(GoogleResourceGet[Calendar]):
    """
        Abstrai o recurso de calendários do Google Calendar API v3.
    """

class GoogleCalendarsResourceImpl(GoogleCalendarsResource):
    """
        Implementa o recurso calendar.calendars() da Google Calendar API v3.
    """
    def __init__(self, resource: GoogleCalendarsResource):
        super().__init__()
        self._resource = resource

    def get(self, **kwargs) -> GoogleResourceGet[Calendar]:
        return make_request_proxy(self._resource.get(**kwargs), Calendar)
