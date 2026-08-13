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

### Agente (n8n)

O GPC é um agente de IA (modelo Cohere) com memória de conversa, acessível via
chat (local do n8n), com as seguintes ferramentas disponíveis:

- Consulta de status do sistema Codeforces (`system.status`)
- Busca semântica (RAG) sobre Termos, Privacidade e o aviso de transparência
  do próprio projeto

### Fluxo de documentos (backend)

1. `terms` e `privacy` são buscados de `codeforces.com`.
2. O conteúdo HTML é filtrado e convertido para Markdown.
3. O resultado é armazenado em cache dentro de `.data`.
4. `disclaimer` é servido a partir de um arquivo local, sem busca externa.

## Estrutura do repositório

```text
.
├── docker-compose.yml
├── Makefile
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── api/docs.py
│   │   ├── models/
│   │   └── services/
│   └── .data/
│       └── docs/
├── scripts/
│   └── copy_workflows.py
└── workflows/
    ├── gpc-agent.json
    └── gpc-docs.json
```

## Pré-requisitos

- Docker
- Docker Compose
- Python 3.12 (para desenvolvimento local do backend)
- `make` (opcional, mas recomendado)

## Setup rápido (desenvolvimento)

Com `make`:

```bash
make setup
```

Esse alvo:

- cria o virtualenv em `backend/.venv`;
- instala dependências de `backend/requirements.txt`;
- instala o backend em modo editável (`pip install -e .`).

## Executando com Docker

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

## Endpoints do backend

Base local esperada: `http://localhost:8000`

- `GET /health` -> verificação de saúde
- `GET /docs/terms` -> termos do Codeforces
- `GET /docs/privacy` -> política de privacidade
- `GET /docs/disclaimer` -> aviso local do projeto

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

## Limpeza do ambiente

```bash
make clean
```

Esse alvo remove virtualenv, cache Python, artefatos egg-info e recursos
Docker relacionados ao projeto.

## Troubleshooting

- Se `terms/privacy` falharem, valide conectividade e possíveis bloqueios
  externos.
- O backend depende de resposta HTTP do Codeforces para atualização desses
  docs.
- Em ambientes MSYS2 no Windows, há tratamento no `Makefile` para conversão
  de paths no export de workflows.

## Próximos passos

- [ ] Consulta ao banco de questões por rating/tags e demais filtros
- [x] Calendário de contests usando Google Calendar API
- [ ] FAQ, via API oficial e blogs do Codeforces
- [ ] Suporte a dúvidas de programação em C/C++
- [ ] Melhorar em relação ao modelo e RAG¹

¹Com a adição do serviço de Calendário e o nodo ferramenta, venho tentando calibrar o uso da ferramenta,
além de outras otimizações na parte do Vector Store.

## Contato

Para dúvidas ou problemas, utilize:

- https://github.com/jppgmx/gpc