"""
    Módulo do worker.
"""

from asyncio import sleep, to_thread
from logging import getLogger

from requests import get
from sqlalchemy.orm import Session

from services.db import get_db_session
from services.logging import start_chronometer as chrono
import models.problemset as psm
import models.contest as cm

CODEFORCES_PROBLEMSET_URL = "https://codeforces.com/api/problemset.problems"
CODEFORCES_CONTESTS_URL = "https://codeforces.com/api/contest.list"
DEFAULT_INTERVAL = 2 * 60 # 2 minutos

LOGGER = getLogger(__name__)

async def start_worker(**kwargs):
    """ Inicia o worker """

    LOGGER.info("Worker iniciado.")
    while True:
        try:
            start_time = chrono()
            await worker_loop(**kwargs)
            LOGGER.info(f"Worker gastou {start_time().total_seconds():.2f} segundos na execução. Vou dormir...")
        except Exception as e:
            LOGGER.exception("Erro durante a execução do worker.")
        await sleep(DEFAULT_INTERVAL)
        LOGGER.info(f"Retomando...")

async def worker_loop(**kwargs):
    """ Loop do worker """

    # Executa a sincronização de forma bloqueante em uma thread separada
    await to_thread(_run_sync_blocking)


def _run_sync_blocking():
    """ Executa a sincronização de forma bloqueante """
    LOGGER.info("Iniciando sincronização com o Codeforces...")
    chronometer = chrono()

    with get_db_session() as session:
        with session.begin():
            sync = chrono()
            sync_codeforces_problemset(session)
            LOGGER.info(f"Sincronização do problemset concluída em {sync().total_seconds():.2f} segundos.")

        with session.begin():
            sync = chrono()
            sync_codeforces_contests(session)
            LOGGER.info(f"Sincronização dos contests concluída em {sync().total_seconds():.2f} segundos.")

    LOGGER.info(f"Tempo total da sincronização: {chronometer().total_seconds():.2f} segundos.")

def sync_codeforces_problemset(session: Session):
    """ Sincroniza o problemset do Codeforces no banco de dados """
    # 0. Criar tabelas caso não existam
    LOGGER.debug("Criando tabelas do problemset, se não existirem...")
    psm.ProblemsetBase.metadata.create_all(session.get_bind())

    # 1. Buscar problemset do Codeforces
    LOGGER.info("Buscando problemset do Codeforces...")
    response = get(CODEFORCES_PROBLEMSET_URL)
    response.raise_for_status()
    problemset_data = response.json()

    total_problems = len(problemset_data['result']['problems'])
    LOGGER.info(f"Total de problemas encontrados: {total_problems}")
    # 2. Montar lista de problemas e dicionários
    statistics = {
        (stat['contestId'], stat['index']): stat['solvedCount']
        for stat in problemset_data['result']['problemStatistics']
    }

    # 3. Cachear as tags existentes no banco de dados para evitar duplicatas
    existing_tags = {tag.name: tag for tag in session.query(psm.Tag).all()}
    LOGGER.debug(f"Tags existentes no banco de dados: {list(existing_tags.keys())}")

    i = 1
    LOGGER.info("Sincronizando problemas...")
    for problem in problemset_data['result']['problems']:
        key = (problem['contestId'], problem['index'])
        tags = []

        LOGGER.debug(f"Processando problema {i}/{total_problems}: {problem['name']} ID: {key[0]}{key[1]}")

        for tag_name in problem.get('tags', []):
            if tag_name not in existing_tags:
                new_tag = psm.Tag(name=tag_name)
                session.add(new_tag)
                existing_tags[tag_name] = new_tag
            
            tags.append(existing_tags[tag_name])

        # 4. Checar se existe
        existing_problem = session.query(psm.Problem).filter_by(
            contest_id=problem['contestId'],
            index=problem['index']
        ).first()

        # 5. Atualizar ou adicionar
        if existing_problem:
            # Atualizar campos do problema existente
            existing_problem.problemset_name = problem.get('problemsetName', None)
            existing_problem.name = problem['name']
            existing_problem.type = psm.ProblemType[problem['type']]
            existing_problem.points = problem.get('points')
            existing_problem.rating = problem.get('rating')
            existing_problem.solved_count = statistics.get(key, 0)
            existing_problem.tags = tags
        else:
            # Adicionar novo problema
            prob = psm.Problem(
                contest_id=problem['contestId'],
                problemset_name=problem.get('problemsetName', None),
                index=problem['index'],
                name=problem['name'],
                type=psm.ProblemType[problem['type']],
                points=problem.get('points'),
                rating=problem.get('rating'),
                solved_count=statistics.get(key, 0),
                tags=tags
            )
            session.add(prob)
        i += 1

    LOGGER.info("Sincronização do problemset concluída.")


