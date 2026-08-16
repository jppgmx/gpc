"""
    API de calendário.
"""

from datetime import datetime
from logging import getLogger
from typing import Annotated, Optional
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, ConfigDict

from services.data_store import DataStore
from services.secrets import get_google_credentials
from services.calendar_provider import CalendarProvider

router = APIRouter(prefix="/calendar")
calendar_provider = CalendarProvider(get_google_credentials(
    DataStore().allocate_file("secrets/gcalendar.json").path
))
LOGGER = getLogger(__name__)

# Esses calendários foram extraídos do iframe da página Calendar do Codeforces.
CALENDARS = {
    # Programming Contests Calendar
    "primary": "k23j233gtcvau7a8ulk2p360m4@group.calendar.google.com",

    # Misc Contests Calendar
    "misc": "efcajlnqvdqjeoud2spsiphnqk@group.calendar.google.com",

    # PCC + MCC
    "all": [
        "k23j233gtcvau7a8ulk2p360m4@group.calendar.google.com",
        "efcajlnqvdqjeoud2spsiphnqk@group.calendar.google.com"
    ]
}

@router.get("/{calendar_id}")
def get_calendar(calendar_id: str):
    """
        Retorna informações sobre um calendário específico.
    """

    LOGGER.debug(f"Recebida requisição em /calendar/{calendar_id} com parâmetros: {{'calendar_id': '{calendar_id}'}}")

    if not calendar_id in CALENDARS:
        return {"error": "Calendário não encontrado."}

    if isinstance(CALENDARS[calendar_id], list):
        cals = [calendar_provider.get_calendar(cal_id) for cal_id in CALENDARS[calendar_id]]
    else:
        cals = [calendar_provider.get_calendar(CALENDARS[calendar_id])]

    cals = [{
        'id': cal.id,
        'name': cal.summary,
        'timezone': cal.time_zone
    } for cal in cals]

    return cals[0] if len(cals) == 1 else cals

class FilterParams(BaseModel):
    """
        Parâmetros de filtro para a listagem de eventos do calendário.
    """
    model_config = ConfigDict(extra="forbid")

    q: Optional[str] = Field(None, description="Termo de pesquisa para filtrar eventos.")
    start: Optional[str] = Field(None, description="Data de início para filtrar eventos (RFC 3339).")
    end: Optional[str] = Field(None, description="Data de término para filtrar eventos (RFC 3339).")
    timezone: Optional[str] = Field(None, description="Fuso horário para os eventos.")
    order_by: Optional[str] = Field(None, description="Campo pelo qual ordenar os eventos.")
    page: Optional[int] = Field(default=1, description="Número da página de resultados a ser retornada.")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Número máximo de eventos a serem retornados.")

def to_rfc3339(dt: str, timezone: ZoneInfo) -> str:
    """
        Converte um objeto datetime para o formato RFC 3339.
    """
    normalized_dt = dt.replace("Z", "+00:00")  # Normaliza o formato de fuso horário
    dt_obj = datetime.fromisoformat(normalized_dt)

    if dt_obj.tzinfo is None:
        dt_obj = dt_obj.replace(tzinfo=timezone)

    return dt_obj.isoformat()

@router.get("/{calendar_id}/events")
def get_calendar_events(calendar_id: str, params: Annotated[FilterParams, Query()]):
    """
        Retorna uma lista de eventos de um calendário específico, com suporte a filtros e paginação.
    """
    LOGGER.debug(f"Recebida requisição em /calendar/{calendar_id}/events com parâmetros: {params.model_dump()}")

    if calendar_id == "all":
        return {"error": "Não é possível listar eventos de todos os calendários."}

    cal = calendar_provider.get_calendar(CALENDARS[calendar_id])
    default_tz = ZoneInfo(cal.time_zone) if cal.time_zone else ZoneInfo("UTC")
    req = {}

    if params.q:
        req['q'] = params.q
    if params.start:
        req['timeMin'] = to_rfc3339(params.start, default_tz)
    if params.end:
        req['timeMax'] = to_rfc3339(params.end, default_tz)
    if params.timezone:
        req['timeZone'] = params.timezone
    if params.order_by:
        req['orderBy'] = params.order_by
        if req['orderBy'] == "startTime":
            req['singleEvents'] = True
    if params.limit:
        req['maxResults'] = params.limit

    events = calendar_provider.list_events(cal, **req)
    if params.page and params.page > 1:
        for _ in range(1, params.page):
            events = calendar_provider.list_events(cal, pageToken=events.next_page_token, **req)

    result = [
        {
            "id": e.id,
            "summary": e.summary,
            "link": e.html_link,
            "description": e.description,
            "updated": e.updated,
            "start": str(e.start),
            "end": str(e.end),
        }
        for e in events.items
    ]

    return {
        "total": len(events.items),
        "page": params.page,
        "limit": params.limit,
        "has_more": bool(events.next_page_token),
        "events": result
    }
