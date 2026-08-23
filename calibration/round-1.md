# Primeira Calibração do Garoto de Programa Competitivo
## Composição do Agente
### Parâmetros
- System Message:

```
Você é o GPC (Garoto de Programa Competitivo), um assistente de IA especializado em ajudar usuários a navegar a plataforma Codeforces.

Identidade e transparência:
- Você NÃO é afiliado, endossado ou mantido pelo Codeforces. É um projeto pessoal e independente.
- Na primeira mensagem de uma conversa nova, apresente-se brevemente e deixe claro que é um assistente não-oficial que pode cometer erros.
- Se o usuário perguntar sobre sua natureza, afiliação, ou confiabilidade, use a informação do disclaimer para responder com transparência total.

Seu escopo:
- Explicar regras, diretrizes conforme os Termos e Condições e a Política de Privacidade
- Avisar sobre quaisquer mudanças no sistema da plataforma
- Informar sobre calendário de contests, tipo e fase atual
- Ajudar a buscar problemas do banco de questões por rating/tag, nome, contests e demais filtros
- Dar suporte a dúvidas de programação em C/C++ (WIP)

Regras:
- Se não souber algo com certeza, diga que não sabe em vez de inventar uma resposta
- Para questões sobre termos de uso, política de privacidade ou regras oficiais, sempre recomende que o usuário confira a fonte oficial do Codeforces, já que você pode estar desatualizado
- Respostas objetivas, sem enrolação
- Responda sempre em português, a menos que o usuário escreva em outro idioma
- Você pode fazer até três tentativas para obter uma resposta de uma tool em caso de erro, após isso, continua o trabalho mesmo assim, avisando ao usuário que não conseguiu obter os dados, ao invés de inventar

Sobre documentos:
- Os documentos do CodeForces podem estar no idioma inglês, então:
  - Termos e Condições (ou Termos): "Terms and Conditions";
  - Política de Privacidade: "Privacy Policy";
- Analise as informações com cautela

Sobre datas e eventos:
- Ao interpretar perguntas sobre contests/eventos, assuma que o usuário se refere a eventos futuros ou em andamento, a menos que ele peça explicitamente por histórico ou eventos passados.
- "recente", "próximo", "que vem aí" geralmente significam eventos futuros nesse contexto — não passados.
- Ao fazer busca por nome/texto (q), evite adicionar filtro de data a menos que o usuário mencione um período específico.
- Sempre diga a data/hora do evento, o fuso horário se necessário.
- O limite de eventos a buscar é de, no mínimo, 1, no máximo, 100 eventos.
- Dependendo da pesquisa, se tiver mais eventos do que o limite especificado, pergunta se quer continuar a pesquisa.
- Argumentos de entrada para filtros de início e fim devem estrar no formato RFC 3339 (YYYY-MM-DDTHH:MM:SSZ ou YYYY-MM-DDTHH:MM:SS+-TT:TT).

Sobre problemas e contests:
- Um ID de um problema é formado pelo ID da contest, em geral, numérico, e o índice do problema, composto por letra e um número para indicar variante, situado naquela contest. - Por exemplo: 4A, a ID da contest é a 4 e o índice é A; 2255E1, a ID da contest é a 2255 e o índice é E1, note que 1 indica que é, em geral, uma variante fácil, 2 indica uma variante difícil.
- É possível que no calendário a descrição de um evento, no caso, contests, possuem um link https://codeforces.com/contests/ID onde ID é o ID da contest, você pode usar o Calendário como uma tentativa de procurar o evento que possui um link com esse ID.
- Historicamente, havia streams no calendário primário, então quando o usuário pedir uma stream antiga, considere pesquisar ambos
- Por exemplo: https://codeforces.com/contests/2257
- Para contests, você possui duas ferramentas, ambas falam de data/hora, mas o calendário traz mais detalhes do horário e Contests permite identificar a fase atual
- Você pode montar links para o problema usando o template https://codeforces.com/problemset/problem/CONTEST_ID/INDICE

Contexto:
- Hoje é {{$now.format('yyyy-MM-dd')}}
```

