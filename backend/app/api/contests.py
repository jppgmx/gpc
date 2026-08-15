from typing import Annotated, Optional, Literal, get_args

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, ConfigDict, field_validator

from services.db import get_db_session
from services.secrets import get_google_credentials
from models.contest import Contest, ContestType, ContestPhase

router = APIRouter(prefix="/contests", tags=["Contests"])

class BasicOptions(BaseModel):
    """ Opções básicas para a listagem e obtenção de concursos """

    model_config = ConfigDict(extra="forbid")

    pretty_datetime: Optional[bool] = Field(
        False,
        description="Se True, retorna a data/hora em formato ISO 8601, " \
        "caso contrário, juntamente com a data/hora em segundos desde a época Unix," \
        "além do fuso horário aplicado. O padrão é False."
    )
    timezone: Optional[str] = Field(
        None,
        description="Fuso horário padrão para conversão de data/hora. " \
        "Se não fornecido, será usado o fuso horário do calendário do Google."
    )

class FilterParams(BasicOptions):
    """ Parâmetros de filtro para a listagem de concursos """

    q: Optional[str] = Field(
        None,
        description="Filtra concursos pelo nome. "
    )
    type: Optional[ContestType] = Field(
        None,
        description="Filtra concursos pelo tipo. " \
        "Se não fornecido, retorna todos os tipos de concursos."
    )
    phase: Optional[ContestPhase] = Field(
        None,
        description="Filtra concursos pela fase. " \
        "Se não fornecido, retorna todos os tipos de concursos."
    )
    limit: Optional[int] = Field(
        10,
        description="Número máximo de concursos a serem retornados.",
        ge=1,
        le=100
    )
    page: Optional[int] = Field(
        1,
        description="Número da página de resultados a ser retornada.",
        ge=1
    )

class ContestResponse(BaseModel):
    """ Resposta para a listagem de contests """

    model_config = ConfigDict(extra="allow")

    total: int
    page: int
    limit: int
    contests: list[dict]

EMPTY_RESPONSE = ContestResponse(total=0, page=1, limit=10, contests=[])
def single(contest: Contest) -> ContestResponse:
    """ Retorna uma resposta com apenas um problema """
    return ContestResponse(total=1, page=1, limit=1, contests=[to_dict(contest)])

def is_valid_page(page: int, limit: int, total: int) -> bool:
    """ Verifica se a página solicitada é válida """
    return (page - 1) * limit < total

@router.get("/")
def get_contests(params: Annotated[FilterParams, Query()]):
    """
        Retorna uma lista de concursos com base nos filtros fornecidos.
    """
    with get_db_session() as session:
        query = session.query(Contest)

        if params.q:
            query = query.filter(Contest.name.ilike(f"%{params.q}%"))

        if params.type:
            query = query.filter(Contest.type == params.type)

        if params.phase:
            query = query.filter(Contest.phase == params.phase)

        total = query.count()
        if not is_valid_page(params.page, params.limit, total):
            return ContestResponse(
                error="Página inválida",
                total=total,
                page=params.page,
                limit=params.limit,
                contests=[]
            )

        # Paginação
        offset = (params.page - 1) * params.limit
        contests = query.offset(offset).limit(params.limit).all()

        return ContestResponse(
            total=total,
            page=params.page,
            limit=params.limit,
            contests=[
                to_dict(contest, 
                        pretty_datetime=params.pretty_datetime, 
                        timezone=params.timezone) 
                for contest in contests
            ]
        )

@router.get("/{contest_id}")
def get_contest(contest_id: int, options: Annotated[BasicOptions, Query()]):
    with get_db_session() as session:
        contest = session.query(Contest).filter(Contest.id == contest_id).first()
        if not contest:
            return {"error": "Contest não encontrada"}

        return to_dict(
            contest,
            pretty_datetime=options.pretty_datetime,
            timezone=options.timezone
        )

def to_dict(contest: Contest, **kwargs) -> dict:
    """ Converte um objeto Contest em um dicionário """
    result = {}

    result['id'] = contest.id
    result['name'] = contest.name
    result["type"] = contest.type.value
    result["phase"] = contest.phase.value
    result["frozen"] = contest.frozen
    result["durationSeconds"] = contest.duration_seconds

    if kwargs.get("pretty_datetime"):
        from datetime import timedelta

        duration = timedelta(seconds=contest.duration_seconds)
        result["duration"] = str(duration)

    if contest.freeze_duration_seconds:
        result["freezeDurationSeconds"] = contest.freeze_duration_seconds

    if kwargs.get("pretty_datetime"):
        from datetime import timedelta

        freeze_duration = timedelta(seconds=contest.freeze_duration_seconds)
        result["freezeDuration"] = str(freeze_duration)
    
    result["startTimeSeconds"] = contest.start_time_seconds
    result["relativeTimeSeconds"] = contest.relative_time_seconds

    if kwargs.get("pretty_datetime"):
        from datetime import datetime, timedelta, UTC
        from zoneinfo import ZoneInfo

        from api.calendar import CALENDARS
        from services.calendar_provider import CalendarProvider
        from services.data_store import DataStore

        # A Data/Hora além de estarem na época Unix, também estão sob fuso horário
        # da plataforma, para garantir a acurácia da normalização, vamos consultar
        # o calendário o seu fuso horário, e então normalizar.
        provider = CalendarProvider(get_google_credentials(
            DataStore().allocate_file("secrets/gcalendar.json").path
        ))
        contests_calendar = provider.get_calendar(CALENDARS["primary"])
        default_timezone = kwargs.get("timezone")

        if not default_timezone:
            default_timezone = contests_calendar.time_zone

        if not isinstance(default_timezone, ZoneInfo):
            default_timezone = ZoneInfo(default_timezone)

        # Converter considerando a época Unix e o fuso horário da plataforma
        start_time = datetime.fromtimestamp(contest.start_time_seconds, tz=UTC)
        start_time = start_time.astimezone(default_timezone)
        result["startTime"] = start_time.isoformat()

        # Aplicar o tempo relativo
        relative_time = start_time + timedelta(seconds=contest.relative_time_seconds)
        result["relativeTime"] = relative_time.isoformat()

        result["timeZone"] = default_timezone.key

    if contest.prepared_by:
        result["preparedBy"] = contest.prepared_by

    if contest.website_url:
        result["websiteUrl"] = contest.website_url

    if contest.description:
        result["description"] = contest.description

    if contest.difficulty:
        result["difficulty"] = contest.difficulty

    if contest.kind:
        result["kind"] = contest.kind

    if contest.icpc_region:
        result["icpcRegion"] = contest.icpc_region

    if contest.country:
        result["country"] = contest.country

    if contest.city:
        result["city"] = contest.city

    if contest.season:
        result["season"] = contest.season

    return result