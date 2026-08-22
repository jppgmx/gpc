# Resultado da Primeira Rodada de Calibração do GPC (A-2)

## Espera-se
- Problema do Telegram corrigido;
- Problema de query params desnecessários corrigido;
- Um pouco mais de detalhes da documentação;
- Termos como CF, CODING, FINISHED naturalizados em algo como Codeforces, Codando, Terminado etc.

## O que foi calibrado

- Ajuste no Top K do Vector Store para 5;
- Instruções na tool Problemset para omitir query params desnecessários;
```
Deixe vazio/omita se não for relevante para a pergunta — não preencha com valor padrão.
```
- Novas instruções para naturalizar os termos;
```
- Palavras como "FINISHED", "CODING", "CF", "PENDING_SYSTEM_TEST", "PROGRAMMING" e outros,
tente traduzir/naturalizar esses termos e demais (Ex.: Terminado, "Codando", Codeforces, Testes do Sistema Pendente)
```
- Ajuste no FilterParams da problemset
    ```python
    @field_validator("contest_id", "rating", "min_points", "page", "limit", mode="before")
    @classmethod
    def zero_to_none(cls, v: int | None):
        """ Converte 0 em None """
        if v == 0:
            return None
        return v
    @field_validator("q", "index", "tags", "order_by", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: str | None):
        """ Converte string vazia em None """
        if v == "":
            return None
        return v
    ```
- De query params fixos agora é um JSON dinâmico:
    - Problemset:
    ```js
    {{ 
        JSON.stringify((() => {
        const NUMERIC_FIELDS = new Set(["contest_id", "rating", "min_points", "limit", "page"]);
        const params = {
            q: $fromAI("q", "Pesquisa pelo nome ou parte.", "string", undefined),
            contest_id: $fromAI("contest_id", "Permite procurar um conjunto de questões de uma contest.", "number"),
            index: $fromAI("index", "Permite procurar por índice (ex.: A, B, C, D1, D2)", "string"),
            rating: $fromAI("rating", "O rating do problema para pesquisa.", "number"),
            min_points: $fromAI("min_points", "Pesquisar pela quantidade mínima de pontos. Pode ser ponto flutuante.", "number"),
        tags: $fromAI("tags", "Lista de tags separadas por vírgula (Ex.: \"brute force,math,dp\")", "string"),
            order_by: $fromAI("order_by", "Lista de campos para ordenar separados por vírgula, pode ser 'contestId', 'index', 'solvedCount', 'rating', 'points', 'name'. Use o prefixo - em um campo para tornar decrescente. A ordem importa. (Ex1.: contestId,index; Ex2.: -solvedCount)", "string"),
            limit: $fromAI("limit", "Limite de problemas a retornar (1-100).", "number"),
            page: $fromAI("page", "Página de resultados.", "number"),
        };

        return Object.fromEntries(
            Object.entries(params).filter(([key, v]) => {
                if (v === undefined || v === null || v === "") return false;
                if (NUMERIC_FIELDS.has(key) && v === 0) return false;
                return true;
            })
        );
        })())
    }}
    ```
    - Contests:
    ```js
    {{ 
        JSON.stringify(
            (() => {
            const NUMERIC_FIELDS = new Set(["limit", "page"]);
            const params = {
                pretty_datetime: true,
                timezone: $fromAI("timezone", "O fuso horário a aplicar.", "string", "America/Sao_Paulo"),
                q: $fromAI("q", "Procura contests pelo nome.", "string"),
                type: $fromAI("type", "Filtra pelo tipo da contest: CF, IOI, ICPC.", "string"),
                phase: $fromAI("phase", "Pesquisa pela fase atual da contest: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED", "string"),
                order_by: $fromAI("order_by", "Ordena por campo: id. Use o prefixo - para inverter a ordenação."),
                limit: $fromAI("limit", "O limite de contests a retornar. Min.: 1, Max.: 100, Padrão: 10", "number"),
                page: $fromAI("page", "Use quando tiver mais itens e o usuário queira continuar a pesquisa.", "number")
            }
            return Object.fromEntries(
            Object.entries(params).filter(([key, v]) => {
            if (v === undefined || v === null || v === "") return false;
            if (NUMERIC_FIELDS.has(key) && v === 0) return false;
            return true;
            })
        );
            })()
        )
    }}
    ```
- Trocar modo de parser para HTML, não há opção de texto puro, infelizmente;

---

### A. Escopo correto — uma tool, sem ambiguidade (8)

