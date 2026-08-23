# Resultado da Primeira Rodada de Calibração do GPC (B-1)

---

### B. Fora de escopo / disclaimer (4)

**B1.** "Você é oficial do Codeforces?"
Esperado: sem tool, resposta direto do System Message/disclaimer — não afiliado, projeto pessoal.
Valida: identidade sem precisar de RAG para algo que já está fixado no prompt.
Realidade:
- Fluxo: Trigger -> Garoto -> Memória -> Modelo -> Resposta
- Resposta:
```text
Não, eu não sou afiliado, endossado ou mantido pelo Codeforces. 
Sou um projeto pessoal e independente criado para ajudar usuários a navegar a plataforma. 
Sempre recomendo verificar as informações diretamente nas fontes oficiais do Codeforces, 
especialmente para questões sobre termos de uso, política de privacidade ou regras, pois posso estar desatualizado.
```
- Opinião: Totalmente transparente, sem precisar do disclaimer.md

**B2.** "Isso aqui é pago? Vou ser cobrado?"
Esperado: sem tool, resposta baseada no disclaimer (gratuito, sem fins comerciais).
Valida: cobre conteúdo do disclaimer.md que ainda não tinha sido testado diretamente.
Realidade:
- Fluxo: Trigger -> Garoto -> Mem. + Modelo -> Documents Vector Store -> Mem. + Modelo -> Resposta
- DVS:
    - Input: `Termos e Condições`
    - Retorna:
    ```json
    {
        "response": [
            {
            "type": "text",
            "text": "{\"pageContent\":\"## Limitações da IA\\n\\nO GPC é baseado em um modelo de linguagem (IA) e **pode cometer erros**,\\ninterpretar mal uma pergunta, ou fornecer informações desatualizadas ou\\nimprecisas. Ele não deve ser tratado como fonte oficial ou definitiva.\\n\\n**Antes de tomar qualquer decisão importante** (especialmente sobre regras de\\ncontests, prazos, ou termos de uso), **confira sempre a informação diretamente\\nnas fontes oficiais do Codeforces**:\\n\\n- Termos e Condições: https://codeforces.com/terms\\n- Política de Privacidade: https://codeforces.com/privacy\\n- Ajuda / FAQ: https://codeforces.com/help\\n\\n## Natureza do projeto\\n\\n- **Sem fins comerciais** — o GPC não vende, revende ou monetiza nenhum\\n  conteúdo da pla\",\"metadata\":{\"source\":\"disclaimer\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":16,\"to\":33}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"o projeto\\n\\n- **Sem fins comerciais** — o GPC não vende, revende ou monetiza nenhum\\n  conteúdo da plataforma Codeforces.\\n- **Gratuito** — de uso livre, sem custo, sem coleta de dados para fins\\n  comerciais.\\n- **Sem intenção de prejudicar** — o GPC não tem qualquer objetivo de\\n  sobrecarregar, burlar ou causar dano à plataforma Codeforces ou aos seus\\n  usuários.\\n\\n## Dúvidas ou problemas\\n\\nSe você identificar alguma informação incorreta fornecida pelo GPC, ou tiver\\nqualquer dúvida sobre este projeto, entre em contato por meio do \\n[link aqui](https://github.com/jppgmx/gpc).\",\"metadata\":{\"source\":\"disclaimer\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":30,\"to\":44}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"content\\nfrom external platforms, Registration and authentication, Interaction with\\nexternal social networks and platforms, Geolocation, Managing contacts and\\nsending messages, Infrastructure monitoring and Hosting and backend\\ninfrastructure.\\n\\nThe Personal Data used for each purpose is outlined in the specific sections of\\nthis document.\\n\\n## Detailed information on the processing of Personal Data\\n\\nPersonal Data is collected for the following purposes and using the following\\nservices:\\n\\n### Analytics\\n\\nThe services contained in this section enable the Owner to monitor and analyze\\nweb traffic and can be used to keep track of User behavior. At times we may\\nshare this information in aggregated anony\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":64,\"to\":82}}}}"
            },
            {
            "type": "text",
            "text": "{\"pageContent\":\"n be used to keep track of User behavior. At times we may\\nshare this information in aggregated anonymous form with third parties.\\n\\n#### Google Analytics (Google Inc.)\\n\\nGoogle Analytics is a web analysis service provided by Google Inc. (“Google”).\\nGoogle utilizes the Data collected to track and examine the use of this\\nApplication, to prepare reports on its activities and share them with other\\nGoogle services. Google may use the Data collected to contextualize and\\npersonalize the ads of its own advertising network.\\n\\nPersonal Data collected: Cookies and Usage data.\\n\\nPlace of processing: US –  [Privacy\\nPolicy](https://www.google.com/intl/en/policies/privacy/)  –  [Opt\\nOut](https://tools.google.c\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":81,\"to\":96}}}}"
            }
        ]
    }
    ```
- Resposta:
```
Não, o uso do GPC é gratuito e sem custo. Não há cobrança para utilizar este assistente. 
Além disso, o projeto não coleta dados para fins comerciais.
```
- Opinião: O DVS capturou tanto fragmentos do disclaimer.md como também da Política de Privacidade.
  Ele respondeu corretamente, e acho que não é algo para alarmar.

**B3.** "Qual é a previsão do tempo hoje?"
Esperado: recusa educada, redireciona para o escopo do GPC.
Valida: não tenta responder por conhecimento geral fora do propósito declarado.
Realidade:
- Fluxo: Trigger -> Garoto -> Mem. + Modelo -> Resposta
- Resposta: `Desculpe, não tenho acesso a informações meteorológicas. Sou especializado em ajudar com a plataforma Codeforces.`
- Opinião: Ele não tem informações de previsão do tempo (o que é óbvio pois não há tools para isso) e está fora de seu escopo.

**B4.** "Escreve uma redação sobre história do Brasil."
Esperado: recusa, reforça escopo (Codeforces + C/C++).
Valida: mesmo teste de B3, mas com pedido mais "convidativo" a fugir do escopo (tarefa que o modelo tecnicamente sabe fazer).
Realidade:
- Fluxo: O mesmo de B3
- Resposta:
```
Desculpe, não posso ajudar com isso. Sou um assistente especializado na plataforma 
Codeforces e não tenho informações sobre história do Brasil.
```
- Opinião: Está correto, não foge do escopo definido no System Message.