# Resultado da Primeira Rodada de Calibração do GPC (A-1)

---

### A. Escopo correto — uma tool, sem ambiguidade (8)

**A1.** "A API do Codeforces está no ar?"
Esperado: `CF System Status`, sem parâmetros.
Valida: disparo básico, sem confundir com `Calendar`/`Contests`.
Realidade:
    - Fluxo: Trigger -> Garoto -> Memória -> Modelo -> CF System Status -> Memória -> Modelo -> Resposta
    - CF System Status:
        - Input: `{}`
        - URL: `https://codeforces.com/api/system.status`
        - Output:
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
                    "value": "591",
                    "type": "OK"
                },
                {
                    "name": "Recently judged submissions (last 5 minutes)",
                    "value": "617",
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
        ```text
        Sim, a API do Codeforces está funcionando normalmente no momento.
        ```
    - Opnião: Foi direto, sem mais detalhes vindos da API do Codeforces.

**A2.** "O que são os Termos de Uso do Codeforces?"
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
                    "text": "{"pageContent":"y\npolicy or by dedicated explanation text contextually with the Data collection.\nThe Personal Data may be freely provided by the User, or collected automatically\nwhen using this Application. Any use of Cookies - or of other tracking tools -\nby this Application or by the owners of third party services used by this\nApplication, unless stated otherwise, serves to identify Users and remember\ntheir preferences, for the sole purpose of providing the service required by the\nUser. Failure to provide certain Personal Data may make it impossible for this\nApplication to provide its services.\n\nUsers are responsible for any Personal Data of third parties obtained, published\nor shared through this Applica","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":18,"to":29}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{"pageContent":"to any person or business entity;\n* using this Website to engage in any advertising or marketing;\n\n### Your Content.\n\nIn these Website Terms And Conditions, “Your Content” shall mean any audio, video, text, images or\nother material you choose to display on this Website. With respect to Your Content, by displaying\nit, you grant Codeforces a non-exclusive, worldwide, irrevocable, royalty-free, sublicensable\nlicense to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your\nContent must be your own and must not be infringing on any third party’s rights. Codeforces reserves\nthe right to remove any of Your Content from this Website at any time, and for any reason,","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":25,"to":35}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{"pageContent":"e provisions of these Terms.\n\n### Severability.\n\nIf any provision of these Terms is found to be unenforceable or invalid under any applicable law,\nsuch unenforceability or invalidity shall not render these Terms unenforceable or invalid as a\nwhole, and such provisions shall be deleted without affecting the remaining provisions herein.\n\n### Variation of Terms.\n\nCodeforces is permitted to revise these Terms at any time as it sees fit, and by using this Website\nyou are expected to review such Terms on a regular basis to ensure you understand all terms and\nconditions governing use of this Website.\n\n### Assignment.\n\nCodeforces shall be permitted to assign, transfer, and subcontract its rights and","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":57,"to":73}}}}"
                    },
                    {
                    "type": "text",
                    "text": "{"pageContent":"fic rules ("Rules") for a Contest on the Contest\nwebsite, which become part of these Terms and your agreement with us with respect to the Contest.\n\n### Restrictions.\n\nYou are expressly and emphatically restricted from all of the following:\n\n* selling, sublicensing and/or otherwise commercializing any Website material;\n* using this Website in any way that is, or may be, damaging to this Website;\n* using this Website in any way that impacts user access to this Website;\n* using this Website contrary to applicable laws and regulations, or in a way that causes, or may cause, harm to the Website, or to any person or business entity;\n* using this Website to engage in any advertising or marketing;","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":15,"to":26}}}}"
                    }
                ]
                }
            ```
        - Resposta:
            ```text
            Os Termos de Uso do Codeforces são as regras e condições que os usuários devem seguir ao utilizar a plataforma. Eles cobrem aspectos como:

            1. Uso de Conteúdo: O usuário concede ao Codeforces uma licença para usar, reproduzir e distribuir qualquer conteúdo que publique na plataforma.
            2. Restrições: Proibição de comercializar materiais do site, causar danos ao site ou violar leis aplicáveis.
            3. Variação dos Termos: O Codeforces pode revisar os termos a qualquer momento, e os usuários devem revisá-los regularmente.

            Recomendo conferir a versão oficial dos Termos e Condições para detalhes completos.
            ```
        - Opinião: Há correspondências do terms.md presentes

**A3.** "Quais dados pessoais o Codeforces coleta?"
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
                    "text": "{"pageContent":"y\npolicy or by dedicated explanation text contextually with the Data collection.\nThe Personal Data may be freely provided by the User, or collected automatically\nwhen using this Application. Any use of Cookies - or of other tracking tools -\nby this Application or by the owners of third party services used by this\nApplication, unless stated otherwise, serves to identify Users and remember\ntheir preferences, for the sole purpose of providing the service required by the\nUser. Failure to provide certain Personal Data may make it impossible for this\nApplication to provide its services.\n\nUsers are responsible for any Personal Data of third parties obtained, published\nor shared through this Applica","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":18,"to":29}}}}"
                },
                {
                    "type": "text",
                    "text": "{"pageContent":"legal action arising from improper\nuse of this Application or the related services. The User declares to be aware\nthat the Data Controller may be required to reveal personal data upon request of\npublic authorities.\n\n### Additional information about User's Personal Data\n\nIn addition to the information contained in this privacy policy, this\nApplication may provide the User with additional and contextual information\nconcerning particular services or the collection and processing of Personal Data\nupon request.\n\n### System logs and maintenance\n\nFor operation and maintenance purposes, this Application and any third party\nservices may collect files that record interaction with this Application (Sy","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":211,"to":226}}}}"
                },
                {
                    "type": "text",
                    "text": "{"pageContent":"content\nfrom external platforms, Registration and authentication, Interaction with\nexternal social networks and platforms, Geolocation, Managing contacts and\nsending messages, Infrastructure monitoring and Hosting and backend\ninfrastructure.\n\nThe Personal Data used for each purpose is outlined in the specific sections of\nthis document.\n\n## Detailed information on the processing of Personal Data\n\nPersonal Data is collected for the following purposes and using the following\nservices:\n\n### Analytics\n\nThe services contained in this section enable the Owner to monitor and analyze\nweb traffic and can be used to keep track of User behavior. At times we may\nshare this information in aggregated anony","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":64,"to":82}}}}"
                },
                {
                    "type": "text",
                    "text": "{"pageContent":"n be used to keep track of User behavior. At times we may\nshare this information in aggregated anonymous form with third parties.\n\n#### Google Analytics (Google Inc.)\n\nGoogle Analytics is a web analysis service provided by Google Inc. (“Google”).\nGoogle utilizes the Data collected to track and examine the use of this\nApplication, to prepare reports on its activities and share them with other\nGoogle services. Google may use the Data collected to contextualize and\npersonalize the ads of its own advertising network.\n\nPersonal Data collected: Cookies and Usage data.\n\nPlace of processing: US –  [Privacy\nPolicy](https://www.google.com/intl/en/policies/privacy/)  –  [Opt\nOut](https://tools.google.c","metadata":{"source":"blob","blobType":"application/json","loc":{"lines":{"from":81,"to":96}}}}"
                }
                ]
            }
            ```
        - Resposta:
            ```text
            O Codeforces coleta dados pessoais que podem ser fornecidos pelo usuário ou coletados automaticamente ao usar a plataforma. Isso inclui:

            1. Dados fornecidos pelo usuário: Informações que você fornece voluntariamente, como ao se registrar ou usar certos serviços.
            2. Dados coletados automaticamente: Como cookies e dados de uso, para identificar usuários e lembrar preferências.
            3. Logs do sistema: Para operação e manutenção, podem ser coletados registros de interação com a plataforma.

            Recomendo verificar a Política de Privacidade oficial para detalhes completos.
            ```
        - Opinião: Há correspondências do privacy.md presentes, mas está algo vago.