**A1.** "A API do Codeforces está no ar?"
Esperado: `CF System Status`, sem parâmetros.
Valida: disparo básico, sem confundir com `Calendar`/`Contests`.
Realidade: **Respostas curtas e suficientes**
    - Resposta:
        ```text
        Sim, a API do Codeforces está funcionando normalmente no momento.
        ```
    - Opnião: Foi direto, sem mais detalhes vindos da API do Codeforces.

**A2 (2º Execução).** "O que são os Termos de Uso do Codeforces?"
Esperado: `Documents Vector Store` (busca em terms.md).
Valida: RAG básico funcionando.
Realidade:
    - Fluxo: Trigger -> Garoto -> Memória -> Modelo -> Documents Vector Store + Embeddings -> Memória
      -> Modelo -> Resposta
    - Documents Vector Store:
        - Input: `{"input": "Terms and Conditions"}`
        - Output:
            ```json
            {
                "response": [
                    {
                    "type": "text",
                    "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{\"pageContent\":\"to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\\n\\n### Your Content.\\n\\nIn these Website Terms And Conditions, “Your Content” shall mean any audio, video, text, images or\\nother material you choose to display on this Website. With respect to Your Content, by displaying\\nit, you grant Codeforces a non-exclusive, worldwide, irrevocable, royalty-free, sublicensable\\nlicense to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your\\nContent must be your own and must not be infringing on any third party’s rights. Codeforces reserves\\nthe right to remove any of Your Content from this Website at any time, and for any reason,\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":25,\"to\":35}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{\"pageContent\":\"to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\\n\\n### Your Content.\\n\\nIn these Website Terms And Conditions, “Your Content” shall mean any audio, video, text, images or\\nother material you choose to display on this Website. With respect to Your Content, by displaying\\nit, you grant Codeforces a non-exclusive, worldwide, irrevocable, royalty-free, sublicensable\\nlicense to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your\\nContent must be your own and must not be infringing on any third party’s rights. Codeforces reserves\\nthe right to remove any of Your Content from this Website at any time, and for any reason,\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":25,\"to\":35}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{\"pageContent\":\"e provisions of these Terms.\\n\\n### Severability.\\n\\nIf any provision of these Terms is found to be unenforceable or invalid under any applicable law,\\nsuch unenforceability or invalidity shall not render these Terms unenforceable or invalid as a\\nwhole, and such provisions shall be deleted without affecting the remaining provisions herein.\\n\\n### Variation of Terms.\\n\\nCodeforces is permitted to revise these Terms at any time as it sees fit, and by using this Website\\nyou are expected to review such Terms on a regular basis to ensure you understand all terms and\\nconditions governing use of this Website.\\n\\n### Assignment.\\n\\nCodeforces shall be permitted to assign, transfer, and subcontract its rights and\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":57,\"to\":73}}}}"
                    }
                ]
                }
            ```
        - Resposta:
            ```text
            Os Termos de Uso do Codeforces são as regras e diretrizes que os usuários devem seguir ao utilizar a plataforma. Eles cobrem aspectos como:

            1. **Uso adequado da plataforma**: Proibição de uso para atividades ilegais, spam, ou qualquer atividade que possa prejudicar a plataforma ou outros usuários.
            2. **Conteúdo do usuário**: Ao publicar conteúdo na plataforma, você concede ao Codeforces uma licença não exclusiva, mundial, irrevogável, isenta de royalties e sublicenciável para usar, reproduzir, adaptar, publicar, traduzir e distribuir o conteúdo em qualquer mídia.
            3. **Responsabilidades do usuário**: Os usuários são responsáveis por manter a segurança de suas contas e por qualquer atividade que ocorra em suas contas.
            4. **Alterações nos Termos**: O Codeforces pode revisar os Termos de Uso a qualquer momento, e os usuários são responsáveis por revisar regularmente os Termos para garantir que estejam cientes das regras e diretrizes.

            Aqui estão alguns pontos-chave dos Termos de Uso do Codeforces:

            * **Proibido**: Vender ou transferir sua conta para qualquer pessoa ou entidade comercial; usar a plataforma para publicidade ou marketing.
            * **Seu Conteúdo**: Qualquer áudio, vídeo, texto, imagem ou outro material que você escolha exibir na plataforma é de sua responsabilidade. O Codeforces reserva-se o direito de remover qualquer conteúdo a qualquer momento e por qualquer motivo.

            Para acessar o documento completo dos Termos de Uso, recomendo que você visite o link oficial do Codeforces: https://codeforces.com/terms.

            Lembre-se de que é importante ler e entender os Termos de Uso antes de utilizar a plataforma para garantir que você esteja em conformidade com as regras e diretrizes estabelecidas pelo Codeforces. Se tiver alguma dúvida específica, posso tentar ajudar com base nas informações que tenho disponíveis.
            ```
        - Opinião: Há correspondências do terms.md presentes, boa contextualização

