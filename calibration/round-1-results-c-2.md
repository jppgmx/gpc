# Resultado da Primeira Rodada de Calibração do GPC (C-1)

## O que espera
- Resolver a determinação de ICPC, mesmo que tenha como type IOI ou outros;
- Bug corrigido da paginação;
- Confirmar usando o calendário que uma contest é rated ou não.

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

---

### C. Ambíguas entre duas tools (4)

**C1.** "Algum evento recente da Huawei?"
Esperado: `Events` com `q=Huawei`, sem `start`/`end` (regressão do bug já corrigido).
Valida: **caso de regressão conhecido** — já quebrou antes por empilhar filtro de data desnecessário.
Realidade: ** Resposta direta e suficiente **
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
Realidade: ** Associação feita corretamente e resposta razoável **
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

**C3 (2º Execução).** "Tem contest ICPC ativa agora?"
Esperado: `Contests` com `type=ICPC`/`phase=CODING` (fase é o diferencial dessa tool) — não `Events`.
Valida: escolha correta quando a pergunta pede *status/fase*, não *data/horário* — testa se o System Message atualizado ("Contests permite identificar a fase atual") está guiando bem.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Contests -> MM -> Resposta
- Contests:
    - URL: http://backend:8000/api/contests/
    - Params: `{"pretty_datetime":true,"timezone":"America/Sao_Paulo","type":"ICPC","phase":"CODING","order_by":"id","limit":10,"page":1}`
    - Retorna:
    ```js
    {
      "total": 0,
      "page": 1,
      "limit": 10,
      "contests": [],
    }
    ```
- Resposta:
```
Não há nenhuma contest do tipo ICPC ativa no momento.
```
- Opinião: Bug corrigido, mas ainda usa o type ICPC, como patch, poderia o agente primeiro procurar pelo termo ICPC, depois pelo
           type ICPC ou IOI como fallback.

**C4 (2º Execução).** "Quando é a próxima Codeforces Round e ela já está valendo pra rating?"
Esperado: possível uso combinado de `Events` (data/hora) + `Contests` (fase/tipo) — mas só se o agente julgar necessário, não por regra fixa de "sempre os dois".m
Valida: se a mudança no System Message (de "sempre use as duas" para uso mais seletivo) está funcionando — comparar com comportamento anterior.
Realidade:
- Fluxo: Trigger -> Garoto -> MM -> Events -> MM -> Resposta
- Contests:
    - Params: {"q":"Codeforces Round","start":"2026-08-23T00:00:00Z","order_by":"startTime","timezone":"America/Sao_Paulo","limit":1,"page":1}
    - Retorno:
    ```json
    {
      "total": 1,
      "page": 1,
      "limit": 1,
      "has_more": false,
      "events": [
        {
          "id": "a99dst19k4ffs2a0bggbpsfm0k",
          "summary": "CF R (Div. 2)",
          "link": "https://www.google.com/calendar/event?eid=YTk5ZHN0MTlrNGZmczJhMGJnZ2Jwc2ZtMGsgazIzajIzM2d0Y3ZhdTdhOHVsazJwMzYwbTRAZw&ctz=America/Sao_Paulo",
          "description": "<a href=\"https://codeforces.com/contests/2258\">Codeforces Round (Div. 2)</a>\n\nRated\n\nAdded automatically",
          "updated": "2026-08-19T14:54:34.565000+00:00",
          "start": "2026-08-29 11:35:00 -03:00",
          "end": "2026-08-29 13:35:00 -03:00"
        }
      ]
    }
    ```
- Resposta:
```
A próxima Codeforces Round (Div. 2) será no dia **29 de agosto de 2026**, das 11:35 às 13:35 (fuso horário: America/Sao_Paulo). Sim, ela está valendo para rating.
```
- Opinião: Respondeu certo, apenas o detalhe da formatação do fuso horário.
