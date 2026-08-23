# Resultado da Primeira Rodada de Calibração do GPC (G-2)

---

## Nomenclaturas:
- `TSN`: Trigger -> System Message -> Normalize
- `TSR`: Trigger -> System Message -> Report -> Message Fallback
- `MF`: Message Fallback
- `MM`: Memória -> Modelo

## O que foi calibrado
- Ausência do ID do problema

---

### G. Uso da tool Tags como pré-passo (3)

**G1 (2º Execução).** "Tem problema sobre aquela técnica de dois ponteiros?"
Esperado: `Tags` (buscar "two pointers" ou similar), depois `Problemset` com o nome exato.
Valida: reconhecimento de descrição vaga em português mapeando pra termo técnico em inglês.
Realidade:
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Problemset -> MM -> Resposta
- Problemset:
    - Input: `{"tags":"two pointers","order_by":"rating","limit":100,"page":1}`
- Resposta:
```
Encontrei 653 problemas relacionados à técnica de dois ponteiros. Aqui estão alguns exemplos:

- **1D Eraser** (ID: 1873D): Rating 800
- **23 Kingdom** (ID: 2101C): Rating 2200
- **A Bit Similar** (ID: 1469E): Rating 2400
- **A Shade of Moonlight** (ID: 989D): Rating 2500
- **Array Game** (ID: 1904C): Rating 1400

Posso continuar listando ou fornecer mais detalhes sobre algum problema específico.
```
- Opinião: Respondeu com o ID, poucas informações, mas como são exemplos ficou a critério de citar apenas.

**G2.** "O que significa a tag '*special'?"
Esperado: `Tags`, resposta usando a descrição cadastrada (critério de julgamento não-padrão).
Valida: tag propositalmente "estranha" (com asterisco) — bom teste de tag que não é autoexplicativa.
Realidade: ** Resposta tecnicamente correta **
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
Realidade: ** Resposta boa **
- Fluxo: TSN -> Garoto -> MM -> Tags -> MM -> Resposta
- Resposta:
```
A tag que você provavelmente está procurando é "math", que abrange problemas de matemática 
geral, equações e álgebra. Além disso, há também a tag "number theory" para problemas relacionados 
à teoria dos números, como números primos, MDC, MMC, aritmética modular e fatoração.
```
- Opinião: O agente apontou que poderia ser `math` ou candidatas como `number theory`, com isso, o usuário deverá escolher 
 ou perguntar outra coisa