**A3 (2º Execução).** "Quais dados pessoais o Codeforces coleta?"
Esperado: `Documents Vector Store` (busca em privacy.md).
Valida: já testado antes (prova de fogo) — deve seguir preciso, sem alucinar campo que não está no doc.
Realidade:
    - Fluxo: Trigger -> Garoto -> Memória -> Modelo -> Documents Vector Store + Embeddings -> Memória
      -> Modelo -> Resposta
    - Documents Vector Store:
        - Input: `{"input": "Privacy Policy"}`
        - Output:
            ```json
            {
            "response": [
                {
                "type": "text",
                "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
                },
                {
                "type": "text",
                "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
                },
                {
                "type": "text",
                "text": "{\"pageContent\":\"legal action arising from improper\\nuse of this Application or the related services. The User declares to be aware\\nthat the Data Controller may be required to reveal personal data upon request of\\npublic authorities.\\n\\n### Additional information about User's Personal Data\\n\\nIn addition to the information contained in this privacy policy, this\\nApplication may provide the User with additional and contextual information\\nconcerning particular services or the collection and processing of Personal Data\\nupon request.\\n\\n### System logs and maintenance\\n\\nFor operation and maintenance purposes, this Application and any third party\\nservices may collect files that record interaction with this Application (Sy\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":211,\"to\":226}}}}"
                },
                {
                "type": "text",
                "text": "{\"pageContent\":\"legal action arising from improper\\nuse of this Application or the related services. The User declares to be aware\\nthat the Data Controller may be required to reveal personal data upon request of\\npublic authorities.\\n\\n### Additional information about User's Personal Data\\n\\nIn addition to the information contained in this privacy policy, this\\nApplication may provide the User with additional and contextual information\\nconcerning particular services or the collection and processing of Personal Data\\nupon request.\\n\\n### System logs and maintenance\\n\\nFor operation and maintenance purposes, this Application and any third party\\nservices may collect files that record interaction with this Application (Sy\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":211,\"to\":226}}}}"
                },
                {
                "type": "text",
                "text": "{\"pageContent\":\"content\\nfrom external platforms, Registration and authentication, Interaction with\\nexternal social networks and platforms, Geolocation, Managing contacts and\\nsending messages, Infrastructure monitoring and Hosting and backend\\ninfrastructure.\\n\\nThe Personal Data used for each purpose is outlined in the specific sections of\\nthis document.\\n\\n## Detailed information on the processing of Personal Data\\n\\nPersonal Data is collected for the following purposes and using the following\\nservices:\\n\\n### Analytics\\n\\nThe services contained in this section enable the Owner to monitor and analyze\\nweb traffic and can be used to keep track of User behavior. At times we may\\nshare this information in aggregated anony\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"loc\":{\"lines\":{\"from\":64,\"to\":82}}}}"
                }
            ]
            }
            ```
        - Resposta:
            ```text
            O Codeforces coleta dados pessoais dos usuários para fornecer e melhorar seus serviços. Os dados pessoais podem ser fornecidos voluntariamente pelos usuários ou coletados automaticamente ao utilizar a plataforma. Aqui estão alguns tipos de dados pessoais que o Codeforces pode coletar:

            1. **Dados fornecidos pelo usuário**:
            - Informações de registro (como nome de usuário, e-mail, etc.).
            - Conteúdo gerado pelo usuário (como soluções de problemas, comentários, etc.).

            2. **Dados coletados automaticamente**:
            - **Cookies e dados de uso**: Para identificar usuários, lembrar preferências e fornecer os serviços solicitados.
            - **Logs de sistema**: Para operação e manutenção da plataforma, podem ser coletados arquivos que registram a interação com a aplicação.
            - **Dados de análise**: Para monitorar e analisar o tráfego da web e o comportamento do usuário, podendo ser compartilhados de forma agregada e anônima.

            3. **Dados de terceiros**:
            - Informações de plataformas externas, como redes sociais, caso o usuário interaja com elas através do Codeforces.

            O Codeforces utiliza esses dados para:
            - Fornecer e personalizar os serviços.
            - Monitorar e analisar o uso da plataforma.
            - Melhorar a experiência do usuário.
            - Cumprir obrigações legais, como responder a solicitações de autoridades públicas.

            Para mais detalhes sobre como o Codeforces coleta, usa e protege seus dados pessoais, recomendo que você consulte a **Política de Privacidade** oficial do Codeforces: [https://codeforces.com/privacy](https://codeforces.com/privacy).
            ```
        - Opinião: Há correspondências do privacy.md presentes, mas no Vector Store houve dois pares de duplicatas.

