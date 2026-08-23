# Resultado da Primeira Rodada de Calibração do GPC (A-3)

## Espera-se

- Evitar duplicatas no Vector Store;
- Ajustado a menção dos problemas;
- Ajustado a citação das contests;

## O que foi calibrado

- Mudanças no fluxo do gpc-docs para:
```
[Manual Trigger]
        │
        ├──────────────┬──────────────┐
        │              │              │
        ▼              ▼              ▼
    [Terms]      [Privacy]     [Disclaimer]
        │              │              │
        ▼              ▼              ▼
 [Set Terms]   [Set Privacy]  [Set Disclaimer]
        └──────────────┼──────────────┘
                       ▼
                    [Merge]
                       │
                       ▼
           [Simple Vector Store (com Clear Store)]
```
Dessa forma, podemos limpar e inserir tudo novamente.
- Sobre problemas: `- Ao mencionar um problema, use sempre o formato combinado (ex: 1466D), não separado`
- Sobre contests: 
```
- Ao listar múltiplos itens retornados por uma ferramenta (contests, problemas, eventos), inclua TODOS os itens da resposta da ferramenta, sem omitir nenhum, mesmo que a lista seja longa.
```

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

**A2 (3º Execução).** "O que são os Termos de Uso do Codeforces?"
Esperado: `Documents Vector Store` (busca em terms.md).
Valida: RAG básico funcionando.
Realidade:
    - Fluxo: Trigger -> Garoto -> Memória -> Modelo -> Documents Vector Store + Embeddings -> Memória
      -> Modelo -> Resposta
    - Documents Vector Store:
        - Input: `{"input": "Terms and Conditions"}`
        - Output:
            ```json
            [
                {
                    "type": "text",
                    "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"line\":2,\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
                },
                {
                    "type": "text",
                    "text": "{\"pageContent\":\"to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\\n\\n### Your Content.\\n\\nIn these Website Terms And Conditions, “Your Content” shall mean any audio, video, text, images or\\nother material you choose to display on this Website. With respect to Your Content, by displaying\\nit, you grant Codeforces a non-exclusive, worldwide, irrevocable, royalty-free, sublicensable\\nlicense to use, reproduce, adapt, publish, translate and distribute it in any and all media. Your\\nContent must be your own and must not be infringing on any third party’s rights. Codeforces reserves\\nthe right to remove any of Your Content from this Website at any time, and for any reason,\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"line\":2,\"loc\":{\"lines\":{\"from\":25,\"to\":35}}}}"
                },
                {
                    "type": "text",
                    "text": "{\"pageContent\":\"e provisions of these Terms.\\n\\n### Severability.\\n\\nIf any provision of these Terms is found to be unenforceable or invalid under any applicable law,\\nsuch unenforceability or invalidity shall not render these Terms unenforceable or invalid as a\\nwhole, and such provisions shall be deleted without affecting the remaining provisions herein.\\n\\n### Variation of Terms.\\n\\nCodeforces is permitted to revise these Terms at any time as it sees fit, and by using this Website\\nyou are expected to review such Terms on a regular basis to ensure you understand all terms and\\nconditions governing use of this Website.\\n\\n### Assignment.\\n\\nCodeforces shall be permitted to assign, transfer, and subcontract its rights and\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"line\":2,\"loc\":{\"lines\":{\"from\":57,\"to\":73}}}}"
                },
                {
                    "type": "text",
                    "text": "{\"pageContent\":\"fic rules (\\\"Rules\\\") for a Contest on the Contest\\nwebsite, which become part of these Terms and your agreement with us with respect to the Contest.\\n\\n### Restrictions.\\n\\nYou are expressly and emphatically restricted from all of the following:\\n\\n* selling, sublicensing and/or otherwise commercializing any Website material;\\n* using this Website in any way that is, or may be, damaging to this Website;\\n* using this Website in any way that impacts user access to this Website;\\n* using this Website contrary to applicable laws and regulations, or in a way that causes, or may cause, harm to the Website, or to any person or business entity;\\n* using this Website to engage in any advertising or marketing;\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"line\":2,\"loc\":{\"lines\":{\"from\":15,\"to\":26}}}}"
                },
                {
                    "type": "text",
                    "text": "{\"pageContent\":\"content\\nfrom external platforms, Registration and authentication, Interaction with\\nexternal social networks and platforms, Geolocation, Managing contacts and\\nsending messages, Infrastructure monitoring and Hosting and backend\\ninfrastructure.\\n\\nThe Personal Data used for each purpose is outlined in the specific sections of\\nthis document.\\n\\n## Detailed information on the processing of Personal Data\\n\\nPersonal Data is collected for the following purposes and using the following\\nservices:\\n\\n### Analytics\\n\\nThe services contained in this section enable the Owner to monitor and analyze\\nweb traffic and can be used to keep track of User behavior. At times we may\\nshare this information in aggregated anony\",\"metadata\":{\"source\":\"blob\",\"blobType\":\"application/json\",\"line\":2,\"loc\":{\"lines\":{\"from\":64,\"to\":82}}}}"
                }
            ]
            ```
        - Resposta:
            ```text
            Os Termos de Uso do Codeforces são as regras e condições que os usuários devem seguir ao utilizar a plataforma. Eles definem como você pode usar o site, o que pode e não pode fazer, e como o Codeforces lida com o conteúdo que você publica. Aqui estão alguns pontos-chave:

            1. **Uso do Site**: Você não pode comercializar o material do site, danificá-lo, afetar o acesso de outros usuários, ou usá-lo de forma contrária às leis aplicáveis.
            2. **Conteúdo do Usuário**: Ao publicar conteúdo (como texto, imagens ou vídeos), você concede ao Codeforces uma licença para usar, reproduzir, adaptar e distribuir esse conteúdo. O Codeforces pode remover qualquer conteúdo a qualquer momento.
            3. **Alterações nos Termos**: O Codeforces pode revisar os Termos de Uso a qualquer momento, e é esperado que os usuários os revisem regularmente.
            4. **Responsabilidades**: O Codeforces não se responsabiliza por danos resultantes do uso do site, e os usuários são responsáveis por suas ações na plataforma.

            Para obter informações completas e atualizadas, recomendo que você consulte diretamente os Termos de Uso oficiais do Codeforces. Lembre-se de que eu sou um assistente não oficial e posso cometer erros, então sempre verifique as informações nas fontes oficiais.
            ```
        - Opinião: Há correspondências do terms.md presentes, boa contextualização e sem duplicatas.