**A4.** "Me mostra problemas de rating 1500."
Esperado: `Problemset` com `rating=1500`, sem `q`/`tags`.
Valida: filtro numérico isolado, sem ruído de outros parâmetros.
Realidade:
    - Fluxo: Trigger -> Garoto -> (Memória -> Modelo -> Problemset) x3 -> Memória -> Modelo -> Resposta
    - Problemset (x3):
        - Input: 
            - n8n:
                ```json
                {
                    "q": "",
                    "contest_id": 0,
                    "index": "",
                    "rating": 1500,
                    "min_points": 0,
                    "tags": "",
                    "order_by": "",
                    "limit": 10,
                    "page": 1
                }
                ```
            - Log do Servidor: `/api/problemset/problems?q=&contest_id=0&index=&rating=1500&min_points=0&tags=&order_by=&limit=10&page=1`
        - Output:
            - GET HTTP 422
            ```json
            {"detail":[{"type":"string_pattern_mismatch","loc":["query","index"],"msg":"String should match pattern '^[A-Z][0-9]?$'","input":"","ctx":{"pattern":"^[A-Z][0-9]?$"}},{"type":"string_type","loc":["query","order_by"],"msg":"Input should be a valid string","input":["name"]}]}
            ```
        - Resposta:
            ```
            Infelizmente, não consegui obter os problemas de rating 1500 devido a um erro no serviço. Peço desculpas pelo inconveniente. Posso tentar novamente mais tarde ou ajudar com outra dúvida?
            ```
        - Opinião: Ele tentou três vezes mas não conseguiu devido a um problema técnico que é o pattern exigido por index.
          Mas acredito que o agente deveria usar os parâmetros que são realmente necessários, ao invés de definir tudo.