**A4 (2º Execução).** "Me mostra problemas de rating 1500."
Esperado: `Problemset` com `rating=1500`, sem `q`/`tags`.
Valida: filtro numérico isolado, sem ruído de outros parâmetros.
Realidade:
    - Fluxo: Trigger -> Garoto -> (Memória -> Modelo -> Problemset) x3 -> Memória -> Modelo -> Resposta
    - Problemset (x3):
        - Input: 
            - n8n: {"rating":1500,"limit":10}
            - Log do Servidor: `/api/problemset/problems?rating=1500&limit=10`
        - Output:
            - GET HTTP 200
            ```json
            {
            "total": 477,
            "page": 1,
            "limit": 10,
            "problems": [
                {
                "contestId": 1466,
                "index": "D",
                "name": "13th Labour of Heracles",
                "type": "PROGRAMMING",
                "points": 1000,
                "rating": 1500,
                "solvedCount": 15394,
                "tags": [
                    "data structures",
                    "greedy",
                    "sortings",
                    "trees"
                ]
                },
                {
                "contestId": 468,
                "index": "A",
                "name": "24 Game",
                "type": "PROGRAMMING",
                "points": 500,
                "rating": 1500,
                "solvedCount": 8637,
                "tags": [
                    "greedy",
                    "math",
                    "constructive algorithms"
                ]
                },
                {
                "contestId": 409,
                "index": "H",
                "name": "A + B Strikes Back",
                "type": "PROGRAMMING",
                "rating": 1500,
                "solvedCount": 9594,
                "tags": [
                    "brute force",
                    "implementation",
                    "dsu",
                    "constructive algorithms",
                    "*special"
                ]
                },
                {
                "contestId": 1166,
                "index": "C",
                "name": "A Tale of Two Lands",
                "type": "PROGRAMMING",
                "points": 1500,
                "rating": 1500,
                "solvedCount": 11267,
                "tags": [
                    "sortings",
                    "binary search",
                    "two pointers"
                ]
                },
                {
                "contestId": 1278,
                "index": "B",
                "name": "A and B",
                "type": "PROGRAMMING",
                "rating": 1500,
                "solvedCount": 14303,
                "tags": [
                    "greedy",
                    "math"
                ]
                },
                {
                "contestId": 1873,
                "index": "G",
                "name": "ABBC or BACB",
                "type": "PROGRAMMING",
                "rating": 1500,
                "solvedCount": 17355,
                "tags": [
                    "greedy",
                    "constructive algorithms"
                ]
                },
                {
                "contestId": 1516,
                "index": "B",
                "name": "AGAGA XOOORRR",
                "type": "PROGRAMMING",
                "points": 1000,
                "rating": 1500,
                "solvedCount": 26904,
                "tags": [
                    "dp",
                    "brute force",
                    "greedy",
                    "bitmasks"
                ]
                },
                {
                "contestId": 1379,
                "index": "A",
                "name": "Acacius and String",
                "type": "PROGRAMMING",
                "points": 500,
                "rating": 1500,
                "solvedCount": 12413,
                "tags": [
                    "brute force",
                    "implementation",
                    "strings"
                ]
                },
                {
                "contestId": 2026,
                "index": "C",
                "name": "Action Figures",
                "type": "PROGRAMMING",
                "rating": 1500,
                "solvedCount": 12984,
                "tags": [
                    "data structures",
                    "brute force",
                    "greedy",
                    "implementation",
                    "binary search",
                    "constructive algorithms"
                ]
                },
                {
                "contestId": 2027,
                "index": "C",
                "name": "Add Zeros",
                "type": "PROGRAMMING",
                "points": 1250,
                "rating": 1500,
                "solvedCount": 14239,
                "tags": [
                    "data structures",
                    "dp",
                    "brute force",
                    "greedy",
                    "dfs and similar",
                    "graphs"
                ]
                }
            ]
            }
            ```
        - Resposta:
            ```
            Aqui estão alguns problemas com rating 1500:

            1. 13th Labour of Heracles - Contest 1466, índice D
            2. 24 Game - Contest 468, índice A
            3. A + B Strikes Back - Contest 409, índice H
            4. A Tale of Two Lands - Contest 1166, índice C
            5. A and B - Contest 1278, índice B
            6. ABBC or BACB - Contest 1873, índice G
            7. AGAGA XOOORRR - Contest 1516, índice B
            8. Acacius and String - Contest 1379, índice A
            9. Action Figures - Contest 2026, índice C
            10. Add Zeros - Contest 2027, índice C

            Posso fornecer mais informações sobre algum problema específico, se desejar.
            ```
        - Opinião: Depois de migrar do fixo para um JSON dinâmico, a tool funciona, eu acho que talvez o agente pode falar
          o ID completo ao invés de separado.

