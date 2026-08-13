"""
    Módulo com abstrações do serviço calendar do Google e serviço CalendarProvider.
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from models.gapi import GoogleService
from models import calendar, event

class _GoogleCalendarV3Service(GoogleService):
    """
        Abstrai o serviço do Google Calendar API v3.
    """

    def calendars(self) -> calendar.GoogleCalendarsResource:
        """ Retorna o recurso de calendários do Google Calendar API v3. """

    def events(self) -> event.GoogleEventsResource:
        """ Retorna o recurso de eventos do Google Calendar API v3. """

# pylint: disable=no-member
class GoogleCalendarV3Service(_GoogleCalendarV3Service):
    """
        Implementa o serviço do Google Calendar API v3.
    """

    def __init__(self, credentials: Credentials):
        super().__init__()
        self._service: _GoogleCalendarV3Service = build('calendar', 'v3', credentials=credentials)

    def calendars(self) -> calendar.GoogleCalendarsResource:
        return calendar.GoogleCalendarsResourceImpl(self._service.calendars())

    def events(self) -> event.GoogleEventsResource:
        return event.GoogleEventsResourceImpl(self._service.events())
# pylint: enable=no-member

class CalendarProvider:
    """
        Serviço que provê informações sobre calendários e eventos usando Google Calendar.
    """
    def __init__(self, credentials: Credentials):
        self.service = GoogleCalendarV3Service(credentials)

    def get_calendar(self, calendar_id: str):
        """
            Retorna informações sobre um calendário específico.
        """
        return self.service.calendars().get(calendarId=calendar_id).execute()

    def list_events(self, calendar: calendar.Calendar, **kwargs) -> event.EventList:
        """
            Lista eventos de um calendário específico.

            Parameters:
                calendar (calendar.Calendar): O calendário do qual listar os eventos.
                **kwargs: Argumentos adicionais para a requisição, como timeMin, timeMax, etc.
            
            Nota:
                Consulte a documentação da Google Calendar API v3 para detalhes sobre os parâmetros
                aceitos pela API, como timeMin, timeMax, maxResults, etc.
        """
        return self.service.events().list(calendarId=calendar.id, **kwargs).execute()