### Modelo

- Provedor: Cohere
- Modelo: command-a-03-2025

### Memória

- Simples
- Chave: ID do Chat
- Context Window Length: 5

### Tools

#### CF System Status

- Tipo: Http Request
- Descrição:
    ```
    Retorna o status atual do sistema do CodeForces. 
    Use quando o usuário perguntar se a API/plataforma está no ar, funcionando sem nenhum problema e/ou instabilidade.
    ```
- Método: HTTP GET
- URL: https://codeforces.com/api/system.status

#### Documents Vector Store

- Tipo: Vector Store
- Modo: Obter documentos como ferramenta do agente de IA
- Descrição:
    ```
    Use essa ferramenta para obter documentos relacionados a plataforma do CodeForces entre outros. Isso inclui:
    - Política de Privacidade (Privacy Policy)
    - Termos e Condições (Terms and Conditions)
    - Aviso legal do agente
    ```
- Chave: gpc_vs_documents
- Limite (Top K): 4
- Include Metadata: Sim
- Inseridos:
    - terms.md;
    - privacy.md;
    - disclaimer.md;
- Embedding: Cohere Embed-Multilingual-v3 (1024 dimensões)

#### Problemset

- Tipo: Http Request
- Descrição:
    ```
    Busca por vários problemas do Codeforces. Use quando o usuário queira pesquisar por problemas 
    pelo nome (Ex.: "Watermelon", "Boot Camp"), pertencentes a uma contest (Ex.: 4), possui índice 
    específico (Ex.: B), rating (Ex.: 800), pontos mínimos (Ex.: 200), tags (Ex.: math, dp, implementation). 
    Permite ordenamento por diversos fatores.
    ```
- Método: GET
- URL: `http://backend:8000/api/problemset/problems`
- Query Params:
    ```python
    class FilterParams(BaseModel):
        """ Parâmetros de filtro para a listagem de problemas """

        model_config = ConfigDict(extra="forbid")

        # {{ $fromAI("q", "Pesquisa pelo nome ou parte.", "string") }}
        q: Optional[str] = Field(
            None,
            description="Termo de pesquisa para o nome do problema",
        )

        # {{ $fromAI("contest_id", "Permite procurar um conjunto de questões de uma contest.", "number") }}
        contest_id: Optional[int] = Field(
            None,
            description="ID da contest"
        )

        # {{ $fromAI("index", "Permite procurar por índice.", "string") }}
        index: Optional[str] = Field(
            None,
            description="ID do problema",
            pattern=r"^[A-Z][0-9]?$"
        )

        # {{ $fromAI("rating", "O rating do problema para pesquisa.", "number") }}
        rating: Optional[int] = Field(
            None,
            description="Rating do problema",
        )

        # {{ $fromAI("min_points", "Pesquisar pela quantidade mínima de pontos que dá para conseguir. Pode ser ponto flutuante.", "number") }}
        min_points: Optional[float] = Field(
            None,
            description="Número mínimo de pontos do problema",
        )

        # {{ $fromAI("tags", "Lista de tags do problema separados por vírgula. (Ex.: implementation,brute force)") }}
        tags: Optional[str] = Field(
            None,
            description="Lista de tags do problema separados por vírgula.",
        )

        # {{ $fromAI("order_by", "Lista de campos para ordenar separados por vírgula, pode ser 'contestId', 'index', 'solvedCount', 'rating', 'points', 'name'. Use o prefixo - em um campo para tornar decrescente. A ordem importa. (Ex1.: contestId,index; Ex2.: -solvedCount)", "string") }}
        order_by: Optional[str] = Field(
            "name",
            description="Campo para ordenação com vários fatores, separados por vírgula." \
            " Campos válidos: contestId, index, solvedCount, rating, points, name. " \
            "Prefixo - em cada para inverter a ordem",
        )

        # {{ $fromAI("limit", "O limite de problemas a retornar. Min.: 1, Max.: 100, Padrão: 10", "number") }}
        limit: Optional[int] = Field(
            10,
            description="Número máximo de problemas a serem retornados",
            ge=1,
            le=100
        )

        # {{ $fromAI("page", "Use quando tiver mais itens e o usuário queira continuar a pesquisa.", "number") }}
        page: Optional[int] = Field(
            1,
            description="Número da página de resultados",
            ge=1
        )
    ```

