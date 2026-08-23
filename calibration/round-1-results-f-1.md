# Resultado da Primeira Rodada de Calibração do GPC (F-1)

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

---

### F. Limites / dados ausentes (3)

**F1.** "Quero problemas com tag 'programação quântica'."
Esperado: `Tags` primeiro, não encontra correspondência, agente informa que não existe essa tag no Codeforces — sem inventar nome parecido.
Valida: "não invente resposta" aplicado a filtro de tag que genuinamente não existe.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Resposta
- Resposta:
```
Infelizmente, não encontrei nenhuma tag relacionada a "programação quântica" no Codeforces. 
As tags disponíveis são mais focadas em tópicos clássicos de programação competitiva, 
como estruturas de dados, algoritmos e matemática. Se tiver interesse em outros tópicos, posso tentar ajudar!
```
- Opinião: Ele fez o certo e não continuou para Problemset.

**F2.** Forçar cenário de falha de tool (ex: desligar temporariamente o backend e perguntar algo que dependa dele).
Esperado: até 3 tentativas, depois informa claramente que não conseguiu obter o dado — sem inventar substituto.
Valida: regra de retry + aviso de falha, que só foi documentada, nunca testada de fato.
Realidade:
- Alvo: Contest
- "Detalhe a contest 2000"
- Fluxo TSR -> Resposta
- Resposta: Desculpe, estou com dificuldades técnicas no momento. Tente novamente em instantes 🙁
- Opinião: Se o backend cair, o agente vai estar incapacitado de fazer qualquer coisa, pois com o novo design, o System Message vem do
    backend e todas as tools, exceto a CF System Status, dependem do backend.

**F3.** "Me dá o link do problema 9999Z." (ID que provavelmente não existe)
Esperado: `Problem` retorna vazio/erro, agente comunica que não encontrou, não monta link genérico do template sem confirmar que o problema existe.
Valida: evita "montar link please" (`problemset/problem/CONTEST_ID/INDICE`) para algo não confirmado — risco de literalmente devolver link quebrado com confiança.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Problem -> MM -> Resposta:
- Problem:
    - URL: http://backend:8000/api/problemset/problems/9999Z
    - Retorna:
    ```json
    {
        "error": "Problema não encontrado."
    }
    ```
- Resposta:
```
Não encontrei nenhum problema com o ID 9999Z. Posso ajudar com algo mais?
```
- Opinião: Fez bem saber primeiro se existe o problema, respondeu corretamente.