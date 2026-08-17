"""
    API de problemas
"""

from logging import getLogger
from re import match
from typing import Literal, Optional, Annotated, get_args

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field, ConfigDict, field_validator

from services.db import get_db_session
from models.problemset import Problem

# Regex para identificar a contest e problema
PROBLEM_ID_REGEX = r"^(?P<contest>[0-9]+)(?P<problem>[A-Z][0-9]?)$"

router = APIRouter(prefix="/problemset", tags=["Problemset"])
LOGGER = getLogger(__name__)

type Order = Literal["contestId", "index", "solvedCount", "rating", "points", "name"]
ORDER_MAPPINGS = {
    "contestId": "contest_id",
    "index": "index",
    "solvedCount": "solved_count",
    "rating": "rating",
    "points": "points",
    "name": "name"
}

class FilterParams(BaseModel):
    """ Parâmetros de filtro para a listagem de problemas """

    model_config = ConfigDict(extra="forbid")

    q: Optional[str] = Field(
        None,
        description="Termo de pesquisa para o nome do problema",
    )
    contest_id: Optional[int] = Field(
        None,
        description="ID da contest"
    )
    index: Optional[str] = Field(
        None,
        description="ID do problema",
        pattern=r"^[A-Z][0-9]?$"
    )
    rating: Optional[int] = Field(
        None,
        description="Rating do problema",
    )
    min_points: Optional[float] = Field(
        None,
        description="Número mínimo de pontos do problema",
    )
    tags: Optional[str] = Field(
        None,
        description="Lista de tags do problema separados por vírgula.",
    )
    order_by: Optional[str] = Field(
        "name",
        description="Campo para ordenação com vários fatores, separados por vírgula." \
        " Campos válidos: contestId, index, solvedCount, rating, points, name. " \
        "Prefixo - em cada para inverter a ordem",
    )
    limit: Optional[int] = Field(
        10,
        description="Número máximo de problemas a serem retornados",
        ge=1,
        le=100
    )
    page: Optional[int] = Field(
        1,
        description="Número da página de resultados",
        ge=1
    )

    @property
    def tags_list(self) -> Optional[list[str]]:
        """ Retorna a lista de tags do problema """
        if self.tags is None:
            return None

        # Remove espaços e divide por vírgula
        # pylint disable=no-member
        normalized = [tag.strip() for tag in self.tags.split(",") if tag.strip()]
        if len(normalized) == 0:
            return []

        return normalized

    @property
    def order_by_list(self) -> list[str]:
        """ Retorna a lista de campos para ordenação """

        if self.order_by is None:
            return ["name"]

        # Remove espaços e divide por vírgula
        # pylint disable=no-member
        normalized = [order.strip() for order in self.order_by.split(",") if order.strip()]
        if len(normalized) == 0:
            return ["name"]

        # Valida se todos os campos são válidos
        # pylint disable=no-member
        valid_fields = get_args(Order.__value__)
        for order in normalized:
            field_name = order[1:] if order.startswith("-") else order
            if field_name not in valid_fields:
                raise ValueError(f"Campo inválido para ordenação: {field_name}")

        return normalized

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v: str | None):
        """ Valida o campo tags """

        if v is None:
            return v

        # Remove espaços e divide por vírgula
        normalized = [tag.strip() for tag in v.split(",") if tag.strip()]
        if len(normalized) == 0:
            return None

        return v

    @field_validator("order_by", mode="before")
    @classmethod
    def validate_order_by(cls, v: str | None):
        """ Valida o campo order_by """

        if v is None:
            return ["name"]

        # Remove espaços e divide por vírgula
        normalized = [order.strip() for order in v.split(",") if order.strip()]
        if len(normalized) == 0:
            return ["name"]

        # Valida se todos os campos são válidos
        # pylint disable=no-member
        valid_fields = get_args(Order.__value__)
        for order in normalized:
            field_name = order[1:] if order.startswith("-") else order
            if field_name not in valid_fields:
                raise ValueError(f"Campo inválido para ordenação: {field_name}")

        return v

