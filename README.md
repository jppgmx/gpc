# GPC (Garoto de Programa Competitivo)

Assistente de IA não oficial para o ecossistema Codeforces — ajuda a explorar a
plataforma, tira dúvidas sobre suas regras e dá suporte a quem está mergulhando
em programação competitiva.

## O que o GPC já faz

- Responde perguntas sobre a plataforma Codeforces via chat, com memória de
  conversa
- Consulta o status do sistema do Codeforces em tempo real
- Responde dúvidas sobre Termos de Uso e Política de Privacidade, usando busca
  semântica (RAG) sobre o conteúdo oficial
- Consulta eventos da plataforma por meio da API do Google Calendar
- Permite consultar problemas e contests da plataforma de forma avançada
- Se apresenta com transparência: deixa claro que é um agente não-oficial e
  que pode errar

## Motivação

Sou do curso de Análise e Desenvolvimento de Sistemas do Instituto Federal do
Sertão Paraibano (IFSPB) — a divisão mais recente, desmembrada do IFPB.

O curso não costuma abordar isso diretamente, mas entrei na área de Programação
Competitiva desde o início. É uma área que ensina a interpretar e resolver
problemas por meio de soluções eficientes — e, na maioria das vezes,
descartáveis, já que não são pensadas para serem mantidas a longo prazo.

Se aprende praticando, e o Codeforces é uma plataforma de nível mundial, com
problemas, contests semanais e competições de peso como ICPC, SBC e OPI.

O GPC nasceu como forma de ajudar quem usa a plataforma — e como oportunidade
de aprender construindo, através do desafio da Oracle Next Education (ONE) em
parceria com a Alura.

## Status

Projeto desenvolvido para o Challenge Agente da Alura, em parceria com a
Oracle Next Education (ONE).

A próxima etapa é tentar fazer deploy, a ideia era usar OCI, mas devido uns
problemas, estarei usando a AWS.

## Não afiliação e transparência

O GPC **não é afiliado, endossado ou mantido pelo Codeforces** ou pela
CODEFORCES GLOBAL FZCO. É um projeto pessoal e independente.

Este projeto utiliza IA e pode cometer erros ou apresentar conteúdo
desatualizado. Para decisões importantes, sempre confira as fontes oficiais:

- Termos e Condições: https://codeforces.com/terms
- Política de Privacidade: https://codeforces.com/privacy
- Ajuda / FAQ: https://codeforces.com/help

Texto completo do aviso local: `backend/assets/docs/disclaimer.md`

## Arquitetura (visão geral)

O projeto possui dois serviços principais via Docker Compose:

- **`backend`** (FastAPI) em `:8000` — serve de suporte ao agente, buscando, normalizando
  e servindo documentos e demais dados.
- **`n8n`** em `:5678` — orquestra o agente de IA (GPC).
- **`caddy`** — disponível em ambiente de produção e é usado para fazer proxy reverso para o n8n.

### Agente (n8n)

O GPC é um agente de IA (modelo Cohere) com memória de conversa, acessível via
chat (via API do Telegram), com as seguintes ferramentas disponíveis:

- Consulta de status do sistema Codeforces (`system.status`)
- Busca semântica (RAG) sobre Termos, Privacidade e o aviso de transparência
  do próprio projeto
- Consulta de eventos nos calendários da plataforma como a Programming Contests Calendar e
  Misc Codeforces Calendar
- Consulta dos problemas da paltaforma com suporte a pesquisa, ordenação e paginação.
- Consulta detalhada das contests da plataforma, também com filtros avançados.

### Fluxo de dados (backend)

O agente possui diversas fontes de dados, porém, devido as limitações da plataforma em fornecer
formas de pesquisa avançadas, inclusive, obter problemas de lá sempre retorna mais de 11 mil objetos,
o backend pega esses dados, normaliza e cacheia.

#### Documentos

1. `terms` e `privacy` são buscados de `codeforces.com`, quando dispara API REST.
2. O conteúdo HTML é filtrado e convertido para Markdown.
3. O resultado é armazenado em cache dentro de `.data`.
4. `disclaimer` é servido a partir de um arquivo local, sem busca externa.

#### Problemas e contests

1. Ao iniciar o servidor, um worker faz a sincronização em um certo intervalo.
2. Consiste em pegar todos os problemas e contests.
3. Normalizar usando os models do SQLAlchemy.
4. Inserir e/ou atualizar no banco de dados.

## Estrutura do repositório

