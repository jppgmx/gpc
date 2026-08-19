"""
    Módulo do worker.
"""

from asyncio import sleep, to_thread
from logging import getLogger

from requests import get
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session

from services.db import get_db_session, insert_update, get_max_batch_size
from services.logging import start_chronometer as chrono
import models.problemset as psm
import models.contest as cm

CODEFORCES_PROBLEMSET_URL = "https://codeforces.com/api/problemset.problems"
CODEFORCES_CONTESTS_URL = "https://codeforces.com/api/contest.list"
DEFAULT_INTERVAL = 6 * 60 * 60 # 6 horas
SYNC_GET_TIMEOUT = 30  # 30 segundos

LOGGER = getLogger(__name__)

async def start_worker(**kwargs):
    """ Inicia o worker """

    LOGGER.info("Worker iniciado.")
    while True:
        try:
            start_time = chrono()
            await worker_loop(**kwargs)
            LOGGER.info(
                "Worker gastou %.2f segundos na execução. Vou dormir...",
                start_time().total_seconds()
            )
        except Exception as _:
            LOGGER.exception("Erro durante a execução do worker.")
        await sleep(DEFAULT_INTERVAL)
        LOGGER.info("Retomando...")

async def worker_loop(**kwargs):
    """ Loop do worker """

    # Executa a sincronização de forma bloqueante em uma thread separada
    await to_thread(_run_sync_blocking, **kwargs)


def _run_sync_blocking(**kwargs):
    """ Executa a sincronização de forma bloqueante """
    LOGGER.info("Iniciando sincronização com o Codeforces...")
    chronometer = chrono()

    with get_db_session() as session:
        with session.begin():
            sync = chrono()
            sync_codeforces_problemset(session)
            LOGGER.info("Sincronização do problemset concluída em %.2f segundos.",
                        sync().total_seconds())

        with session.begin():
            sync = chrono()
            sync_codeforces_contests(session)
            LOGGER.info("Sincronização dos contests concluída em %.2f segundos.",
                        sync().total_seconds())

    LOGGER.info("Tempo total da sincronização: %.2f segundos.", chronometer().total_seconds())

def sync_codeforces_problemset(session: Session):
    """ Sincroniza o problemset do Codeforces no banco de dados """
    # 0. Criar tabelas caso não existam
    LOGGER.debug("Criando tabelas do problemset, se não existirem...")
    psm.ProblemsetBase.metadata.create_all(session.get_bind())

    # 1. Buscar problemset do Codeforces
    LOGGER.info("Buscando problemset do Codeforces...")
    response = get(CODEFORCES_PROBLEMSET_URL, timeout=SYNC_GET_TIMEOUT)
    response.raise_for_status()
    problemset_data = response.json()
    LOGGER.debug("CF status: %s", problemset_data['status'])

    total_problems = len(problemset_data['result']['problems'])
    LOGGER.info("Total de problemas encontrados: %d", total_problems)
    # 2. Montar lista de problemas e dicionários
    statistics = {
        (stat['contestId'], stat['index']): stat['solvedCount']
        for stat in problemset_data['result']['problemStatistics']
    }
    problemset_data = problemset_data['result']['problems']

    # 3. Cachear as tags existentes no banco de dados para evitar duplicatas
    existing_tags = {tag.name: tag for tag in session.query(psm.Tag).all()}
    LOGGER.debug("Tags existentes no banco de dados: %s", list(existing_tags.keys()))

    LOGGER.info("Sincronizando problemas...")
    for i in range(0, total_problems):
        problem = problemset_data[i]
        LOGGER.debug(
            "Processando problema %d/%d: %s (Contest ID: %s, Index: %s)",
            i+1, total_problems, problem['name'], problem.get('contestId'), problem['index']
        )

        for tag_name in problem.get('tags', []):
            if tag_name not in existing_tags:
                LOGGER.debug("Adicionando nova tag: %s", tag_name)
                new_tag = psm.Tag(name=tag_name)
                session.add(new_tag)
                existing_tags[tag_name] = new_tag

        solved_count = statistics.get((problem['contestId'], problem['index']), 0)
        tmp = problem
        problemset_data[i] = {
            "contestId": tmp.get('contestId'),
            "index": tmp.get('index'),
            "problemsetName": tmp.get('problemsetName'),
            "name": tmp.get('name'),
            "type": psm.ProblemType[tmp.get('type')],
            "points": tmp.get('points'),
            "rating": tmp.get('rating'),
            "solvedCount": solved_count,
            "tags": tmp.get('tags', [])
        }
        del tmp

    del statistics
    session.flush()

    relationships = []
    LOGGER.debug("Construindo relacionamentos de tags...")
    for i, problem in enumerate(problemset_data, start=1):
        LOGGER.debug(
            "Processando problema %d/%d para relacionamento de tags",
            i, len(problemset_data)
        )
        for tag_name in problem['tags']:
            tag = existing_tags[tag_name]
            relationships.append({
                "problemContestId": problem['contestId'],
                "problemIndex": problem['index'],
                "tagId": tag.id
            })
        del problem['tags']  # Remove a lista de tags do problema para não armazenar no banco

    batch_size = get_max_batch_size(session, psm.Problem)
    batch_count = (len(problemset_data) // batch_size) + \
        (1 if len(problemset_data) % batch_size else 0)

    LOGGER.debug("Inserindo/atualizando problemas em lotes de tamanho %d...", batch_size)
    for i in range(batch_count):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(problemset_data))
        LOGGER.debug(
            "Processando lote %d/%d: problemas %d a %d",
            i + 1, batch_count, start_index + 1, end_index
        )
        insert_update(
            session, psm.Problem, problemset_data[start_index:end_index],
            index_elements=["contestId", "index"]
        )

    batch_size = get_max_batch_size(session, psm.ProblemTag)
    batch_count = len(relationships) // batch_size + \
        (1 if len(relationships) % batch_size else 0)

    LOGGER.debug("Inserindo relacionamentos de tags em lotes de tamanho %d...", batch_size)

    # Limpando a tabela de relacionamentos antes de inserir os novos dados
    session.execute(delete(psm.ProblemTag))
    for i in range(batch_count):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(relationships))
        LOGGER.debug(
            "Processando lote %d/%d: relacionamentos de tags %d a %d",
            i + 1, batch_count, start_index + 1, end_index
        )
        session.execute(insert(psm.ProblemTag).values(relationships[start_index:end_index]))

    LOGGER.info(
        "Sincronização do problemset concluída: %d problemas e %d relacionamentos de tags.",
        len(problemset_data), len(relationships)
    )


