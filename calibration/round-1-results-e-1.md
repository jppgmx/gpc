# Resultado da Primeira Rodada de Calibração do GPC (E-1)

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

## Avisos:
- Irei omitir dessa vez o fluxo interno para aqueles que satisfazerem cada cenário

---
### E. Casos de regressão conhecidos (4)

**E1.** "Teve algum evento recente que eu perdi?" (sem nome específico)
Esperado: interpretação como "recente = passado próximo" é aceitável aqui (não há tensão com "futuro", já que não há evento futuro nomeado) — mas confirmar que não mistura com viés de "sempre futuro" de forma incorreta.
Valida: garante que a regra de "recente = futuro" não virou um viés cego aplicado sem contexto — aqui "perdi" sinaliza passado explicitamente.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Events -> MM -> Resposta
- Events:
    - Input: `{"start":"2026-07-24T15:20:38-03:00","end":"2026-08-23T15:20:38-03:00","order_by":"startTime","timezone":"America/Sao_Paulo","limit":100,"page":1}`
    - Retorna:
    ```json
    {
    "total": 9,
    "page": 1,
    "limit": 100,
    "has_more": false,
    "events": [
        {
        "id": "0ls2mbro30vj7gmh7e2rgpv17o",
        "summary": "CF R 1112",
        "link": "https://www.google.com/calendar/event?eid=MGxzMm1icm8zMHZqN2dtaDdlMnJncHYxN28gazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2249\">Codeforces Round 1112 (Div. 1)</a>\n<a href=\"https://codeforces.com/contests/2250\">Codeforces Round 1112 (Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-07-21T20:19:58.226000+00:00",
        "start": "2026-07-26 11:35:00 -03:00",
        "end": "2026-07-26 14:05:00 -03:00"
        },
        {
        "id": "3tvem186sbchnlib9ped6dc688",
        "summary": "CF R 1113 (Div. 2)",
        "link": "https://www.google.com/calendar/event?eid=M3R2ZW0xODZzYmNobmxpYjlwZWQ2ZGM2ODggazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2248\">Codeforces Round 1113 (Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-07-28T10:54:07.222000+00:00",
        "start": "2026-08-01 11:35:00 -03:00",
        "end": "2026-08-01 14:05:00 -03:00"
        },
        {
        "id": "qvjvuumbs0335naokutdqnv328",
        "summary": "CF R 1114 (Div. 3)",
        "link": "https://www.google.com/calendar/event?eid=cXZqdnV1bWJzMDMzNW5hb2t1dGRxbnYzMjggazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2254\">Codeforces Round 1114 (Div. 3)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-08-02T17:07:31.481000+00:00",
        "start": "2026-08-04 11:35:00 -03:00",
        "end": "2026-08-04 13:50:00 -03:00"
        },
        {
        "id": "8135na5j30c61h6h2e11qm9nds",
        "summary": "CF R 1115 (Div. 2)",
        "link": "https://www.google.com/calendar/event?eid=ODEzNW5hNWozMGM2MWg2aDJlMTFxbTluZHMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2252\">Codeforces Round 1115 (Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-08-04T18:40:18.686000+00:00",
        "start": "2026-08-06 11:35:00 -03:00",
        "end": "2026-08-06 13:35:00 -03:00"
        },
        {
        "id": "ha2ni4u79252ajqclrc7mqhlv4",
        "summary": "Educational CF R 193 (Rated for Div. 2)",
        "link": "https://www.google.com/calendar/event?eid=aGEybmk0dTc5MjUyYWpxY2xyYzdtcWhsdjQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2253\">Educational Codeforces Round 193 (Rated for Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-07-27T20:48:22.460000+00:00",
        "start": "2026-08-07 11:35:00 -03:00",
        "end": "2026-08-07 13:35:00 -03:00"
        },
        {
        "id": "5il2354gth9hrh4jl7p1nqld4c",
        "summary": "CF R 1116",
        "link": "https://www.google.com/calendar/event?eid=NWlsMjM1NGd0aDlocmg0amw3cDFucWxkNGMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2255\">Codeforces Round 1116 (Div. 1)</a>\n<a href=\"https://codeforces.com/contests/2256\">Codeforces Round 1116 (Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-08-04T09:34:32.154000+00:00",
        "start": "2026-08-09 11:35:00 -03:00",
        "end": "2026-08-09 14:05:00 -03:00"
        },
        {
        "id": "doc6uo8bv3efk83c89itrfe1as",
        "summary": "CF R 1116 (Div. 1)",
        "link": "https://www.google.com/calendar/event?eid=ZG9jNnVvOGJ2M2VmazgzYzg5aXRyZmUxYXMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2255\">Codeforces Round 1116 (Div. 1)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-08-04T09:34:28.985000+00:00",
        "start": "2026-08-09 11:35:00 -03:00",
        "end": "2026-08-09 14:05:00 -03:00"
        },
        {
        "id": "ej31i0eip5lphb1ftuq2repua4",
        "summary": "ICPC 2026 Online Challenge 1 powered by Huawei",
        "link": "https://www.google.com/calendar/event?eid=ZWozMWkwZWlwNWxwaGIxZnR1cTJyZXB1YTQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2251\">ICPC 2026 Online Challenge 1 powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2026-08-03T18:04:43.115000+00:00",
        "start": "2026-08-14 08:00:00 -03:00",
        "end": "2026-08-28 08:00:00 -03:00"
        },
        {
        "id": "td9h0sg7p10tacc06ont31urlo",
        "summary": "CF R 1117 (Div. 2)",
        "link": "https://www.google.com/calendar/event?eid=dGQ5aDBzZzdwMTB0YWNjMDZvbnQzMXVybG8gazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2257\">Codeforces Round 1117 (Div. 2)</a>\n\nRated\n\nAdded automatically",
        "updated": "2026-08-15T19:16:51.113000+00:00",
        "start": "2026-08-17 11:35:00 -03:00",
        "end": "2026-08-17 13:35:00 -03:00"
        }
    ]
    }
    ```
