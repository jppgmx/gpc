# Resultado da Primeira Rodada de Calibração do GPC (C-1)

# O que foi ajustado antes
- Modificado as query params para se tornar um JSON dinâmico:
```js
{{
  JSON.stringify(
      (() => {
        const NUMERIC_FIELDS = new Set(["limit", "page"])
        const params = {
          q: $fromAI("q", "Termo de busca textual livre para filtrar eventos por nome/descrição", "string"),
          start: $fromAI("start", "Data de início do intervalo (RFC 3339). Deixe vazio se o usuário não mencionar um período específico — buscas por nome/texto (q) já cobrem todos os períodos automaticamente", "string"),
          end: $fromAI("end", "Data de término do intervalo (RFC 3339). Deixe vazio se o usuário não mencionar um período específico", "string"),
          order_by: $fromAI("order_by", "startTime para ordenar por data do evento, updated para última modificação", "string"),
          timezone: "America/Sao_Paulo",
          limit: $fromAI("limit", "Número máximo de eventos a retornar (1-100).", "number"),
          page: $fromAI("page", "A página a procurar na pesquisa, caso haja mais itens acima do limite.", "number")
        }
  
        return Object.fromEntries(
          Object.entries(params).filter(([key, v]) => {
            if (v === undefined || v === null || v === "") return false;
            if (NUMERIC_FIELDS.has(key) && v === 0) return false;
            return true;
          })
        )
      })()
    )
}}
```

- O System Message agora está em um arquivo e é feito HTTP Request:
1. Trigger dispara;
2. Obtém SysMsg;
3. Se tudo certo, normaliza para injetar dados e passa ao agente;
4. Caso contrário, reporta e manda uma mensagem de fallback;
- Ajustes no em /api/problemset/tags

---

# Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

---

### C. Ambíguas entre duas tools (4)

**C1.** "Algum evento recente da Huawei?"
Esperado: `Events` com `q=Huawei`, sem `start`/`end` (regressão do bug já corrigido).
Valida: **caso de regressão conhecido** — já quebrou antes por empilhar filtro de data desnecessário.
Realidade:
- Fluxo: (Versão legada) Trigger -> Garoto -> MM (Memória e Modelo) -> Events -> MM -> Resposta
- Events:
    - URL: http://backend:8000/api/calendar/primary/events
    - Params: {"q":"Huawei","start":"2026-08-22T00:00:00Z","end":"2026-08-22T23:59:59Z","order_by":"startTime",
      "timezone":"America/Sao_Paulo","limit":1,"page":1}
    - Servidor: /api/calendar/primary/events?q=Huawei&start=2026-08-22T00%3A00%3A00Z&end=2026-08-22T23%3A59%3A59Z&order_by=startTime&timezone=America%2FSao_Paulo&limit=1&page=1
    - Output:
    ```
    {
        "total": 1,
        "page": 1,
        "limit": 1,
        "has_more": false,
        "events": [
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
```text
Sim, há um evento recente da Huawei:

- ICPC 2026 Online Challenge 1 powered by Huawei:
  - Data: 14 de agosto de 2026 às 08:00 até 28 de agosto de 2026 às 08:00
  - Fuso horário: -03:00
  - Link: https://codeforces.com/contests/2251
```
- Opinião: Respondeu bem, apenas a questão do fuso horário que poderia dizer de forma naturalizada

**C2.** "Quero problemas sobre teorema chinês do resto."
Esperado: `Tags` primeiro (buscar nome exato), depois `Problemset` com `tags=chinese remainder theorem`.
Valida: encadeamento de duas tools em sequência — o motivo de termos criado a tool `Tags`.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Problemset -> MM -> Resposta
- Tags:
  - Retorno:
  ```json
  {
    "count": 38,
    "tags": [
      {
        "name": "data structures",
        "description": "Estruturas de dados (Heaps, Árvores de Segmentos, Fenwick Trees, etc)."
      },
      ...,
      {
        "name": "string suffix structures",
        "description": "Estruturas de dados avançadas para sufixos de strings (Suffix Array, Suffix Automaton, Suffix Tree)."
      },
      {
        "name": "chinese remainder theorem",
        "description": "Teorema Chinês do Resto (CRT), utilizado em sistemas de congruências modulares simultâneas."
      },
      {
        "name": "*special",
        "description": "Problemas especiais ou de brincadeira, comuns em concursos de Primeiro de Abril (April Fools)."
      },
      ...,
      {
        "name": "meet-in-the-middle",
        "description": "Técnica 'Meet-in-the-Middle', que divide o espaço de busca complexo ao meio, resolve ambas as partes e as combina."
      }
    ]
  }
  ```
- Problemset:
  - Input: `{"tags":"chinese remainder theorem","limit":100,"page":1}`
  - Retorno:
  ```json
  {
    "total": 25,
    "page": 1,
    "limit": 100,
    "problems": [
      {
        "contestId": 2097,
        "index": "C",
        "name": "Bermuda Triangle",
        "type": "PROGRAMMING",
        "points": 1500,
        "rating": 2400,
        "solvedCount": 1056,
        "tags": [
          "implementation",
          "math",
          "number theory",
          "geometry",
          "chinese remainder theorem"
        ]
      },
      {
        "contestId": 1266,
        "index": "A",
        "name": "Competitive Programmer",
        "type": "PROGRAMMING",
        "points": 500,
        "rating": 1000,
        "solvedCount": 17827,
        "tags": [
          "math",
          "chinese remainder theorem"
        ]
      },
      {
        "contestId": 919,
        "index": "E",
        "name": "Congruence Equation",
        "type": "PROGRAMMING",
        "points": 2000,
        "rating": 2100,
        "solvedCount": 2572,
        "tags": [
          "math",
          "number theory",
          "chinese remainder theorem"
        ]
      },
      ...
    ]
  }
  ```
- Resposta:
```
Aqui estão alguns problemas relacionados ao Teorema Chinês do Resto:

1. Bermuda Triangle (2097C)
2. Competitive Programmer (1266A)
3. Congruence Equation (919E)
4. ConstructOR (1748D)
5. Cyclic Cipher (722F)
6. Decypher the String (1117E)
7. Dyn-scripted Robot (Easy Version) (1993F1)
8. Dyn-scripted Robot (Hard Version) (1993F2)
9. Engineer Artem (1438C)
10. Epic Convolution (1054H)
11. GCD Guess (1665D)
12. GCD Table (338D)
13. Game of Scientists (Version 1) (2174E1)
14. Game of Scientists (Version 2) (2174E2)
15. Grid Covering (2217C)
16. King Keykhosrow's Mystery (2034A)
17. Koxia and Number Theory (1770C)
18. Nephren Runs a Cinema (896D)
19. Nikita and Order Statistics (993E)
20. Omkar and Akmar (1536F)
21. Power Tower (906D)
22. RGB Walking (2077G)
23. Remainders Game (687B)
24. Two chandeliers (1500B)
25. Zhily and Signpost (2223C)

Esses problemas envolvem o uso do Teorema Chinês do Resto para resolver sistemas de congruências modulares simultâneas.
```
- Opinião: Respondeu bem, se fosse para detalhar, o usuário pediria, e fez uma boa associação entre Problemset <-> Tags 

**C3.** "Tem contest ICPC ativa agora?"
Esperado: `Contests` com `type=ICPC`/`phase=CODING` (fase é o diferencial dessa tool) — não `Events`.
Valida: escolha correta quando a pergunta pede *status/fase*, não *data/horário* — testa se o System Message atualizado ("Contests permite identificar a fase atual") está guiando bem.
Realidade:
- Fluxo: Trigger -> Garoto -> (MM -> Contests 3x) -> MM -> Resposta
- Contests:
    - URL: http://backend:8000/api/contests/
    - Params: {"pretty_datetime":true,"type":"ICPC","phase":"CODING","order_by":"id","limit":1,"page":1}
    - Resposta:
    ```js
    {
    "total": 0,
    "page": 1,
    "limit": 1,
    "contests": [],
    "error": "Página inválida"
    }
    ```
- Resposta:
```
Infelizmente, não consegui obter os dados para responder sua pergunta.
```
- Opinião: Com base no que ocorreu, descobri um bug da API que quando a pesquisa resulta em zero, ele não passa no
  is_valid_page, alegando que a "Página é inválida", e é inválida pois não há para zero elementos.
  Corrigido, quando o total obtido for zero, apenas uma resposta vazia sem error.
  Curiosidade: a ICPC da Huawei de Agosto/2026 é do tipo IOI, então foi com essa pegadinha que o bug foi descoberto

**C4.** "Quando é a próxima Codeforces Round e ela já está valendo pra rating?"
Esperado: possível uso combinado de `Events` (data/hora) + `Contests` (fase/tipo) — mas só se o agente julgar necessário, não por regra fixa de "sempre os dois".m
Valida: se a mudança no System Message (de "sempre use as duas" para uso mais seletivo) está funcionando — comparar com comportamento anterior.
Realidade:
- Fluxo: Trigger -> Garoto -> MM -> Contests -> MM -> Resposta
- Contests:
    - Params: {"pretty_datetime":true,"type":"CF","phase":"BEFORE","order_by":"id","limit":1,"page":1}
    - Retorno:
    ```
    {
    "total": 1,
    "page": 1,
    "limit": 1,
    "contests": [
        {
        "id": 2258,
        "name": "Codeforces Round (Div. 2)",
        "type": "CF",
        "phase": "BEFORE",
        "frozen": false,
        "durationSeconds": 7200,
        "duration": "2:00:00",
        "startTimeSeconds": 1788014100,
        "relativeTimeSeconds": -569419,
        "startTime": "2026-08-29T17:35:00+03:00",
        "relativeTime": "2026-08-23T03:24:41+03:00",
        "timeZone": "Europe/Moscow"
        }
    ]
    }
    ```
- Resposta:
```
A próxima Codeforces Round é a Codeforces Round (Div. 2), que acontecerá em 29 de agosto de 2026 às 17:35 (UTC+3). 
Como ela ainda não começou, ela está valendo para rating.
```
- Opinião: Dá para garantir que é rated?
