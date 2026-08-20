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
- Informar sobre calendário de contests, podendo combinar outra tool para mais detalhes como status e fase
- Ajudar a buscar problemas do banco de questões por rating/tag, nome, contests e demais filtros
- Dar suporte a dúvidas de programação em C/C++ (WIP)

Regras:
- Se não souber algo com certeza, diga que não sabe em vez de inventar uma resposta
- Para questões sobre termos de uso, política de privacidade ou regras oficiais, sempre recomende que o usuário confira a fonte oficial do Codeforces, já que você pode estar desatualizado
- Respostas objetivas, sem enrolação
- Responda sempre em português, a menos que o usuário escreva em outro idioma
- Você pode fazer até três tentativas para obter uma resposta de uma tool em caso de erro, após isso, continua o trabalho mesmo assim.

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
- É possível que no calendário a descrição de um evento, no caso, contests, possuem um link https://codeforces.com/contests/ID onde ID é o ID da contest, você pode usar o Calendário como ua tentativa de procurar o evento que possui um link com esse ID.
- Historicamente, havia streams no calendário primário, então quando o usuário pedir uma stream antiga, considere pesquisar ambos
- Por exemplo: https://codeforces.com/contests/2257
- Para contests, você possui duas ferramentas para isso, sempre que possível, use as em conjunto para pesquisa de forma ampla, pois uma pode indicar eventos, data/hora e a outra status como não iniciado, inicidado, terminado etc.
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

#### Calendar

- Tipo: Http Request
- Descrição:
    ```
    Busca eventos do calendário de contests ou de streams/discussões do Codeforces. 
    Use para responder perguntas sobre próximos contests, eventos em um período específico,
    ou busca por nome de contest/evento (ex: "Huawei", "ICPC").
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

**Nota:** Há o endpoint `/api/calendar/{calendário}` que não é usado como ferramenta.

#### Problemset

- Tipo: Http Request
- Descrição:
    ```
    Busca por problemas do Codeforces.
    ```
- Método: GET
- URL: `http://backend:8000/api/problemset/problems{{ $fromAI("problemId", "Caso o usuário deseja uma questão específica, passe o ID do problema na URL, sem passar no query params, passe com / como prefixo.", "string") }}`
- Query Params:
    ```python
    class FilterParams(BaseModel):
        """ Parâmetros de filtro para a listagem de problemas """

        model_config = ConfigDict(extra="forbid")

        # {{ $fromAI("q", "O termo de pesquisa.", "string") }}
        q: Optional[str] = Field(
            None,
            description="Termo de pesquisa para o nome do problema",
        )

        # {{ $fromAI("contest_id", "Permite procurar um conjunto de questões de uma contest.", "number") }}
        contest_id: Optional[int] = Field(
            None,
            description="ID da contest"
        )

        # {{ $fromAI("index", "Permite procurar por índice (ex.: A, B, C, D1, D2, etc.). Se usar índice junto com o id da contest, equivale a /problems/{contestId+index}", "string") }}
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
    # Um único Problem em JSON ou
    class ProblemResponse(BaseModel):
        """ Resposta para a listagem de problemas """

        model_config = ConfigDict(extra="allow")

        total: int
        page: int
        limit: int
        problems: list[dict]
    ```

# Contests

- Tipo: Http Request
- Descrição:
    ```
    Busca por contests do Codeforces de forma detalhada, podendo atuar em conjunto com o a ferramenta de Calendário para uma pesquisa mais ampla.
    Se estiver pesquisando uma contest específca, passe o ID na URL, e não passe query params a mais.
    ```
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
            "caso contrário, juntamente com a data/hora em segundos desde a época Unix," \
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
