"""
    Módulo do model de concursos (contests) do Codeforces

    A modelagem final dos problemas foi determinada da seguinte forma:
    - Documentação oficial do Codeforces: https://codeforces.com/apiHelp
    - A realidade vinda dos testes

    Dado uma amostra de 11356 problemas, eis a frequência de cada campo:

    - id = 2139/2139 (100,00%)
    - name = 2139/2139 (100,00%)
    - type = 2139/2139 (100,00%)
    - phase = 2139/2139 (100,00%)
    - frozen = 2139/2139 (100,00%)
    - durationSeconds = 2139/2139 (100,00%)
    - freezeDurationSeconds = 14/2139 (0,65%)
    - startTimeSeconds = 2139/2139 (100,00%)
    - relativeTimeSeconds = 2139/2139 (100,00%)
    - preparedBy = 0/2139 (0,00%)
    - websiteUrl = 0/2139 (0,00%)
    - description = 0/2139 (0,00%)
    - difficulty = 0/2139 (0,00%)
    - kind = 0/2139 (0,00%)
    - icpcRegion = 0/2139 (0,00%)
    - country = 0/2139 (0,00%)
    - city = 0/2139 (0,00%)
    - season = 0/2139 (0,00%)

    Aqui o resultado é curioso, pois a maioria documentada não é usada, além de freezeDurationSeconds
    ter apenas 14 ocorrências. Mas assim como os problemas, vamos manter compatibilidade com a
    documentação oficial.
"""

import enum
from typing import Optional
from sqlalchemy import Text, Integer, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class ContestsBase(DeclarativeBase):
    """ Base do banco de concursos (contests) do Codeforces """

class ContestType(enum.Enum):
    """ Tipos de concursos """

    CF = 'CF'
    IOI = 'IOI'
    ICPC = 'ICPC'

class ContestPhase(enum.Enum):
    """ Fases de concursos """

    BEFORE = 'BEFORE'
    CODING = 'CODING'
    PENDING_SYSTEM_TEST = 'PENDING_SYSTEM_TEST'
    SYSTEM_TEST = 'SYSTEM_TEST'
    FINISHED = 'FINISHED'

class Contest(ContestsBase):
    """ Representa um concurso (contest) do Codeforces """

    __tablename__ = 'contest'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[ContestType] = mapped_column(Enum(ContestType))
    phase: Mapped[ContestPhase] = mapped_column(Enum(ContestPhase))
    frozen: Mapped[bool] = mapped_column(Boolean)
    duration_seconds: Mapped[int] = mapped_column("durationSeconds", Integer)
    freeze_duration_seconds: Mapped[Optional[int]] = mapped_column("freezeDurationSeconds", Integer, nullable=True)
    start_time_seconds: Mapped[Optional[int]] = mapped_column("startTimeSeconds", Integer, nullable=True)
    relative_time_seconds: Mapped[Optional[int]] = mapped_column("relativeTimeSeconds", Integer, nullable=True)
    prepared_by: Mapped[Optional[str]] = mapped_column("preparedBy", Text, nullable=True)
    website_url: Mapped[Optional[str]] = mapped_column("websiteUrl", Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    difficulty: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    kind: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    icpc_region: Mapped[Optional[str]] = mapped_column("icpcRegion", Text(), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
    season: Mapped[Optional[str]] = mapped_column(Text(), nullable=True)
