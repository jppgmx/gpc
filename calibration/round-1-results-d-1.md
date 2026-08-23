# Resultado da Primeira Rodada de Calibração do GPC (D-1)

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

## Avisos:
- Irei omitir dessa vez o fluxo interno para aqueles que satisfazerem cada cenário

---

### D. Multi-turno com memória (4)

**D1.**
Turno 1: "O que tem para esse mês?"
Turno 2: "E algum da Huawei?"
Esperado: turno 2 reaproveita contexto (mês já estabelecido) mas ajusta para busca textual — sem repetir pergunta ao usuário.
Valida: já testado antes com sucesso — vira teste de regressão.
Realidade:
- Turno 1
    - Fluxo: TSN -> Garoto -> MM -> Events -> MM -> Resposta
    - Events:
        - Input: {"start":"2026-08-01T00:00:00Z","end":"2026-08-31T23:59:59Z","order_by":"startTime","timezone":"America/Sao_Paulo","limit":100,"page":1}
    - Resposta:
    ```md
    Aqui estão os eventos agendados para agosto de 2026 no Codeforces:

    1. **Codeforces Round 1113 (Div. 2)**
    - Data: 01/08/2026
    - Horário: 11:35 - 14:05 BRT
    - Rated

    2. **Codeforces Round 1114 (Div. 3)**
    - Data: 04/08/2026
    - Horário: 11:35 - 13:50 BRT
    - Rated

    3. **Codeforces Round 1115 (Div. 2)**
    - Data: 06/08/2026
    - Horário: 11:35 - 13:35 BRT
    - Rated

    4. **Educational Codeforces Round 193 (Rated for Div. 2)**
    - Data: 07/08/2026
    - Horário: 11:35 - 13:35 BRT
    - Rated

    5. **Codeforces Round 1116 (Div. 1 e Div. 2)**
    - Data: 09/08/2026
    - Horário: 11:35 - 14:05 BRT
    - Rated

    6. **ICPC 2026 Online Challenge 1 powered by Huawei**
    - Data: 14/08/2026 a 28/08/2026
    - Horário: 08:00 BRT
    - Unrated

    7. **Codeforces Round 1117 (Div. 2)**
    - Data: 17/08/2026
    - Horário: 11:35 - 13:35 BRT
    - Rated

    8. **Codeforces Round (Div. 2)**
    - Data: 29/08/2026
    - Horário: 11:35 - 13:35 BRT
    - Rated

    Esses são todos os eventos agendados para este mês.
    ```
    - Opinião: Respondeu bem, inclusive consegue afirmar sobre ser rated ou não.
