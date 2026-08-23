# Resultado da Primeira Rodada de Calibração do GPC (G-1)

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

---

### G. Uso da tool Tags como pré-passo (3)

**G1.** "Tem problema sobre aquela técnica de dois ponteiros?"
Esperado: `Tags` (buscar "two pointers" ou similar), depois `Problemset` com o nome exato.
Valida: reconhecimento de descrição vaga em português mapeando pra termo técnico em inglês.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Problemset -> MM -> Resposta
- Problemset:
    - Input: `{"tags":"two pointers","order_by":"rating","limit":100,"page":1}`
- Resposta:
```
Encontrei 653 problemas com a tag "two pointers". Aqui estão alguns exemplos:

- Notelock (800)
- All Lengths Subtraction (800)
- Two Screens (800)
- Seating in a Bus (800)
- Contest Proposal (800)
- Prefiquence (800)
- 1D Eraser (800)
- Parity Sort (800)
- Long Long (800)
- Sasha and Array Coloring (800)

Posso fornecer mais detalhes sobre algum problema específico ou continuar listando problemas com essa tag.
```
- Opinião: Respondeu, mas ocultou o ID do problema, e isso é ruim. Calibração necessária.

**G2.** "O que significa a tag '*special'?"
Esperado: `Tags`, resposta usando a descrição cadastrada (critério de julgamento não-padrão).
Valida: tag propositalmente "estranha" (com asterisco) — bom teste de tag que não é autoexplicativa.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Resposta
- Tags:
    - Descrição de *special: Problemas especiais ou de brincadeira, comuns em concursos de Primeiro de Abril (April Fools).
- Resposta:
```
A tag "*special" indica problemas especiais ou de brincadeira, geralmente encontrados em contests de Primeiro de Abril (April Fools).
```
- Opinião: Ele respondeu com base na descrição, não é certeza que essa descrição seja 100% correta.

**G3.** "Quero um problema de matemática, mas não sei o nome certo da tag."
Esperado: `Tags` retorna algo como "math", "number theory", "combinatorics" — agente pode perguntar qual o usuário prefere, ou já buscar com a mais genérica (`math`).
Valida: caso de ambiguidade real dentro da própria tool `Tags` — decisão do agente quando há múltiplas tags candidatas.
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Resposta
- Resposta:
```
A tag que você provavelmente está procurando é "math", que abrange problemas de matemática 
geral, equações e álgebra. Além disso, há também a tag "number theory" para problemas relacionados 
à teoria dos números, como números primos, MDC, MMC, aritmética modular e fatoração.
```
- Opinião: O agente apontou que poderia ser `math` ou candidatas como `number theory`, com isso, o usuário deverá escolher 
 ou perguntar outra coisa