**A5.** "O que é o problema 4A?"
Esperado: `Problem` com ID `4A` no path (não `Problemset` com `contest_id=4&index=A`).
Valida: agente escolhe a tool de item único, não a de busca, quando há ID exato.
Realidade:
    - Fluxo: Trigger -> Garoto -> Mem. -> Modelo -> Problem -> Mem. -> Modelo -> Resposta
    - Problem:
        - Input: http://backend:8000/api/problemset/problems/4A
        - Output:
            - GET HTTP 200
            ```json
                {
                    "contestId": 4,
                    "index": "A",
                    "name": "Watermelon",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "solvedCount": 719240,
                    "tags": [
                        "brute force",
                        "math"
                    ]
                }
            ```
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

**A6.** "Quais contests já aconteceram esse mês?"
Esperado: `Contests` com `phase=FINISHED`, período implícito ou textual do mês corrente.
Valida: única exceção documentada ao viés "futuro por padrão" — usuário pediu histórico explicitamente.
Realidade:
    - Fluxo: Trigger -> Garoto -> Mem. -> Modelo -> Events -> Mem. -> Modelo -> Respostas
    - Events:
        - Input: http://backend:8000/api/calendar/primary/events?q=&start=2026-08-01T00%3A00%3A00Z&end=2026-08-20T23%3A59%3A59Z&order_by=startTime&limit=100&timezone=America%2FSao_Paulo&page=1
        - Output:
            - HTTP 200
            ```json
                {
                    "total": 8,
                    "page": 1,
                    "limit": 100,
                    "has_more": false,
                    "events": [
                        {
                        "id": "3tvem186sbchnlib9ped6dc688",
                        "summary": "CF R 1113 (Div. 2)",
                        "link": "https://www.google.com/calendar/event?eid=M3R2ZW0xODZzYmNobmxpYjlwZWQ2ZGM2ODggazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2248\"\u003ECodeforces Round 1113 (Div. 2)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-07-28T10:54:07.222000+00:00",
                        "start": "2026-08-01 11:35:00 -03:00",
                        "end": "2026-08-01 14:05:00 -03:00"
                        },
                        {
                        "id": "qvjvuumbs0335naokutdqnv328",
                        "summary": "CF R 1114 (Div. 3)",
                        "link": "https://www.google.com/calendar/event?eid=cXZqdnV1bWJzMDMzNW5hb2t1dGRxbnYzMjggazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2254\"\u003ECodeforces Round 1114 (Div. 3)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-08-02T17:07:31.481000+00:00",
                        "start": "2026-08-04 11:35:00 -03:00",
                        "end": "2026-08-04 13:50:00 -03:00"
                        },
                        {
                        "id": "8135na5j30c61h6h2e11qm9nds",
                        "summary": "CF R 1115 (Div. 2)",
                        "link": "https://www.google.com/calendar/event?eid=ODEzNW5hNWozMGM2MWg2aDJlMTFxbTluZHMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2252\"\u003ECodeforces Round 1115 (Div. 2)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-08-04T18:40:18.686000+00:00",
                        "start": "2026-08-06 11:35:00 -03:00",
                        "end": "2026-08-06 13:35:00 -03:00"
                        },
                        {
                        "id": "ha2ni4u79252ajqclrc7mqhlv4",
                        "summary": "Educational CF R 193 (Rated for Div. 2)",
                        "link": "https://www.google.com/calendar/event?eid=aGEybmk0dTc5MjUyYWpxY2xyYzdtcWhsdjQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2253\"\u003EEducational Codeforces Round 193 (Rated for Div. 2)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-07-27T20:48:22.460000+00:00",
                        "start": "2026-08-07 11:35:00 -03:00",
                        "end": "2026-08-07 13:35:00 -03:00"
                        },
                        {
                        "id": "5il2354gth9hrh4jl7p1nqld4c",
                        "summary": "CF R 1116",
                        "link": "https://www.google.com/calendar/event?eid=NWlsMjM1NGd0aDlocmg0amw3cDFucWxkNGMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2255\"\u003ECodeforces Round 1116 (Div. 1)\u003C/a\u003E\n\u003Ca href=\"https://codeforces.com/contests/2256\"\u003ECodeforces Round 1116 (Div. 2)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-08-04T09:34:32.154000+00:00",
                        "start": "2026-08-09 11:35:00 -03:00",
                        "end": "2026-08-09 14:05:00 -03:00"
                        },
                        {
                        "id": "doc6uo8bv3efk83c89itrfe1as",
                        "summary": "CF R 1116 (Div. 1)",
                        "link": "https://www.google.com/calendar/event?eid=ZG9jNnVvOGJ2M2VmazgzYzg5aXRyZmUxYXMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2255\"\u003ECodeforces Round 1116 (Div. 1)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-08-04T09:34:28.985000+00:00",
                        "start": "2026-08-09 11:35:00 -03:00",
                        "end": "2026-08-09 14:05:00 -03:00"
                        },
                        {
                        "id": "ej31i0eip5lphb1ftuq2repua4",
                        "summary": "ICPC 2026 Online Challenge 1 powered by Huawei",
                        "link": "https://www.google.com/calendar/event?eid=ZWozMWkwZWlwNWxwaGIxZnR1cTJyZXB1YTQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2251\"\u003EICPC 2026 Online Challenge 1 powered by Huawei\u003C/a\u003E\n\nUnrated\n\nAdded automatically",
                        "updated": "2026-08-03T18:04:43.115000+00:00",
                        "start": "2026-08-14 08:00:00 -03:00",
                        "end": "2026-08-28 08:00:00 -03:00"
                        },
                        {
                        "id": "td9h0sg7p10tacc06ont31urlo",
                        "summary": "CF R 1117 (Div. 2)",
                        "link": "https://www.google.com/calendar/event?eid=dGQ5aDBzZzdwMTB0YWNjMDZvbnQzMXVybG8gazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
                        "description": "\u003Ca href=\"https://codeforces.com/contests/2257\"\u003ECodeforces Round 1117 (Div. 2)\u003C/a\u003E\n\nRated\n\nAdded automatically",
                        "updated": "2026-08-15T19:16:51.113000+00:00",
                        "start": "2026-08-17 11:35:00 -03:00",
                        "end": "2026-08-17 13:35:00 -03:00"
                        }
                    ]
                }
            ```
        - Resposta:
            ```
                Aqui estão os contests que já aconteceram este mês:

                1. Codeforces Round 1113 (Div. 2)
                - Data: 01/08/2026
                - Horário: 11:35 - 14:05 (Fuso horário: -03:00)

                2. Codeforces Round 1114 (Div. 3)
                - Data: 04/08/2026
                - Horário: 11:35 - 13:50 (Fuso horário: -03:00)

                3. Codeforces Round 1115 (Div. 2)
                - Data: 06/08/2026
                - Horário: 11:35 - 13:35 (Fuso horário: -03:00)

                4. Educational Codeforces Round 193 (Rated for Div. 2)
                - Data: 07/08/2026
                - Horário: 11:35 - 13:35 (Fuso horário: -03:00)

                5. Codeforces Round 1116 (Div. 1 e Div. 2)
                - Data: 09/08/2026
                - Horário: 11:35 - 14:05 (Fuso horário: -03:00)

                6. ICPC 2026 Online Challenge 1 powered by Huawei
                - Data: 14/08/2026 - 28/08/2026
                - Horário: 08:00 - 08:00 (Fuso horário: -03:00)

                7. Codeforces Round 1117 (Div. 2)
                - Data: 17/08/2026
                - Horário: 11:35 - 13:35 (Fuso horário: -03:00)

                Esses são todos os contests que ocorreram até o momento neste mês.
            ```
        - Opnião: Aqui houve uma imprecisão, pois o agente não usou Contests e considerou que a ICPC da Huawei ocorreu no sentido
          de que já terminou, mas é até dia 28. Precisa ajustar.