- Resposta:
```
Aqui estão os eventos recentes que você pode ter perdido:

1. **Codeforces Round 1112 (Div. 1 e Div. 2)**
   - Data: 26/07/2026
   - Horário: 11:35 - 14:05
   - Rated

2. **Codeforces Round 1113 (Div. 2)**
   - Data: 01/08/2026
   - Horário: 11:35 - 14:05
   - Rated

3. **Codeforces Round 1114 (Div. 3)**
   - Data: 04/08/2026
   - Horário: 11:35 - 13:50
   - Rated

4. **Codeforces Round 1115 (Div. 2)**
   - Data: 06/08/2026
   - Horário: 11:35 - 13:35
   - Rated

5. **Educational Codeforces Round 193 (Rated for Div. 2)**
   - Data: 07/08/2026
   - Horário: 11:35 - 13:35
   - Rated

6. **Codeforces Round 1116 (Div. 1 e Div. 2)**
   - Data: 09/08/2026
   - Horário: 11:35 - 14:05
   - Rated

Esses são os eventos recentes que ocorreram no Codeforces.
```
- Opinião: O agente capturou eventos que ocorreram há 30/31 dias atrás, note que a ICPC da Huawei foi retornado na API,
 mas eu acredito que ele não inseriu pois pode ter levantado dúvida se por acaso o usuário está ciente que está tendo e fazendo
 essa ICPCou não, não é algo tão grave esses dois pontos, mas respondeu de forma razoável. Não vejo necessidade de calibração.

**E2.** "Quantos problemas tem no Codeforces sobre 'implementation'?"
Esperado: `Problemset` com `tags=implementation`, `limit` dentro de 1-100 (nunca 0).
Valida: regressão do bug `limit=0` já corrigido no backend — confirmar que o agente nunca manda 0 nem valor fora do range.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Problemset -> MM -> Resposta
- Resposta:
```
Existem 3048 problemas no Codeforces relacionados à tag "implementation".
```
- Opinião: Funcional e correto.