def sync_codeforces_contests(session: Session):
    """ Sincroniza os concursos do Codeforces no banco de dados """
    # 0. Criar tabelas caso não existam
    LOGGER.debug("Criando tabelas de concursos, se não existirem...")
    cm.ContestsBase.metadata.create_all(session.get_bind())

    # 1. Buscar concursos do Codeforces
    LOGGER.info("Buscando concursos do Codeforces...")
    response = get(CODEFORCES_CONTESTS_URL, timeout=SYNC_GET_TIMEOUT)
    response.raise_for_status()
    contests_data = response.json()
    LOGGER.debug("CF status: %s", contests_data['status'])

    contests_data = contests_data['result']
    total_contests = len(contests_data)
    LOGGER.info("Total de concursos encontrados: %d", total_contests)

    # 2. Montar lista de concursos
    LOGGER.info("Sincronizando concursos...")
    for i, contest in enumerate(contests_data, start=1):
        LOGGER.debug(
            "Processando concurso %d/%d: %s ID: %d",
            i, total_contests, contest['name'], contest['id']
        )

        tmp = contest
        contests_data[i-1] = {
            "id": tmp.get('id'),
            "name": tmp.get('name'),
            "type": cm.ContestType[tmp.get('type')],
            "phase": cm.ContestPhase[tmp.get('phase')],
            "frozen": tmp.get('frozen'),
            "duration_seconds": tmp.get('durationSeconds'),
            "freeze_duration_seconds": tmp.get('freezeDurationSeconds'),
            "start_time_seconds": tmp.get('startTimeSeconds'),
            "relative_time_seconds": tmp.get('relativeTimeSeconds'),
            "prepared_by": tmp.get('preparedBy'),
            "website_url": tmp.get('websiteUrl'),
            "description": tmp.get('description'),
            "difficulty": tmp.get('difficulty'),
            "kind": tmp.get('kind'),
            "icpc_region": tmp.get('icpcRegion'),
            "country": tmp.get('country'),
            "city": tmp.get('city'),
            "season": tmp.get('season')
        }
        del tmp

    batch_size = get_max_batch_size(session, cm.Contest)
    batch_count = (len(contests_data) // batch_size) + \
        (1 if len(contests_data) % batch_size else 0)

    LOGGER.debug("Inserindo/atualizando concursos em lotes de tamanho %d...", batch_size)
    for i in range(batch_count):
        start_index = i * batch_size
        end_index = min((i + 1) * batch_size, len(contests_data))
        LOGGER.debug(
            "Processando lote %d/%d: concursos %d a %d",
            i + 1, batch_count, start_index + 1, end_index
        )
        insert_update(
            session, cm.Contest, contests_data[start_index:end_index],
            index_elements=["id"]
        )
    LOGGER.info("Sincronização dos concursos concluída.")