**A3 (3º Execução).** "Quais dados pessoais o Codeforces coleta?"
Esperado: `Documents Vector Store` (busca em privacy.md).
Valida: já testado antes (prova de fogo) — deve seguir preciso, sem alucinar campo que não está no doc.
Realidade:
    - Fluxo: Trigger -> Garoto -> Memória -> Modelo -> Documents Vector Store + Embeddings -> Memória
      -> Modelo -> Resposta
    - Documents Vector Store:
        - Input: `{"input": "Privacy Policy"}`
        - Output:
            ```json
            [
            {
                "type": "text",
                "text": "{\"pageContent\":\"y\\npolicy or by dedicated explanation text contextually with the Data collection.\\nThe Personal Data may be freely provided by the User, or collected automatically\\nwhen using this Application. Any use of Cookies - or of other tracking tools -\\nby this Application or by the owners of third party services used by this\\nApplication, unless stated otherwise, serves to identify Users and remember\\ntheir preferences, for the sole purpose of providing the service required by the\\nUser. Failure to provide certain Personal Data may make it impossible for this\\nApplication to provide its services.\\n\\nUsers are responsible for any Personal Data of third parties obtained, published\\nor shared through this Applica\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":18,\"to\":29}}}}"
            },
            {
                "type": "text",
                "text": "{\"pageContent\":\"legal action arising from improper\\nuse of this Application or the related services. The User declares to be aware\\nthat the Data Controller may be required to reveal personal data upon request of\\npublic authorities.\\n\\n### Additional information about User's Personal Data\\n\\nIn addition to the information contained in this privacy policy, this\\nApplication may provide the User with additional and contextual information\\nconcerning particular services or the collection and processing of Personal Data\\nupon request.\\n\\n### System logs and maintenance\\n\\nFor operation and maintenance purposes, this Application and any third party\\nservices may collect files that record interaction with this Application (Sy\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":211,\"to\":226}}}}"
            },
            {
                "type": "text",
                "text": "{\"pageContent\":\"content\\nfrom external platforms, Registration and authentication, Interaction with\\nexternal social networks and platforms, Geolocation, Managing contacts and\\nsending messages, Infrastructure monitoring and Hosting and backend\\ninfrastructure.\\n\\nThe Personal Data used for each purpose is outlined in the specific sections of\\nthis document.\\n\\n## Detailed information on the processing of Personal Data\\n\\nPersonal Data is collected for the following purposes and using the following\\nservices:\\n\\n### Analytics\\n\\nThe services contained in this section enable the Owner to monitor and analyze\\nweb traffic and can be used to keep track of User behavior. At times we may\\nshare this information in aggregated anony\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":64,\"to\":82}}}}"
            },
            {
                "type": "text",
                "text": "{\"pageContent\":\"n be used to keep track of User behavior. At times we may\\nshare this information in aggregated anonymous form with third parties.\\n\\n#### Google Analytics (Google Inc.)\\n\\nGoogle Analytics is a web analysis service provided by Google Inc. (“Google”).\\nGoogle utilizes the Data collected to track and examine the use of this\\nApplication, to prepare reports on its activities and share them with other\\nGoogle services. Google may use the Data collected to contextualize and\\npersonalize the ads of its own advertising network.\\n\\nPersonal Data collected: Cookies and Usage data.\\n\\nPlace of processing: US –  [Privacy\\nPolicy](https://www.google.com/intl/en/policies/privacy/)  –  [Opt\\nOut](https://tools.google.c\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":81,\"to\":96}}}}"
            },
            {
                "type": "text",
                "text": "{\"pageContent\":\"s a video content visualization service provided by Google Inc. that\\nallows this Application to incorporate content of this kind on its pages.\\n\\nPersonal Data collected: Cookies and Usage data.\\n\\nPlace of processing: US –  [Privacy\\nPolicy](https://www.google.it/intl/en/policies/privacy/)\\n\\n### Geolocation\\n\\n#### Geolocation (This Application)\\n\\nThis Application may collect, use, and share User location Data in order to\\nprovide location-based services. Most browsers and devices provide tools to opt\\nout from this feature by default. If explicit authorization has been provided,\\nthe User’s location data may be tracked by this Application.\\n\\nPersonal Data collected: geographic position.\\n\\n### Interactio\",\"metadata\":{\"source\":\"privacy\",\"blobType\":\"text/plain\",\"loc\":{\"lines\":{\"from\":119,\"to\":138}}}}"
            }
            ]
            ```
        - Resposta:
            ```text
            O Codeforces coleta os seguintes tipos de dados pessoais:

            1. **Dados Fornecidos pelo Usuário**:
            - Informações fornecidas voluntariamente durante o cadastro ou uso da plataforma, como nome de usuário e e-mail.

            2. **Dados Coletados Automaticamente**:
            - **Cookies e Dados de Uso**: Para identificar usuários, lembrar preferências e fornecer os serviços solicitados.
            - **Logs do Sistema**: Arquivos que registram a interação com a plataforma para fins de operação e manutenção.
            - **Dados de Análise**: Como os do Google Analytics, para monitorar e analisar o tráfego da web e o comportamento do usuário. Esses dados podem ser compartilhados de forma agregada e anônima com terceiros.

            3. **Dados de Geolocalização**:
            - **Localização Geográfica**: O Codeforces pode coletar, usar e compartilhar dados de localização do usuário para fornecer serviços baseados em localização, desde que haja autorização explícita.

            4. **Interação com Plataformas Externas**:
            - Dados obtidos através de redes sociais e outras plataformas externas quando o usuário interage com o Codeforces por meio delas.

            Para mais detalhes, consulte a Política de Privacidade oficial do Codeforces. Lembre-se de que eu sou um assistente não oficial e posso cometer erros, então sempre verifique as informações nas fontes oficiais.
            ```
        - Opinião: Há correspondências do privacy.md presentes, excelente contextualização e
          considero excelente o novo design do gpc-docs.