def sync_codeforces_contests(session: Session):
    """ Sincroniza os concursos do Codeforces no banco de dados """
    # 0. Criar tabelas caso não existam
    LOGGER.debug("Criando tabelas de concursos, se não existirem...")
    cm.ContestsBase.metadata.create_all(session.get_bind())

    # 1. Buscar concursos do Codeforces
    LOGGER.info("Buscando concursos do Codeforces...")
    response = get(CODEFORCES_CONTESTS_URL)
    response.raise_for_status()
    contests_data = response.json()

    total_contests = len(contests_data['result'])
    LOGGER.info(f"Total de concursos encontrados: {total_contests}")
    i = 1

    # 2. Montar lista de concursos
    LOGGER.info("Sincronizando concursos...")
    for contest in contests_data['result']:
        LOGGER.debug(f"Processando concurso {i}/{total_contests}: {contest['name']} ID: {contest['id']}")

        # 3. Checar se existe
        existing_contest = session.query(cm.Contest).filter_by(id=contest['id']).first()

        if existing_contest:
            existing_contest.name = contest['name']
            existing_contest.type = cm.ContestType[contest['type']]
            existing_contest.phase = cm.ContestPhase[contest['phase']]
            existing_contest.frozen = contest['frozen']
            existing_contest.duration_seconds = contest['durationSeconds']
            existing_contest.freeze_duration_seconds = contest.get('freezeDurationSeconds')
            existing_contest.start_time_seconds = contest.get('startTimeSeconds')
            existing_contest.relative_time_seconds = contest.get('relativeTimeSeconds')
            existing_contest.prepared_by = contest.get('preparedBy')
            existing_contest.website_url = contest.get('websiteUrl')
            existing_contest.description = contest.get('description')
            existing_contest.difficulty = contest.get('difficulty')
            existing_contest.kind = contest.get('kind')
            existing_contest.icpc_region = contest.get('icpcRegion')
            existing_contest.country = contest.get('country')
            existing_contest.city = contest.get('city')
            existing_contest.season = contest.get('season')
        else:
            con = cm.Contest(
                id=contest['id'],
                name=contest['name'],
                type=cm.ContestType[contest['type']],
                phase=cm.ContestPhase[contest['phase']],
                frozen=contest['frozen'],
                duration_seconds=contest['durationSeconds'],
                freeze_duration_seconds=contest.get('freezeDurationSeconds'),
                start_time_seconds=contest.get('startTimeSeconds'),
                relative_time_seconds=contest.get('relativeTimeSeconds'),
                prepared_by=contest.get('preparedBy'),
                website_url=contest.get('websiteUrl'),
                description=contest.get('description'),
                difficulty=contest.get('difficulty'),
                kind=contest.get('kind'),
                icpc_region=contest.get('icpcRegion'),
                country=contest.get('country'),
                city=contest.get('city'),
                season=contest.get('season')
            )
            session.add(con)

        i += 1
    LOGGER.info("Sincronização dos concursos concluída.")