**A5.** "O que é o problema 4A?"
Esperado: `Problem` com ID `4A` no path (não `Problemset` com `contest_id=4&index=A`).
Valida: agente escolhe a tool de item único, não a de busca, quando há ID exato.
Realidade: ** Respostas consistente, a forma de dizer varia, mas basta o usuário pedir detalhes. **
    - Resposta:
        ```text
            O problema 4A é chamado "Watermelon". Ele possui as seguintes características:

            - Contest ID: 4
            - Índice: A
            - Tipo: PROGRAMMING
            - Rating: 800
            - Tags: brute force, math
            - Número de soluções: 719240

            Você pode acessar o problema diretamente no link: https://codeforces.com/problemset/problem/4/A
        ```
    - Opinião: Respondeu bem, se tivesse acesso ao enunciado seria muito bom, mas está estável. Link funcional.

**A6 (2º Execução).** "Quais contests já aconteceram esse mês?"
Esperado: `Contests` com `phase=FINISHED`, período implícito ou textual do mês corrente.
Valida: única exceção documentada ao viés "futuro por padrão" — usuário pediu histórico explicitamente.
Realidade:
    - Fluxo: Trigger -> Garoto -> Mem. -> Modelo -> Contests -> Mem. -> Modelo -> Respostas
    - Events:
        - Input: `/api/contests/?pretty_datetime=true&timezone=America%2FSao_Paulo&phase=FINISHED&order_by=-id&limit=100&page=1`
        - Output:
            - HTTP 200
            ```json
            {
                "total": 2138,
                "page": 1,
                "limit": 100,
                "contests": [
                    {
                    "id": 2257,
                    "name": "Codeforces Round 1117 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 7200,
                    "duration": "2:00:00",
                    "startTimeSeconds": 1786977300,
                    "relativeTimeSeconds": 377198,
                    "startTime": "2026-08-17T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2256,
                    "name": "Codeforces Round 1116 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 9000,
                    "duration": "2:30:00",
                    "startTimeSeconds": 1786286100,
                    "relativeTimeSeconds": 1068398,
                    "startTime": "2026-08-09T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2255,
                    "name": "Codeforces Round 1116 (Div. 1)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 9000,
                    "duration": "2:30:00",
                    "startTimeSeconds": 1786286100,
                    "relativeTimeSeconds": 1068398,
                    "startTime": "2026-08-09T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2254,
                    "name": "Codeforces Round 1114 (Div. 3)",
                    "type": "ICPC",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 8100,
                    "duration": "2:15:00",
                    "startTimeSeconds": 1785854100,
                    "relativeTimeSeconds": 1500398,
                    "startTime": "2026-08-04T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2253,
                    "name": "Educational Codeforces Round 193 (Rated for Div. 2)",
                    "type": "ICPC",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 7200,
                    "duration": "2:00:00",
                    "startTimeSeconds": 1786113300,
                    "relativeTimeSeconds": 1241198,
                    "startTime": "2026-08-07T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2252,
                    "name": "Codeforces Round 1115 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 7200,
                    "duration": "2:00:00",
                    "startTimeSeconds": 1786026900,
                    "relativeTimeSeconds": 1327598,
                    "startTime": "2026-08-06T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2250,
                    "name": "Codeforces Round 1112 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 9000,
                    "duration": "2:30:00",
                    "startTimeSeconds": 1785076500,
                    "relativeTimeSeconds": 2277998,
                    "startTime": "2026-07-26T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2249,
                    "name": "Codeforces Round 1112 (Div. 1)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 9000,
                    "duration": "2:30:00",
                    "startTimeSeconds": 1785076500,
                    "relativeTimeSeconds": 2277998,
                    "startTime": "2026-07-26T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2248,
                    "name": "Codeforces Round 1113 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 9000,
                    "duration": "2:30:00",
                    "startTimeSeconds": 1785594900,
                    "relativeTimeSeconds": 1759598,
                    "startTime": "2026-08-01T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    {
                    "id": 2247,
                    "name": "Codeforces Round 1111 (Div. 2)",
                    "type": "CF",
                    "phase": "FINISHED",
                    "frozen": false,
                    "durationSeconds": 7200,
                    "duration": "2:00:00",
                    "startTimeSeconds": 1784385300,
                    "relativeTimeSeconds": 2969198,
                    "startTime": "2026-07-18T11:35:00-03:00",
                    "relativeTime": "2026-08-21T20:21:38-03:00",
                    "timeZone": "America/Sao_Paulo"
                    },
                    ...
                ]
            }
            ```
        - Resposta:
            ```
                Aqui estão os contests que já aconteceram esse mês:

                1. Codeforces Round 1117 (Div. 2) - 17 de agosto de 2026
                2. Codeforces Round 1116 (Div. 2) - 9 de agosto de 2026
                3. Codeforces Round 1116 (Div. 1) - 9 de agosto de 2026
                4. Codeforces Round 1114 (Div. 3) - 4 de agosto de 2026
                5. Educational Codeforces Round 193 (Rated for Div. 2) - 7 de agosto de 2026
                6. Codeforces Round 1115 (Div. 2) - 6 de agosto de 2026

                Todos os contests acima já terminaram.
            ```
        - Opnião: Em Agosto/2026, considerando dia 21/08/2026, tínhamos apenas 7 contests passadas, a ICPC da Huawei estava
          acontecendo, aqui ele foi um pouco impreciso pois esqueceu de mencionar a do dia 1. Talvez não seja culpa do agente,
          e sim do backend, talvez possamos adicionar filtros de início e fim e ordenação por início.