**A4 (3º Execução).** "Me mostra problemas de rating 1500."
Esperado: `Problemset` com `rating=1500`, sem `q`/`tags`.
Valida: filtro numérico isolado, sem ruído de outros parâmetros.
Realidade: ** Mesmo fluxo e resposta, apenas a atualização **
        - Resposta:
            ```
            Aqui estão alguns problemas com rating 1500:

            1. **1466D - 13th Labour of Heracles**
            - Tags: Estruturas de Dados, Guloso, Ordenação, Árvores

            2. **468A - 24 Game**
            - Tags: Guloso, Matemática, Algoritmos Construtivos

            3. **409H - A + B Strikes Back**
            - Tags: Força Bruta, Implementação, DSU, Algoritmos Construtivos, *Especial*

            4. **1166C - A Tale of Two Lands**
            - Tags: Ordenação, Busca Binária, Dois Ponteiros

            5. **1278B - A and B**
            - Tags: Guloso, Matemática

            6. **1873G - ABBC or BACB**
            - Tags: Guloso, Algoritmos Construtivos

            7. **1516B - AGAGA XOOORRR**
            - Tags: Programação Dinâmica, Força Bruta, Guloso, Máscaras de Bits

            8. **1379A - Acacius and String**
            - Tags: Força Bruta, Implementação, Strings

            9. **2026C - Action Figures**
            - Tags: Estruturas de Dados, Força Bruta, Guloso, Implementação, Busca Binária, Algoritmos Construtivos

            10. **2027C - Add Zeros**
                - Tags: Estruturas de Dados, Programação Dinâmica, Força Bruta, Guloso, DFS e Similares, Grafos

            Esses problemas cobrem uma variedade de conceitos e técnicas, como estruturas de dados, algoritmos guloso, busca binária, entre outros.
            ```
        - Opinião: Respostas boas, ID combinado, e a naturalização das tags foi excelente.