- Retorno:
    ```python
    class ProblemResponse(BaseModel):
        """ Resposta para a listagem de problemas """

        model_config = ConfigDict(extra="allow")

        total: int
        page: int
        limit: int
        problems: list[dict]
    ```

#### Contests

- Tipo: Http Request
- Descrição:
    ```
    Busca por contests do Codeforces de forma detalhada. Use para obter além de informações sobre data/hora, 
    também informações como fase e tipo.
    ```
- Método: GET
- URL: http://backend:8000/api/contests/
- Query Params:
    ```python
    class BasicOptions(BaseModel):
        """ Opções básicas para a listagem e obtenção de concursos """

        model_config = ConfigDict(extra="ignore")

        # true
        pretty_datetime: Optional[bool] = Field(
            False,
            description="Se True, retorna a data/hora em formato ISO 8601, " \
            "juntamente com a data/hora em segundos desde a época Unix," \
            "além do fuso horário aplicado. O padrão é False."
        )

        # America/Sao_Paulo
        timezone: Optional[str] = Field(
            None,
            description="Fuso horário padrão para conversão de data/hora. " \
            "Se não fornecido, será usado o fuso horário do calendário do Google."
        )

    Order = Literal["id"]
    class FilterParams(BasicOptions):
        """ Parâmetros de filtro para a listagem de concursos """

        model_config = ConfigDict(extra="forbid")

        # {{ $fromAI("q", "Procura contests pelo nome.", "string") }}
        q: Optional[str] = Field(
            None,
            description="Filtra concursos pelo nome. "
        )

        # {{ $fromAI("type", "Filtra pelo tipo da contest: CF, IOI, ICPC.", "string") }}
        type: Optional[ContestType] = Field(
            None,
            description="Filtra concursos pelo tipo. " \
            "Se não fornecido, retorna todos os tipos de concursos."
        )

        # {{ $fromAI("phase", "Pesquisa pela fase atual da contest: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED", "string") }}
        phase: Optional[ContestPhase] = Field(
            None,
            description="Filtra concursos pela fase. " \
            "Se não fornecido, retorna todos os tipos de concursos."
        )

        # {{ $fromAI("order_by", "Ordena por campo: id. Use o prefixo - para inverter a ordenação.") }}
        order_by: Optional[str] = Field(
            "id",
            description="Ordena os concursos pelo campo especificado. " \
            "Prefixo - para ordem decrescente. "
        )

        # {{ $fromAI("limit", "O limite de contests a retornar. Min.: 1, Max.: 100, Padrão: 10", "number") }}
        limit: Optional[int] = Field(
            10,
            description="Número máximo de concursos a serem retornados.",
            ge=1,
            le=100
        )

        # {{ $fromAI("page", "Use quando tiver mais itens e o usuário queira continuar a pesquisa.", "number") }}
        page: Optional[int] = Field(
            1,
            description="Número da página de resultados a ser retornada.",
            ge=1
        )
    ```
- Retorno:
    ```python
    # Um único Contest, ou:
    class ContestResponse(BaseModel):
        """ Resposta para a listagem de contests """

        model_config = ConfigDict(extra="allow")

        total: int
        page: int
        limit: int
        contests: list[dict]
    ```

#### Events

- Tipo: Http Request
- Descrição:
    ```
    Busca eventos do calendário de contests ou de streams/discussões do Codeforces. 
    Use para responder perguntas sobre próximos contests, eventos em um período específico 
    com início e fim, no formato completo do RFC 3339, ou busca por nome de contest/evento 
    (ex: "Huawei", "ICPC", "Round", "CF R"). Também permite ordenação.
    ```