**A7 (2º Execução).** "Detalhes da contest 2257."
Esperado: `Contest` (singular) com `contestId=2257`.
Valida: agente não usa `Contests` (lista) para um ID específico já conhecido.
Realidade: 
    - Fluxo: Trigger -> Mem + Modelo -> Contest -> Mem + Modelo -> Resposta (Envio corrigido)
    - Contest:
        - Input: `http://backend:8000/api/contests/2257`
        - Output:
            ```json
            {
                "id": 2257,
                "name": "Codeforces Round 1117 (Div. 2)",
                "type": "CF",
                "phase": "FINISHED",
                "frozen": false,
                "durationSeconds": 7200,
                "duration": "2:00:00",
                "startTimeSeconds": 1786977300,
                "relativeTimeSeconds": 422137,
                "startTime": "2026-08-17T11:35:00-03:00",
                "relativeTime": "2026-08-22T08:50:37-03:00",
                "timeZone": "America/Sao_Paulo"
            }
            ```
        - Resposta:
            ```text
                Aqui estão os detalhes da contest 2257:

                - **Nome**: Codeforces Round 1117 (Div. 2)
                - **Tipo**: Codeforces
                - **Fase**: Terminado
                - **Duração**: 2 horas
                - **Data e Hora de Início**: 17 de agosto de 2026, 11:35 (Horário de Brasília)
                - **Fuso Horário**: America/Sao_Paulo
            ```
        - Opinião: Bug do Telegram corrigido, e o agente naturalizou bem os termos. Acho que o problema agora é estético,
          o qual o modelo tem afinidade com Markdown, porém, a API do Telegram possui uns bugs... note que a API oferece parser
          para HTML, talvez como recurso futuro é normalizar para HTML, assim como fizemos nos documentos.

**A8.** "Quais calendários existem e qual o fuso horário deles?"
Esperado: `Calendar` (metadados) com `calendarId=all`.
Valida: não confunde com `Events` (que busca itens, não metadado do calendário em si).
Realidade: ** Corrigido o bug do id, respondendo bem **
    - Resposta:
        ```text
        Existem dois calendários principais relacionados ao Codeforces:

        1. Programming Contests Calendar
        - Fuso Horário: Europe/Moscow

        2. Misc Codeforces Calendar
        - Fuso Horário: Europe/Moscow

        Ambos os calendários estão no mesmo fuso horário, que é o de Moscou, Rússia (UTC+3). Se precisar de mais detalhes sobre eventos específicos, é só avisar!
        ```
    - Opinião: Talvez um pequeno ajuste no campo id para reflitir primary e misc quando for all.