- Turno 2
    - Fluxo: TSN -> Garoto -> MM -> Events -> MM -> Resposta
    - Events:
        - Input: `{"q":"Huawei","order_by":"startTime","timezone":"America/Sao_Paulo","limit":100,"page":1}`
        - Retorna:
        ```json
        {
        "total": 12,
        "page": 1,
        "limit": 100,
        "has_more": false,
        "events": [
            {
            "id": "s96oc49d2mt8t77ual43f3r76c",
            "summary": "Huawei Honorcup Marathon 1",
            "link": "https://www.google.com/calendar/event?eid=czk2b2M0OWQybXQ4dDc3dWFsNDNmM3I3NmMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
            "description": "<a href=\"https://codeforces.com/contests/1052\">Huawei Honorcup Marathon 1</a>\n\nUnrated\n\nAdded automatically",
            "updated": "2018-09-20T13:31:45.580000+00:00",
            "start": "2018-09-20 14:00:00 -03:00",
            "end": "2018-10-04 14:00:00 -03:00"
            },
            {
            "id": "fdqs7jspphfnt6r8m60mopvl4s",
            "summary": "Huawei Honorcup Marathon 2",
            "link": "https://www.google.com/calendar/event?eid=ZmRxczdqc3BwaGZudDZyOG02MG1vcHZsNHMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
            "description": "<a href=\"https://codeforces.com/contests/1235\">Huawei Honorcup Marathon 2</a>\n\nUnrated\n\nAdded automatically",
            "updated": "2019-09-24T09:16:24.250000+00:00",
            "start": "2019-09-30 15:00:00 -03:00",
            "end": "2019-10-14 15:00:00 -03:00"
            },
            ...,
            {
            "id": "img4f5n27fi6kt38qloeinsk80",
            "summary": "2024 ICPC World Finals Challenge powered by Huawei",
            "link": "https://www.google.com/calendar/event?eid=aW1nNGY1bjI3Zmk2a3QzOHFsb2VpbnNrODAgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
            "description": "<a href=\"https://codeforces.com/contests/2015\">2024 ICPC World Finals Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
            "updated": "2025-08-07T10:52:35.863000+00:00",
            "start": "2024-09-17 03:34:00 -03:00",
            "end": "2024-09-17 06:34:00 -03:00"
            },
            {
            "id": "47dpoc6cch6duj7uu0l5vv35ng",
            "summary": "ICPC 2025 Online Winter Challenge powered by Huawei",
            "link": "https://www.google.com/calendar/event?eid=NDdkcG9jNmNjaDZkdWo3dXUwbDV2djM1bmcgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
            "description": "<a href=\"https://codeforces.com/contests/2177\">ICPC 2025 Online Winter Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
            "updated": "2025-12-08T18:54:36.518000+00:00",
            "start": "2025-12-26 08:00:00 -03:00",
            "end": "2026-01-11 08:00:00 -03:00"
            },
            {
            "id": "ej31i0eip5lphb1ftuq2repua4",
            "summary": "ICPC 2026 Online Challenge 1 powered by Huawei",
            "link": "https://www.google.com/calendar/event?eid=ZWozMWkwZWlwNWxwaGIxZnR1cTJyZXB1YTQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
            "description": "<a href=\"https://codeforces.com/contests/2251\">ICPC 2026 Online Challenge 1 powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
            "updated": "2026-08-03T18:04:43.115000+00:00",
            "start": "2026-08-14 08:00:00 -03:00",
            "end": "2026-08-28 08:00:00 -03:00"
            }
        ]
        }
        ```
    - Resposta:
    ```
    O próximo evento da Huawei no Codeforces é o **ICPC 2026 Online Challenge 1 powered by Huawei**, 
    que ocorrerá de 14 a 28 de agosto de 2026, das 08:00 BRT. Este evento é Unrated.
    ```
    - Opinião: Também respondeu bem, mas ele falou "que ocorrerá", se hoje é 23/08/2026, poderia dizer que está acontecendo agora.
     Ajustar o nodo Normalize e o system_message.md
- Opinião Geral: Respondeu bem, apenas essa imprecisão sobre o que ocorre, vai ocorrer e já ocorreu.

**D2.**
Turno 1: "Quais tags existem relacionadas a grafos?"
Turno 2: "Me mostra problemas fáceis com essa tag."
Esperado: turno 2 usa a tag exata identificada no turno 1 (via `Tags`), não uma nova tentativa de adivinhar.
Valida: memória carregando resultado de tool anterior, não só texto da conversa.
Realidade:
- Turno 1
    - Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Resposta
    - Resposta:
    ```
    Aqui estão as tags relacionadas a grafos no Codeforces:

    1. **dfs and similar** — Busca em Profundidade (DFS) e algoritmos de travessia relacionados em grafos ou árvores.
    2. **graphs** — Problemas envolvendo grafos (representação, componentes conexas, travessias).
    3. **trees** — Árvores, grafos conexos e acíclicos (diâmetro, ancestral comum mais baixo/LCA).
    4. **shortest paths** — Algoritmos de caminhos mais curtos em grafos (Dijkstra, Bellman-Ford, Floyd-Warshall).
    5. **graph matchings** — Emparelhamento em grafos (Bipartite Matching, Algoritmo de Hopcroft-Karp).
    6. **flows** — Fluxos em Redes (Network Flows, Max Flow, Min Cut, Min Cost Max Flow).
    7. **2-sat** — Problema de Satisfatibilidade Booleana em 2-CNF (2-SAT), frequentemente resolvido com grafos de implicação.
    ```
    - Opinião: Respondeu bem, cobriu várias tags