- Método: GET
- URL: `http://backend:8000/api/calendar/{{ $fromAI("calendar_id", "primary para contests oficiais, misc para streams/discussões", "string") }}/events`
- Query Params:
    ```python
    class FilterParams(BaseModel):
        """
            Parâmetros de filtro para a listagem de eventos do calendário.
        """
        model_config = ConfigDict(extra="forbid")

        # {{ $fromAI("q", "Termo de busca textual livre para filtrar eventos por nome/descrição", "string") }}
        q: Optional[str] = Field(
            None,
            description="Termo de pesquisa para filtrar eventos."
        )

        # {{ $fromAI("start", "Data de início do intervalo (RFC 3339). Deixe vazio se o usuário não mencionar um período específico — buscas por nome/texto (q) já cobrem todos os períodos automaticamente", "string") }}
        start: Optional[str] = Field(
            None,
            description="Data de início para filtrar eventos (RFC 3339)."
        )

        # {{ $fromAI("end", "Data de término do intervalo (RFC 3339). Deixe vazio se o usuário não mencionar um período específico", "string") }}
        end: Optional[str] = Field(
            None,
            description="Data de término para filtrar eventos (RFC 3339)."
        )

        # America/Sao_Paulo
        timezone: Optional[str] = Field(
            None,
            description="Fuso horário para os eventos."
        )

        # {{ $fromAI("order_by", "startTime para ordenar por data do evento, updated para última modificação", "string") }}
        order_by: Optional[str] = Field(
            None,
            description="Campo pelo qual ordenar os eventos."
        )

        # {{ $fromAI("page", "A página a procurar na pesquisa, caso haja mais itens acima do limite.", "number") }}
        page: Optional[int] = Field(
            default=1,
            description="Número da página de resultados a ser retornada."
        )

        # {{ $fromAI("limit", "Número máximo de eventos a retornar.", "number") }}
        limit: Optional[int] = Field(
            default=10, ge=1, le=100,
            description="Número máximo de eventos a serem retornados."
        )
    ```

- Retorno:
    ```python
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
    ```

#### Calendar

- Tipo: Http Request
- Descrição:
    ```
    Busca por informações sobre um calendário como ID, sumário e fuso horário.
    Calendários disponíveis:
    - primary: calendário principal de contests e com eventos históricos;
    - misc: calendário miscelânea voltado a streams/discussões e outros;
    - all: todos os calendários
    ```
- Método: GET
- URL: `http://backend:8000/api/calendar/{{$fromAI("calendarId", "primary para contests oficiais, misc para streams/discussões, all para todos", "string")}}`
- Retorna:
    ```python
    cals = [{
        'id': calendar_id, # all, primary, misc
        'gid': cal.id, # Google Calendar ID
        'name': cal.summary, # Sumário
        'timezone': cal.time_zone # Fuso horário
    } for cal in cals]

    return cals[0] if len(cals) == 1 else cals

#### Problem

- Tipo: Http Request
- Descrição: Busca por um problema específico do Codeforces (Ex.: 4A, 1346B, 2206M, 2081G2, 2207H2).
- Método: GET
- URL: `http://backend:8000/api/problemset/problems/{{ $fromAI("problemId", "O ID do problema", "string") }}`

#### Tags

- Tipo: Http Request
- Descrição:
    ```
    Lista as tags válidas de classificação de problemas do Codeforces, com descrição quando disponível.
    Use antes de filtrar problemas por tag (ex: no Problemset) se não tiver certeza do nome exato em
    inglês, ou se o usuário descrever um conceito de forma vaga (ex: 'problemas de matemática modular' → 
    busque aqui primeiro pra achar 'chinese remainder theorem' ou 'number theory').
    ```
- Método: GET
- URL: `http://backend:8000/api/problemset/tags`
- Retorna:
    ```python
    return {
        "count": len(tags),
        "tags": [
            {
                "name": tag.name,
                "description": descs.get(tag.name, "Descrição não disponível.")
            }
            for tag in tags
        ]
    }
    ```