```text
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── calendar.py
│   │   │   ├── contests.py
│   │   │   ├── docs.py
│   │   │   └── problemset.py
│   │   ├── models
│   │   │   ├── mdconvs
│   │   │   │   └── privacy.py
│   │   │   ├── sources
│   │   │   │   ├── cache.py
│   │   │   │   └── url.py
│   │   │   ├── transformers
│   │   │   │   ├── callable.py
│   │   │   │   ├── html_transformer.py
│   │   │   │   └── markdown.py
│   │   │   ├── calendar.py
│   │   │   ├── contest.py
│   │   │   ├── document.py
│   │   │   ├── event.py
│   │   │   ├── gapi.py
│   │   │   └── problemset.py
│   │   ├── services
│   │   │   ├── calendar_provider.py
│   │   │   ├── data_store.py
│   │   │   ├── db.py
│   │   │   ├── document_provider.py
│   │   │   ├── logging.py
│   │   │   ├── profiling.py
│   │   │   ├── secrets.py
│   │   │   └── worker.py
│   │   └── main.py
│   ├── assets
│   │   ├── docs
│   │   │   ├── disclaimer.md
│   │   │   ├── privacy.md
│   │   │   └── terms.md
│   │   └── README.md
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── requirements-dev.txt
├── calibration
│   └── round-1.md
├── scripts
│   ├── copy_workflows.py
│   └── envgen.py
├── workflows
│   ├── gpc-agent.json
│   └── gpc-docs.json
├── Caddyfile
├── docker-compose.prod.yml
├── docker-compose.yml
├── Makefile
└── README.md
```

## Tecnologias usadas

As principais tecnologias e ferramentas usadas neste projeto incluem:

- Python 3.12
- FastAPI (backend web framework)
- Uvicorn (ASGI server)
- SQLite (banco de dados)
- SQLAlchemy (ORM)
- requests (cliente HTTP)
- Pydantic (validação de dados)
- BeautifulSoup4 (parser de HTML)
- markdownify (conversor de HTML para Markdown)
- Google APIs (integração com o Calendário)
- tzdata (informações de fuso horário)
- psutil (métricas de % de CPU e RAM)
- n8n (automação/workflows)
- Docker e Docker Compose
- Cloudflare Tunnel (para testes localhost)
- Deploy na Amazon Web Services (AWS)
- make
- pylint

## Pré-requisitos

- Docker
- Docker Compose
- Python 3.12 (para desenvolvimento local do backend)
- `make` (opcional, mas recomendado)
- Se estiver rodando localhost, você precisará criar um túnel usando Cloudflare para criar uma URL pública.
  É dessa forma que a API do Telegram possa funcionar localmente.
- Se estiver em ambiente de produção (por exemplo, AWS ou OCI), certifique-se que haja um endereço IP público,
  de preferência fixo, e um provedor DNS.

### Setup do Túnel Cloudflare

1. Crie ou entre na sua conta do Cloudflare;
2. Em seu dashboard, vá em **Protect & Connect > Networking > Tunnels**;
3. Clique em **Create Tunnel**;
4. Siga as instruções como inserir nome e instalar o cloudflared;
5. Abra o terminal e digite `cloudflared tunnel --url http://localhost:5678`;
6. O Cloudflare vai lher dar uma URL a cada execução do cloudflared.
  ```
  +--------------------------------------------------------------------------------------------+
  |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
  |  https://XYZ.trycloudflare.com                                                             |
  +--------------------------------------------------------------------------------------------+
  ```

### Setup para produção (sugestão)