- Turno 2
    - Fluxo: TSN -> Garoto -> MM -> Problemset -> MM -> Resposta
    - Problemset:
        - Input: `{"rating":1200,"tags":"graphs","order_by":"-solvedCount","limit":5,"page":1}`
        - Retorno:
        ```json
        {
        "total": 11,
        "page": 1,
        "limit": 5,
        "problems": [
            {
            "contestId": 217,
            "index": "A",
            "name": "Ice Skating",
            "type": "PROGRAMMING",
            "points": 500,
            "rating": 1200,
            "solvedCount": 25464,
            "tags": [
                "brute force",
                "dfs and similar",
                "dsu",
                "graphs"
            ]
            },
            {
            "contestId": 1559,
            "index": "C",
            "name": "Mocha and Hiking",
            "type": "PROGRAMMING",
            "points": 1000,
            "rating": 1200,
            "solvedCount": 23272,
            "tags": [
                "constructive algorithms",
                "graphs"
            ]
            },
            {
            "contestId": 1327,
            "index": "B",
            "name": "Princesses and Princes",
            "type": "PROGRAMMING",
            "rating": 1200,
            "solvedCount": 19745,
            "tags": [
                "brute force",
                "greedy",
                "graphs"
            ]
            },
            {
            "contestId": 522,
            "index": "A",
            "name": "Reposts",
            "type": "PROGRAMMING",
            "points": 500,
            "rating": 1200,
            "solvedCount": 19425,
            "tags": [
                "dp",
                "dfs and similar",
                "graphs",
                "trees",
                "*special"
            ]
            },
            {
            "contestId": 1647,
            "index": "B",
            "name": "Madoka and the Elegant Gift",
            "type": "PROGRAMMING",
            "points": 1250,
            "rating": 1200,
            "solvedCount": 17251,
            "tags": [
                "brute force",
                "implementation",
                "constructive algorithms",
                "graphs"
            ]
            }
        ]
        }
        ```
    - Resposta:
    ```
    Aqui estão alguns problemas fáceis com a tag "graphs" no Codeforces:

    1. Ice Skating (217A) — Rating 1200, 25.5k resoluções
    2. Mocha and Hiking (1559C) — Rating 1200, 23.3k resoluções
    3. Princesses and Princes (1327B) — Rating 1200, 19.7k resoluções
    4. Reposts (522A) — Rating 1200, 19.4k resoluções
    5. Madoka and the Elegant Gift (1647B) — Rating 1200, 17.3k resoluções
    ```
    - Opinião: O rating 1200 é considerado dificuldade alta, existe uma associação de ratings onde o menor (800) é considerado
     as fáceis e a maior bem complexas.
- Opinião Geral: Ele obteu as tags e problemas bem, e ordenou com base na quantidade de resoluções, apenas esse ajuste da dificuldade.

**D3.**
Turno 1: "Status do sistema do Codeforces."
Turno 2: "E tá funcionando bem mesmo?"
Esperado: turno 2 **não** dispara `CF System Status` de novo (dado já está na memória recente, resposta já foi dada) — a menos que o agente julgue que o dado pode ter mudado.
Valida: evitar chamada redundante de tool quando a resposta já está disponível no contexto imediato.
Realidade:
- Turno 1
    - Fluxo: TSN -> Garoto -> MM -> CF System Status -> MM -> Resposta
        - CFSS:
            - Retorna:
            ```json
            {
            "status": "OK",
            "result": {
                "rows": [
                {
                    "name": "MQ messages received recently",
                    "value": "OK",
                    "type": "OK"
                },
                {
                    "name": "Recently submitted submissions (last 5 minutes)",
                    "value": "568",
                    "type": "OK"
                },
                {
                    "name": "Recently judged submissions (last 5 minutes)",
                    "value": "572",
                    "type": "OK"
                },
                {
                    "name": "Keeper ping",
                    "value": "OK",
                    "type": "OK"
                },
                {
                    "name": "Problem repository availability",
                    "value": "OK",
                    "type": "OK"
                }
                ]
            }
            }
            ```
    - Resposta:
    ```
    O sistema do Codeforces está operando normalmente no momento. Aqui estão alguns indicadores:

    - **Submissões recentes (últimos 5 minutos):** 568
    - **Submissões julgadas (últimos 5 minutos):** 572
    - **Status geral:** OK
    ```
    - Opinião: Respondeu correto, e com alguns indicadores.