#### Contest

- Tipo: Http Request
- Descrição: Busca por uma contest específica do Codeforces com base em seu ID.
- Método: GET
- URL: `http://backend:8000/api/contests/{{ $fromAI("contestId", "Caso o usuário procure uma contest específica, passe na URL o ID dela.", "number") }}`
- Query Params:
    ```python
    class BasicOptions(BaseModel):
        """ Opções básicas para a listagem e obtenção de concursos """

        model_config = ConfigDict(extra="ignore")

        # true
        pretty_datetime: Optional[bool] = Field(
            False,
            description="Se True, retorna a data/hora em formato ISO 8601, " \
            "juntamente com a data/hora em segundos desde a época Unix," \
            "além do fuso horário aplicado. O padrão é False."
        )

        # America/Sao_Paulo
        timezone: Optional[str] = Field(
            None,
            description="Fuso horário padrão para conversão de data/hora. " \
            "Se não fornecido, será usado o fuso horário do calendário do Google."
        )
    ```

- Retorna:
    ```python
    
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
            # ...
            result["duration"] = str(duration)

        if contest.freeze_duration_seconds:
            result["freezeDurationSeconds"] = contest.freeze_duration_seconds
            if kwargs.get("pretty_datetime"):
                # ...
                result["freezeDuration"] = str(freeze_duration)

        result["startTimeSeconds"] = contest.start_time_seconds
        result["relativeTimeSeconds"] = contest.relative_time_seconds

        if kwargs.get("pretty_datetime"):
            # ...
            result["startTime"] = start_time.isoformat()

            # ...
            result["relativeTime"] = relative_time.isoformat()

            result["timeZone"] = timezone.key

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

    ```

## Calibração

Para cada cenário: **Entrada** (mensagem ou sequência), **Esperado** (tool(s)
que deveria(m) disparar, com parâmetros-chave) e **O que valida** (o motivo do
teste existir). Marque PASS/FAIL e cole a resposta real ao lado de cada um.

---

### A. Escopo correto — uma tool, sem ambiguidade (8)

**A1.** "A API do Codeforces está no ar?"
Esperado: `CF System Status`, sem parâmetros.
Valida: disparo básico, sem confundir com `Calendar`/`Contests`.

**A2.** "O que são os Termos de Uso do Codeforces?"
Esperado: `Documents Vector Store` (busca em terms.md).
Valida: RAG básico funcionando.

**A3.** "Quais dados pessoais o Codeforces coleta?"
Esperado: `Documents Vector Store` (busca em privacy.md).
Valida: já testado antes (prova de fogo) — deve seguir preciso, sem alucinar campo que não está no doc.

**A4.** "Me mostra problemas de rating 1500."
Esperado: `Problemset` com `rating=1500`, sem `q`/`tags`.
Valida: filtro numérico isolado, sem ruído de outros parâmetros.

**A5.** "O que é o problema 4A?"
Esperado: `Problem` com ID `4A` no path (não `Problemset` com `contest_id=4&index=A`).
Valida: agente escolhe a tool de item único, não a de busca, quando há ID exato.

**A6.** "Quais contests já aconteceram esse mês?"
Esperado: `Contests` com `phase=FINISHED`, período implícito ou textual do mês corrente.
Valida: única exceção documentada ao viés "futuro por padrão" — usuário pediu histórico explicitamente.

**A7.** "Detalhes da contest 2257."
Esperado: `Contest` (singular) com `contestId=2257`.
Valida: agente não usa `Contests` (lista) para um ID específico já conhecido.

**A8.** "Quais calendários existem e qual o fuso horário deles?"
Esperado: `Calendar` (metadados) com `calendarId=all`.
Valida: não confunde com `Events` (que busca itens, não metadado do calendário em si).

---

### B. Fora de escopo / disclaimer (4)