**A5 (2º Execução).** "O que é o problema 4A?"
Esperado: `Problem` com ID `4A` no path (não `Problemset` com `contest_id=4&index=A`).
Valida: agente escolhe a tool de item único, não a de busca, quando há ID exato.
Realidade: ** Respostas consistente, a forma de dizer varia, mas basta o usuário pedir detalhes. **
    - Resposta:
        ```text
        O problema **4A**, também conhecido como **"Watermelon"**, é um problema de programação com as seguintes características:

        - **Rating**: 800
        - **Tags**: Força Bruta, Matemática
        - **Número de Resoluções**: 719.489 (até o momento)

        Esse problema é relativamente simples e envolve conceitos básicos de matemática e força bruta. Se precisar de mais detalhes ou ajuda para resolvê-lo, é só avisar!
        ```
    - Opinião: Respondeu bem também, na maioria das vezes, o resultado depende do prompting e do contexto.

**A6 (3º Execução).** "Quais contests já aconteceram esse mês?"
Esperado: `Contests` com `phase=FINISHED`, período implícito ou textual do mês corrente.
Valida: única exceção documentada ao viés "futuro por padrão" — usuário pediu histórico explicitamente.
Realidade: ** Mesmo resultado, atualizando resposta nova **
        - Resposta:
            ```
                Aqui estão os contests que já terminaram este mês:

                1. **Codeforces Round 1117 (Div. 2)**
                - Data: 17 de agosto de 2026
                - Duração: 2 horas

                2. **Codeforces Round 1116 (Div. 2)**
                - Data: 9 de agosto de 2026
                - Duração: 2 horas e 30 minutos

                3. **Codeforces Round 1116 (Div. 1)**
                - Data: 9 de agosto de 2026
                - Duração: 2 horas e 30 minutos

                4. **Codeforces Round 1115 (Div. 2)**
                - Data: 6 de agosto de 2026
                - Duração: 2 horas

                5. **Codeforces Round 1113 (Div. 2)**
                - Data: 1 de agosto de 2026
                - Duração: 2 horas e 30 minutos

                Todos os contests listados acima já foram finalizados. Se precisar de mais informações sobre algum deles, é só pedir!
            ```
        - Opnião: Houve uma imprecisão, no próximo round de calibração, iremos focar aqui,

**A7 (2º Execução).** "Detalhes da contest 2257."
Esperado: `Contest` (singular) com `contestId=2257`.
Valida: agente não usa `Contests` (lista) para um ID específico já conhecido.
Realidade: ** Respostas estão boas. **
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