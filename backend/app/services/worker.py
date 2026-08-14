from asyncio import sleep

from requests import get
from sqlalchemy.orm import Session

from services.db import get_db_session
import models.problemset as psm
import models.contest as cm

CODEFORCES_PROBLEMSET_URL = "https://codeforces.com/api/problemset.problems"
CODEFORCES_CONTESTS_URL = "https://codeforces.com/api/contest.list"
DEFAULT_INTERVAL = 2 * 60 # 2 minutos

async def start_worker(**kwargs):
    """ Inicia o worker """
    
    while True:
        try:
            await worker_loop(**kwargs)
        except Exception as e:
            print(f"Erro no worker: {e}")
        await sleep(DEFAULT_INTERVAL)

async def worker_loop(**kwargs):
    """ Loop do worker """

    with get_db_session() as session:
        with session.begin():
            sync_codeforces_problemset(session)

        with session.begin():
            sync_codeforces_contests(session)

def sync_codeforces_problemset(session: Session):
    """ Sincroniza o problemset do Codeforces no banco de dados """
    # 0. Criar tabelas caso não existam
    psm.ProblemsetBase.metadata.create_all(session.get_bind())

    # 1. Buscar problemset do Codeforces
    response = get(CODEFORCES_PROBLEMSET_URL)
    response.raise_for_status()
    problemset_data = response.json()

    # 2. Montar lista de problemas e dicionários
    statistics = {
        (stat['contestId'], stat['index']): stat['solvedCount']
        for stat in problemset_data['result']['problemStatistics']
    }

    # 3. Cachear as tags existentes no banco de dados para evitar duplicatas
    existing_tags = {tag.name: tag for tag in session.query(psm.Tag).all()}

    for problem in problemset_data['result']['problems']:
        key = (problem['contestId'], problem['index'])
        tags = []

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


def sync_codeforces_contests(session: Session):
    """ Busca a lista de concursos do Codeforces """
    # 0. Criar tabelas caso não existam
    cm.ContestsBase.metadata.create_all(session.get_bind())

    # 1. Buscar concursos do Codeforces
    response = get(CODEFORCES_CONTESTS_URL)
    response.raise_for_status()
    contests_data = response.json()

    # 2. Montar lista de concursos
    for contest in contests_data['result']:

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