- Turno 2
    - Fluxo: TSN -> Garoto -> MM -> Memória -> Resposta
    - Resposta:
    ```
    Sim, o sistema do Codeforces está funcionando bem, de acordo com os indicadores de status. 
    Não há sinais de problemas ou instabilidades no momento.
    ```
    - Opinião: Respondeu com base em sua memória, e está bom.
- Opinião Geral: Ele obteve e respondeu corretamente.

**D4.**
Turno 1: "Fala sobre a Política de Privacidade."
Turno 2: "E os Termos, tem alguma cláusula sobre isso também?"
Esperado: turno 2 dispara nova busca no Vector Store (agora sobre terms.md), sem confundir com o resultado do turno 1.
Valida: troca de fonte dentro do mesmo Vector Store entre turnos consecutivos.
Realidade:
- Turno 1
    - Fluxo: TSN -> Garoto -> MM -> Documents Vector Store -> MM -> Resposta
    - Resposta:
    ```
    A Política de Privacidade do Codeforces aborda como os dados pessoais dos usuários são coletados, usados e compartilhados. Aqui estão alguns pontos-chave:

    1. **Coleta de Dados:** Os dados pessoais podem ser fornecidos pelo usuário ou coletados automaticamente durante o uso da plataforma. Isso inclui o uso de cookies e outras ferramentas de rastreamento para identificar usuários e lembrar suas preferências.

    2. **Uso de Dados:** Os dados são usados para fornecer os serviços solicitados pelo usuário. A falha em fornecer certos dados pode impedir o funcionamento adequado da plataforma.

    3. **Compartilhamento de Dados:** Em alguns casos, informações agregadas e anônimas podem ser compartilhadas com terceiros. O Codeforces também utiliza serviços de terceiros, como o Google Analytics, que podem coletar e processar dados de uso.

    4. **Geolocalização:** A plataforma pode coletar, usar e compartilhar dados de localização do usuário para fornecer serviços baseados em localização, desde que o usuário tenha autorizado explicitamente.

    5. **Segurança:** O Codeforces pode ser obrigado a revelar dados pessoais mediante solicitação de autoridades públicas em casos de ações legais.

    6. **Informações Adicionais:** A plataforma pode fornecer informações contextuais adicionais sobre a coleta e processamento de dados pessoais mediante solicitação do usuário.

    **Recomendação:** Para detalhes completos e atualizados, consulte a [Política de Privacidade oficial do Codeforces](https://codeforces.com/privacy).
    ```
    - Opinião: Respondeu bem, com correspondências ao privacy.md, excelente contextualização.