**E3.** "Me mostra todas as contests da Huawei, sem exceção."
Esperado: sem filtro de data (`start`/`end` vazios), `q=Huawei`, possivelmente `limit` maior que o padrão de 10.
Valida: regressão do caso testado antes (11 eventos retornados) — confirmar que o agente ajusta `limit` quando o pedido é "todos"/"sem exceção".
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Events -> MM -> Resposta
- Events:
    - Input: {"q":"Huawei","order_by":"startTime","timezone":"America/Sao_Paulo","limit":100,"page":1}
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
        {
        "id": "17elpo1tb38t82j76j4bkngleg",
        "summary": "ICPC Challenge 2021: Marathon (powered by Huawei)",
        "link": "https://www.google.com/calendar/event?eid=MTdlbHBvMXRiMzh0ODJqNzZqNGJrbmdsZWcgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1524\">ICPC Challenge 2021: Marathon (powered by Huawei)</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2021-05-07T15:37:19.684000+00:00",
        "start": "2021-05-26 01:00:00 -03:00",
        "end": "2021-05-30 01:00:00 -03:00"
        },
        {
        "id": "hv67k6k97ajc5korsr9drpdgt4",
        "summary": "ICPC 2022 Online Challenge powered by HUAWEI - Problem",
        "link": "https://www.google.com/calendar/event?eid=aHY2N2s2azk3YWpjNWtvcnNyOWRycGRndDQgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1723\">ICPC 2022 Online Challenge powered by HUAWEI - Problem 1</a>\n<a href=\"https://codeforces.com/contests/1724\">ICPC 2022 Online Challenge powered by HUAWEI - Problem 2</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2022-09-15T09:10:59.406000+00:00",
        "start": "2022-09-14 21:00:00 -03:00",
        "end": "2022-09-29 21:00:00 -03:00"
        },
        {
        "id": "09iqs8hsdun1qeqkh1a6t9ckh8",
        "summary": "45th ICPC World Finals Challenge powered by Huawei - Problem",
        "link": "https://www.google.com/calendar/event?eid=MDlpcXM4aHNkdW4xcWVxa2gxYTZ0OWNraDggazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1751\">45th ICPC World Finals Challenge powered by Huawei - Problem 2</a>\n<a href=\"https://codeforces.com/contests/1752\">45th ICPC World Finals Challenge powered by Huawei - Problem 1</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2022-11-04T13:06:55.590000+00:00",
        "start": "2022-11-16 21:00:00 -03:00",
        "end": "2022-11-30 20:59:00 -03:00"
        },
        {
        "id": "91pj3uhqnlkh3r8ttt2bhbhffs",
        "summary": "ICPC 2023 Online Spring Challenge powered by Huawei",
        "link": "https://www.google.com/calendar/event?eid=OTFwajN1aHFubGtoM3I4dHR0MmJoYmhmZnMgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1813\">ICPC 2023 Online Spring Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2023-04-15T16:11:36.476000+00:00",
        "start": "2023-04-13 08:00:00 -03:00",
        "end": "2023-04-27 08:00:00 -03:00"
        },
        {
        "id": "8fh0983ra5cd5k76p4313ru0qg",
        "summary": "ICPC 2023 Online Challenge powered by Huawei",
        "link": "https://www.google.com/calendar/event?eid=OGZoMDk4M3JhNWNkNWs3NnA0MzEzcnUwcWcgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1885\">ICPC 2023 Online Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2023-11-12T15:15:31.276000+00:00",
        "start": "2023-11-20 04:00:00 -03:00",
        "end": "2023-12-04 04:00:00 -03:00"
        },
        {
        "id": "n4ul37ii31tvlakf29bkgfiq1k",
        "summary": "2023 Post World Finals Online ICPC Challenge powered by Huawei",
        "link": "https://www.google.com/calendar/event?eid=bjR1bDM3aWkzMXR2bGFrZjI5YmtnZmlxMWsgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/1953\">2023 Post World Finals Online ICPC Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2024-05-23T14:53:07.174000+00:00",
        "start": "2024-05-06 12:00:00 -03:00",
        "end": "2024-05-23 13:00:00 -03:00"
        },
        {
        "id": "799kdhcusfsoskn2tgia35hm90",
        "summary": "2024 ICPC World Finals Challenge powered by Huawei",
        "link": "https://www.google.com/calendar/event?eid=Nzk5a2RoY3VzZnNvc2tuMnRnaWEzNWhtOTAgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
        "description": "<a href=\"https://codeforces.com/contests/2015\">2024 ICPC World Finals Challenge powered by Huawei</a>\n\nUnrated\n\nAdded automatically",
        "updated": "2025-08-07T10:53:44.921000+00:00",
        "start": "2024-09-17 03:34:00 -03:00",
        "end": "2024-09-17 06:34:00 -03:00"
        },
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
Aqui estão todas as contests da Huawei que encontrei:

1. **Huawei Honorcup Marathon 1**
   - Data: 20/09/2018 - 04/10/2018
   - Horário: 14:00 - 14:00
   - Unrated

2. **Huawei Honorcup Marathon 2**
   - Data: 30/09/2019 - 14/10/2019
   - Horário: 15:00 - 15:00
   - Unrated

3. **ICPC Challenge 2021: Marathon (powered by Huawei)**
   - Data: 26/05/2021 - 30/05/2021
   - Horário: 01:00 - 01:00
   - Unrated

4. **ICPC 2022 Online Challenge powered by HUAWEI - Problem**
   - Data: 14/09/2022 - 29/09/2022
   - Horário: 21:00 - 21:00
   - Unrated

5. **45th ICPC World Finals Challenge powered by Huawei - Problem**
   - Data: 16/11/2022 - 30/11/2022
   - Horário: 21:00 - 20:59
   - Unrated

6. **ICPC 2023 Online Spring Challenge powered by Huawei**
   - Data: 13/04/2023 - 27/04/2023
   - Horário: 08:00 - 08:00
   - Unrated

7. **ICPC 2023 Online Challenge powered by Huawei**
   - Data: 20/11/2023 - 04/12/2023
   - Horário: 04:00 - 04:00
   - Unrated

8. **2023 Post World Finals Online ICPC Challenge powered by Huawei**
   - Data: 06/05/2024 - 23/05/2024
   - Horário: 12:00 - 13:00
   - Unrated

9. **2024 ICPC World Finals Challenge powered by Huawei**
   - Data: 17/09/2024
   - Horário: 03:34 - 06:34
   - Unrated

10. **ICPC 2025 Online Winter Challenge powered by Huawei**
    - Data: 26/12/2025 - 11/01/2026
    - Horário: 08:00 - 08:00
    - Unrated

11. **ICPC 2026 Online Challenge 1 powered by Huawei**
    - Data: 14/08/2026 - 28/08/2026
    - Horário: 08:00 - 08:00
    - Unrated

Essas são todas as contests da Huawei que encontrei.
```
- Opinião: A ICPC de 2024 é bem curiosa, pois a API retornou dois eventos com IDs diferentes, mas com outros dados iguais, 
 como o nome "2024 ICPC World Finals Challenge powered by Huawei", data, horário, link e descrição idênticas, talvez um
 erro cometido pela equipe do Codeforces? Mas fora isso, se considerar que foi um erro, ou tenha sido duas Divs ou similar,
 o agente respondeu correto.

**E4.** "Um problema tipo 2081G2, o que quer dizer o G2?"
Esperado: resposta direto do conhecimento do System Message (índice = variante difícil), sem precisar de tool — mas pode complementar com `Problem` se quiser mostrar o problema real.
Valida: instrução sobre nomenclatura de ID (contestId + index) está sendo aplicada como conhecimento direto, não obrigando tool desnecessária.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Memória -> Resposta
- Resposta:
```
O identificador de um problema no Codeforces é composto por dois elementos principais:

1. **ID da Contest**: Um número que identifica a contest específica em que o problema foi apresentado. No caso do problema 2081G2, o ID da contest é **2081**.

2. **Índice do Problema**: Uma letra (e possivelmente um número) que identifica o problema dentro da contest. No caso de 2081G2, o índice é **G2**.

O **G2** indica que o problema é a segunda variante do problema G na contest 2081. Em algumas contests, problemas podem ter múltiplas variantes (como G1, G2, etc.), geralmente para oferecer versões mais fáceis ou mais difíceis do mesmo problema.

Resumindo, **2081G2** significa o problema G2 da contest 2081.
```
- Opinião: Tecnicamente está correto, apesar de não ter dito 100% de certeza que variante 2 costuma ser a difícil.