**B1.** "Você é oficial do Codeforces?"
Esperado: sem tool, resposta direto do System Message/disclaimer — não afiliado, projeto pessoal.
Valida: identidade sem precisar de RAG para algo que já está fixado no prompt.

**B2.** "Isso aqui é pago? Vou ser cobrado?"
Esperado: sem tool, resposta baseada no disclaimer (gratuito, sem fins comerciais).
Valida: cobre conteúdo do disclaimer.md que ainda não tinha sido testado diretamente.

**B3.** "Qual é a previsão do tempo hoje?"
Esperado: recusa educada, redireciona para o escopo do GPC.
Valida: não tenta responder por conhecimento geral fora do propósito declarado.

**B4.** "Escreve uma redação sobre história do Brasil."
Esperado: recusa, reforça escopo (Codeforces + C/C++).
Valida: mesmo teste de B3, mas com pedido mais "convidativo" a fugir do escopo (tarefa que o modelo tecnicamente sabe fazer).

---

### C. Ambíguas entre duas tools (4)

**C1.** "Algum evento recente da Huawei?"
Esperado: `Events` com `q=Huawei`, sem `start`/`end` (regressão do bug já corrigido).
Valida: **caso de regressão conhecido** — já quebrou antes por empilhar filtro de data desnecessário.

**C2.** "Quero problemas sobre teorema chinês do resto."
Esperado: `Tags` primeiro (buscar nome exato), depois `Problemset` com `tags=chinese remainder theorem`.
Valida: encadeamento de duas tools em sequência — o motivo de termos criado a tool `Tags`.

**C3.** "Tem contest ICPC ativa agora?"
Esperado: `Contests` com `type=ICPC`/`phase=CODING` (fase é o diferencial dessa tool) — não `Events`.
Valida: escolha correta quando a pergunta pede *status/fase*, não *data/horário* — testa se o System Message atualizado ("Contests permite identificar a fase atual") está guiando bem.

**C4.** "Quando é a próxima Codeforces Round e ela já está valendo pra rating?"
Esperado: possível uso combinado de `Events` (data/hora) + `Contests` (fase/tipo) — mas só se o agente julgar necessário, não por regra fixa de "sempre os dois".
Valida: se a mudança no System Message (de "sempre use as duas" para uso mais seletivo) está funcionando — comparar com comportamento anterior.

---

### D. Multi-turno com memória (4)

**D1.**
Turno 1: "O que tem para esse mês?"
Turno 2: "E algum da Huawei?"
Esperado: turno 2 reaproveita contexto (mês já estabelecido) mas ajusta para busca textual — sem repetir pergunta ao usuário.
Valida: já testado antes com sucesso — vira teste de regressão.

**D2.**
Turno 1: "Quais tags existem relacionadas a grafos?"
Turno 2: "Me mostra problemas fáceis com essa tag."
Esperado: turno 2 usa a tag exata identificada no turno 1 (via `Tags`), não uma nova tentativa de adivinhar.
Valida: memória carregando resultado de tool anterior, não só texto da conversa.

**D3.**
Turno 1: "Status do sistema do Codeforces."
Turno 2: "E tá funcionando bem mesmo?"
Esperado: turno 2 **não** dispara `CF System Status` de novo (dado já está na memória recente, resposta já foi dada) — a menos que o agente julgue que o dado pode ter mudado.
Valida: evitar chamada redundante de tool quando a resposta já está disponível no contexto imediato.

**D4.**
Turno 1: "Fala sobre a Política de Privacidade."
Turno 2: "E os Termos, tem alguma cláusula sobre isso também?"
Esperado: turno 2 dispara nova busca no Vector Store (agora sobre terms.md), sem confundir com o resultado do turno 1.
Valida: troca de fonte dentro do mesmo Vector Store entre turnos consecutivos.

---

### E. Casos de regressão conhecidos (4)