class ProblemResponse(BaseModel):
    """ Resposta para a listagem de problemas """

    model_config = ConfigDict(extra="allow")

    total: int
    page: int
    limit: int
    problems: list[dict]

EMPTY_RESPONSE = ProblemResponse(total=0, page=1, limit=10, problems=[])
def single(problem: Problem) -> ProblemResponse:
    """ Retorna uma resposta com apenas um problema """
    return ProblemResponse(total=1, page=1, limit=1, problems=[to_dict(problem)])

def is_valid_page(page: int, limit: int, total: int) -> bool:
    """ Verifica se a página solicitada é válida """
    return (page - 1) * limit < total

@router.get("/problems")
def get_problems(params: Annotated[FilterParams, Query()]):
    """
        Retorna uma lista de problemas com base nos filtros fornecidos.
    """

    LOGGER.debug(
        "Recebida requisição em /problemset/problems com parâmetros: %s",
        params.model_dump()
    )

    with get_db_session() as session:
        query = session.query(Problem)

        if params.contest_id and params.index:
            # Estamos fazendo o mesmo que /problems/{problem_id},
            # então podemos retornar apenas um problema
            problem = query.filter_by(contest_id=params.contest_id, index=params.index).first()
            if not problem:
                return EMPTY_RESPONSE

            return single(problem)

        if params.q:
            query = query.filter(Problem.name.ilike(f"%{params.q}%"))
        if params.contest_id:
            query = query.filter(Problem.contest_id == params.contest_id)
        if params.index:
            query = query.filter(Problem.index == params.index)
        if params.rating:
            query = query.filter(Problem.rating == params.rating)
        if params.min_points:
            query = query.filter(Problem.points >= params.min_points)
        if params.tags:
            for tag in params.tags_list:
                query = query.filter(Problem.tags.any(name=tag))

        total_count = query.count()

        if not is_valid_page(params.page, params.limit, total_count):
            return ProblemResponse(
                error="Página inválida",
                total=total_count,
                page=params.page,
                limit=params.limit,
                problems=[]
            )

        for order in params.order_by_list:
            mapped_order = ORDER_MAPPINGS.get(order.lstrip("-"))
            if order.startswith("-"):
                query = query.order_by(getattr(Problem, mapped_order).desc())
            else:
                query = query.order_by(getattr(Problem, mapped_order))

        problems = (
            query.offset((params.page - 1) * params.limit)
            .limit(params.limit)
            .all()
        )

        return ProblemResponse(
            total=total_count,
            page=params.page,
            limit=params.limit,
            problems=[to_dict(problem) for problem in problems]
        )

@router.get("/problems/{problem_id}")
def get_problem(problem_id: Annotated[str, Field(pattern=PROBLEM_ID_REGEX)]):
    """
        Retorna informações sobre um problema específico.
    """

    LOGGER.debug(
        "Recebida requisição em /problemset/problems/%s com parâmetros: {'problem_id': '%s'}",
        problem_id, problem_id
    )

    contest_id, problem_index = match(PROBLEM_ID_REGEX, problem_id).groups()
    result = {}
    with get_db_session() as session:
        problem = session.query(Problem).filter_by(
            contest_id=contest_id, index=problem_index
        ).first()

        if not problem:
            return {
                "error": "Problema não encontrado."
            }

        result = to_dict(problem)

    return result

def to_dict(problem: Problem) -> dict:
    """ Converte um objeto Problem em um dicionário """

    result = {}

    result['contestId'] = problem.contest_id
    if problem.problemset_name:
        result['problemsetName'] = problem.problemset_name
    result['index'] = problem.index
    result['name'] = problem.name
    result['type'] = problem.type.value
    if problem.points is not None:
        result['points'] = problem.points
    if problem.rating is not None:
        result['rating'] = problem.rating
    result['solvedCount'] = problem.solved_count
    result['tags'] = [tag.name for tag in problem.tags]

    return result