- Turno 2
    - Fluxo: TSN -> Garoto -> MM -> DVS -> MM -> Resposta
    - DVS:
        - Input: Terms and Conditions
        - Retorna:
        ```json
        {
        "response": [
            {
            "type": "text",
            "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\\n\\n### Your Content.\\n\\nIn these Website Terms And Conditions, “Your Content” shall mean any audio, video, text, images or\\nother material you choose to display on this Website. With respect to Your Content, by displaying\\nit, you grant Codeforces a non-exclusive, worldwide, irrevocable, royalty-free, sublicensable\\nlicense to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your\\nContent must be your own and must not be infringing on any third party’s rights. Codeforces reserves\\nthe right to remove any of Your Content from this Website at any time, and for any reason,\",\"metadata\":{\"source\":\"terms\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":25,\"to\":35}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"e provisions of these Terms.\\n\\n### Severability.\\n\\nIf any provision of these Terms is found to be unenforceable or invalid under any applicable law,\\nsuch unenforceability or invalidity shall not render these Terms unenforceable or invalid as a\\nwhole, and such provisions shall be deleted without affecting the remaining provisions herein.\\n\\n### Variation of Terms.\\n\\nCodeforces is permitted to revise these Terms at any time as it sees fit, and by using this Website\\nyou are expected to review such Terms on a regular basis to ensure you understand all terms and\\nconditions governing use of this Website.\\n\\n### Assignment.\\n\\nCodeforces shall be permitted to assign, transfer, and subcontract its rights and\",\"metadata\":{\"source\":\"terms\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":57,\"to\":73}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"fic rules (\\\"Rules\\\") for a Contest on the Contest\\nwebsite, which become part of these Terms and your agreement with us with respect to the Contest.\\n\\n### Restrictions.\\n\\nYou are expressly and emphatically restricted from all of the following:\\n\\n* selling, sublicensing and/or otherwise commercializing any Website material;\\n* using this Website in any way that is, or may be, damaging to this Website;\\n* using this Website in any way that impacts user access to this Website;\\n* using this Website contrary to applicable laws and regulations, or in a way that causes, or may cause, harm to the Website, or to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\",\"metadata\":{\"source\":\"terms\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":15,\"to\":26}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"content\\nfrom external platforms, Registration and authentication, Interaction with\\nexternal social networks and platforms, Geolocation, Managing contacts and\\nsending messages, Infrastructure monitoring and Hosting and backend\\ninfrastructure.\\n\\nThe Personal Data used for each purpose is outlined in the specific sections of\\nthis document.\\n\\n## Detailed information on the processing of Personal Data\\n\\nPersonal Data is collected for the following purposes and using the following\\nservices:\\n\\n### Analytics\\n\\nThe services contained in this section enable the Owner to monitor and analyze\\nweb traffic and can be used to keep track of User behavior. At times we may\\nshare this information in aggregated anony\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":64,\"to\":82}}}}"
            }
        ]
        }
        ```
    - Resposta:
    ```
    Sim, os Termos e Condições do Codeforces também abordam questões relacionadas à privacidade e ao uso de dados. Aqui estão alguns pontos relevantes:

    1. **Seu Conteúdo:** Ao exibir qualquer material (áudio, vídeo, texto, imagens) na plataforma, você concede ao Codeforces uma licença não exclusiva, global, irrevogável e isenta de royalties para usar, reproduzir, adaptar, publicar, traduzir e distribuir esse conteúdo em qualquer mídia. O Codeforces reserva-se o direito de remover qualquer conteúdo a qualquer momento e por qualquer motivo.

    2. **Restrições:** Os usuários são proibidos de usar a plataforma para fins comerciais, como venda ou sublicenciamento de materiais, ou de maneira que possa danificar a plataforma, impactar o acesso de outros usuários ou violar leis e regulamentos.

    3. **Variação dos Termos:** O Codeforces pode revisar os Termos a qualquer momento, e os usuários são incentivados a revisá-los regularmente para garantir que compreendam todas as condições de uso da plataforma.

    4. **Atribuição:** O Codeforces pode atribuir, transferir ou subcontratar seus direitos e obrigações conforme necessário.

    **Recomendação:** Para detalhes completos e atualizados, consulte os [Termos e Condições oficiais do Codeforces](https://codeforces.com/terms).
    ```
    - Opinião: Ele também respondeu bem, ele pegou fragmentos do privacy.md, mas respondeu usando fragmentos do terms.md
- Opinião Geral: Em geral, o RAG está estável, Top K, que antes era 4 agora é 5, está bom. Está normal.