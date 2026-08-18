"""
    Módulo do model de problemas do Codeforces

    A modelagem final dos problemas foi determinada da seguinte forma:
    - Documentação oficial do Codeforces: https://codeforces.com/apiHelp
    - A realidade vinda dos testes

    Dado uma amostra de 11356 problemas, eis a frequência de cada campo:
    - contestId = 11356/11356 (100,00%)
    - problemsetName = 0/11356 (0,00%)
    - index = 11356/11356 (100,00%)
    - name = 11356/11356 (100,00%)
    - type = 11356/11356 (100,00%)
    - points = 7442/11356 (65,53%)
    - rating = 11080/11356 (97,57%)
    - tags = 11356/11356 (100,00%)

    Apesar de problemsetName estar na documentação, não se aparenta estar sendo usado.
    Mas mantenhamos compatibilidade com a documentação oficial, caso seja usado no futuro.

    Além disso, outro objeto era o ProblemStatistics, que trazia o campo solvedCount, separado
    do objeto Problem. O teste também comprovou que contestId, index e solvedCount estão 100% 
    presentes, mas como forma de simplificação, vamos manter o campo solvedCount dentro de Problem.

"""

from typing import Optional, List
import enum
from sqlalchemy import String, Integer, Float, Enum
from sqlalchemy import UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class ProblemsetBase(DeclarativeBase):
    """ Base do banco de problemas do Codeforces """

class ProblemType(enum.Enum):
    """ Tipos de problemas """

    PROGRAMMING = 'PROGRAMMING'
    QUESTION = 'QUESTION'

class Problem(ProblemsetBase):
    """ Representa um problema do Codeforces """

    __tablename__ = 'problem'
    __table_args__ = (
        UniqueConstraint(
            'contestId', 'index'
        ),
    )
    contest_id: Mapped[int] = mapped_column("contestId", Integer, primary_key=True)
    index: Mapped[str] = mapped_column(String(10), primary_key=True)
    problemset_name: Mapped[str | None] = mapped_column("problemsetName", String(255))
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[ProblemType] = mapped_column(Enum(ProblemType))
    points: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    solved_count: Mapped[int] = mapped_column("solvedCount", Integer, nullable=False)
    tags: Mapped[List["Tag"]] = relationship(
        secondary="problem_tag",
        back_populates="problems"
    )

class ProblemTag(ProblemsetBase):
    """ Associação entre problemas e tags """

    __tablename__ = 'problem_tag'

    problem_contest_id: Mapped[int] = mapped_column(
        "problemContestId", primary_key=True
    )
    problem_index: Mapped[str] = mapped_column(
        "problemIndex", primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        "tagId", ForeignKey("tag.id"), primary_key=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['problemContestId', 'problemIndex'],
            ['problem.contestId', 'problem.index']
        ),
    )

class Tag(ProblemsetBase):
    """ Representa uma tag de problema (dp, implementation, etc) """

    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    problems: Mapped[List[Problem]] = relationship(
        secondary="problem_tag",
        back_populates="tags"
    )