Você pode criar uma conta no [Duck DNS](https://www.duckdns.org/), adicionar um nome e associar o IP da instância pública.
Fica algo como `nome.duckdns.org`, então na etapa da produção, precisará configurar o Caddyfile para apontar para esse
endereço DNS.

### Antes do Docker subir...

É necessário que seja gerado um arquivo .env para que o n8n assuma um domínio.
Você pode chamar os comandos make abaixo e responda os prompts para gerar, ou
pode criar manualmente com base no template abaixo:

```
# Host
N8N_HOST=localhost
N8N_PROTOCOL=http
N8N_PORT=5678

# URLs
PUBLIC_URL=http://localhost:5678
WEBHOOK_URL=http://localhost:5678/
N8N_EDITOR_BASE_URL=http://localhost:5678

# Timezone
GENERIC_TIMEZONE=America/Sao_Paulo
```

O template acima já permite rodar n8n em ambiente local, caso esteja em produção e use
a sugestão acima:

```
# Host
N8N_HOST=nome.duckdns.org
N8N_PROTOCOL=https
N8N_PORT=5678

# URLs
PUBLIC_URL=https://nome.duckdns.org
WEBHOOK_URL=https://nome.duckdns.org/
N8N_EDITOR_BASE_URL=https://nome.duckdns.org

# Timezone
GENERIC_TIMEZONE=America/Sao_Paulo
```

## Setup rápido (desenvolvimento)

Com `make`:

```bash
make setup
```

Esse alvo:

- cria o virtualenv em `backend/.venv`;
- instala dependências de `backend/requirements.txt`;
- instala dependências adicionais de `backend/requirements-dev.txt`
- instala o backend em modo editável (`pip install -e .`).

## Pylint

É possível rodar o Pylint para checar a sintaxe do código:

```bash
make pylint
```

## Executando com Docker

- .env é **requerido** para iniciar

Subir tudo:

```bash
make start
```

Subir apenas n8n:

```bash
make start-n8n
```

Subir apenas backend:

```bash
make start-backend
```

Parar tudo:

```bash
make stop
```

Tem também `stop-n8n` e `stop-backend`.

## ou caso queira testar apenas o servidor sem Docker

```bash
make server
```

## Produção

- .env é **requerido** para iniciar

No make:
```bash
make start-prod # Inicia
make stop-prod # Para
```

Usam a versão `docker-compose.prod.yml`, que é idêntica ao `docker-compose.yml` para n8n e backend,
apenas é adicionado um contêiner do Caddy para fazer proxy reverso ao n8n.

## Notas de inicialização

- Você pode usar a variável de ambiente `LOG_LEVEL` para definir a severidade dos logs;
- Garanta que .env esteja devidamente presente.

## Endpoints do backend

Base local esperada: `http://localhost:8000` (nos contêineres `http://backend:8000`)

- `GET /health` -> verificação de saúde
- `GET /docs/terms` -> termos do Codeforces
- `GET /docs/privacy` -> política de privacidade
- `GET /docs/disclaimer` -> aviso local do projeto
- `GET /api/calendar/primary` -> calendário "Programming Contests Calendar"
- `GET /api/calendar/misc` -> calendário "Misc Codeforces Calendar"
- `GET /api/calendar/all` -> todos os calendários
- `GET /api/calendar/{calendário}/events` -> eventos do calendário especificado
- `GET /api/problemset/problems` -> todos os problemas do Codeforces
- `GET /api/problemset/problems/{id¹}` -> um problema do Codeforces
- `GET /api/contests` -> todas as contests do Codeforces
- `GET /api/contests/{id²}` -> uma contest (ou concurso, se traduzir literalmente) do Codeforces

¹O ID de um problema é composto por duas partes:
  - ID da Contest: Um valor numérico como 4, 2251 etc.
  - Índice: Uma composição de letra e número para:
    - Indicar a posição naquela contest, como A, B, C...
    - Indicar a variação daquele problema.
    Por exemplo: A (primeiro problema), C2 (segunda variante do terceiro problema).
  - Com isso temos IDs como 4A, 2255E1, 1169B etc.

²O ID da contest é numérico, como descrito acima.

## Workflows do n8n

Arquivos versionados em:

- `workflows/gpc-agent.json`
- `workflows/gpc-docs.json`

Exportar workflows do container n8n para a pasta local:

```bash
make export-workflows
```

Observação: o processo usa `scripts/copy_workflows.py` para copiar e renomear
os arquivos com base no campo `name` do JSON.

Importar workflows:

```bash
make import-workflows
```

Note que terá que inserir manualmente quaisquer credenciais usados.

## Limpeza do ambiente

```bash
make clean
```

Esse alvo remove virtualenv, cache Python, artefatos egg-info, recursos
Docker e quaiquer arquivos relacionados ao projeto.

## Troubleshooting

- Se `terms/privacy` falharem, valide conectividade e possíveis bloqueios
  externos.
- O backend depende de resposta HTTP do Codeforces para atualização desses
  documentos e demais dados.
- Em ambientes MSYS2 no Windows, há tratamento no `Makefile` para conversão
  de paths no export de workflows.

## Próximos passos

- [x] Consulta ao banco de questões por rating/tags e demais filtros
- [x] Consulta as contests
- [x] Calendário de contests usando Google Calendar API
- [x] Adicionar logging para o backend
- [x] deploy para AWS
- [!] Melhorar em relação ao modelo e RAG¹
- [ ] Busca de enunciados de cada problema
- [ ] FAQ, via API oficial e blogs do Codeforces
- [ ] Suporte a dúvidas de programação em C/C++

¹A primeira calibração será feita e está em progresso

## Contato

Para dúvidas ou problemas, utilize:

- https://github.com/jppgmx/gpc