**A7.** "Detalhes da contest 2257."
Esperado: `Contest` (singular) com `contestId=2257`.
Valida: agente não usa `Contests` (lista) para um ID específico já conhecido.
Realidade: 
    - **BUG** no envio usando API do Telegram: `{ "ok": false, "error_code": 400, "description": "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 285" }`
    - Fluxo: Trigger -> Mem + Modelo -> Contest -> Mem + Modelo -> Resposta (Envio bugado)
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
                    "relativeTimeSeconds": 350067,
                    "startTime": "2026-08-17T11:35:00-03:00",
                    "relativeTime": "2026-08-21T12:49:27-03:00",
                    "timeZone": "America/Sao_Paulo"
                }
            ```
        - Resposta (recuperado dos logs):
            ```text
                Aqui estão os detalhes da **Codeforces Round 1117 (Div. 2)** (Contest ID: 2257):
                
                - **Nome**: Codeforces Round 1117 (Div. 2)
                - **Tipo**: CF
                - **Fase**: FINISHED
                - **Duração**: 2 horas (7200 segundos)
                - **Data e Horário de Início**: 17/08/2026 às 11:35 (Fuso horário: America/Sao_Paulo, UTC-3)
                
                Essa contest já foi concluída. Se precisar de mais informações, é só perguntar!	
            ```
        - Opinião: Respondeu bem, dentro do n8n, pois o BadRequest impediu que aparecesse no chat do Telegram.
          Talvez ao invés do modelo chamar de CF ou FINISHED, pudesse falar com uma linguagem natural como Codeforces
          e Terminado.

**A8.** "Quais calendários existem e qual o fuso horário deles?"
Esperado: `Calendar` (metadados) com `calendarId=all`.
Valida: não confunde com `Events` (que busca itens, não metadado do calendário em si).
Realidade:
    - Fluxo: Trigger -> Mem. + Modelo -> Calendar -> Mem. + Modelo -> Resposta
    - Calendar:
        - Input: `http://backend:8000/api/calendar/all`
        - Output:
            ```json
            [
                {
                    "id": "all",
                    "gid": "k23j233gtcvau7a8ulk2p360m4@group.calendar.google.com",
                    "name": "Programming Contests Calendar",
                    "timezone": "Europe/Moscow"
                },
                {
                    "id": "all",
                    "gid": "efcajlnqvdqjeoud2spsiphnqk@group.calendar.google.com",
                    "name": "Misc Codeforces Calendar",
                    "timezone": "Europe/Moscow"
                }
            ]
            ```
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