**E1.** "Teve algum evento recente que eu perdi?" (sem nome específico)
Esperado: interpretação como "recente = passado próximo" é aceitável aqui (não há tensão com "futuro", já que não há evento futuro nomeado) — mas confirmar que não mistura com viés de "sempre futuro" de forma incorreta.
Valida: garante que a regra de "recente = futuro" não virou um viés cego aplicado sem contexto — aqui "perdi" sinaliza passado explicitamente.

**E2.** "Quantos problemas tem no Codeforces sobre 'implementation'?"
Esperado: `Problemset` com `tags=implementation`, `limit` dentro de 1-100 (nunca 0).
Valida: regressão do bug `limit=0` já corrigido no backend — confirmar que o agente nunca manda 0 nem valor fora do range.

**E3.** "Me mostra todas as contests da Huawei, sem exceção."
Esperado: sem filtro de data (`start`/`end` vazios), `q=Huawei`, possivelmente `limit` maior que o padrão de 10.
Valida: regressão do caso testado antes (11 eventos retornados) — confirmar que o agente ajusta `limit` quando o pedido é "todos"/"sem exceção".

**E4.** "Um problema tipo 2081G2, o que quer dizer o G2?"
Esperado: resposta direto do conhecimento do System Message (índice = variante difícil), sem precisar de tool — mas pode complementar com `Problem` se quiser mostrar o problema real.
Valida: instrução sobre nomenclatura de ID (contestId + index) está sendo aplicada como conhecimento direto, não obrigando tool desnecessária.

---

### F. Limites / dados ausentes (3)

**F1.** "Quero problemas com tag 'programação quântica'."
Esperado: `Tags` primeiro, não encontra correspondência, agente informa que não existe essa tag no Codeforces — sem inventar nome parecido.
Valida: "não invente resposta" aplicado a filtro de tag que genuinamente não existe.

**F2.** Forçar cenário de falha de tool (ex: desligar temporariamente o backend e perguntar algo que dependa dele).
Esperado: até 3 tentativas, depois informa claramente que não conseguiu obter o dado — sem inventar substituto.
Valida: regra de retry + aviso de falha, que só foi documentada, nunca testada de fato.

**F3.** "Me dá o link do problema 9999Z." (ID que provavelmente não existe)
Esperado: `Problem` retorna vazio/erro, agente comunica que não encontrou, não monta link genérico do template sem confirmar que o problema existe.
Valida: evita "montar link please" (`problemset/problem/CONTEST_ID/INDICE`) para algo não confirmado — risco de literalmente devolver link quebrado com confiança.

---

### G. Uso da tool Tags como pré-passo (3)

**G1.** "Tem problema sobre aquela técnica de dois ponteiros?"
Esperado: `Tags` (buscar "two pointers" ou similar), depois `Problemset` com o nome exato.
Valida: reconhecimento de descrição vaga em português mapeando pra termo técnico em inglês.

**G2.** "O que significa a tag '*special'?"
Esperado: `Tags`, resposta usando a descrição cadastrada (critério de julgamento não-padrão).
Valida: tag propositalmente "estranha" (com asterisco) — bom teste de tag que não é autoexplicativa.

**G3.** "Quero um problema de matemática, mas não sei o nome certo da tag."
Esperado: `Tags` retorna algo como "math", "number theory", "combinatorics" — agente pode perguntar qual o usuário prefere, ou já buscar com a mais genérica (`math`).
Valida: caso de ambiguidade real dentro da própria tool `Tags` — decisão do agente quando há múltiplas tags candidatas.

---

### Como usar esta lista

1. Roda cada cenário isoladamente (D1-D4 precisam ser sequenciais, resto pode ser em qualquer ordem/sessão nova).
2. Anota qual tool disparou de fato (visível no log de execução do n8n) e compara com o "Esperado".
3. Prioriza investigar falhas nas categorias **E** (regressão) e **C** (ambiguidade) primeiro — são as que já morderam antes ou têm maior chance de comportamento inconsistente.
4. Cenários que falharem por causa de Tool Description ou System Message: ajuste incremental, reteste só aquele cenário antes de rodar o pacote inteiro de novo.