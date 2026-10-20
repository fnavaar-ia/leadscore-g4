# Processo unificado — LeadScore G4

**Challenge 003 — Lead Scorer · Versão 1.0 · Consolidação em 20/10/2026**

Este documento reúne a preparação descrita no registro inicial e o desenvolvimento relatado no M6 em um processo único: entender o problema, depurar interpretações, especificar, construir por módulos, verificar, registrar decisões e preparar a submissão. Serve como narrativa do trabalho e roteiro para sua continuidade. Não substitui código, logs individuais ou o README exigido pelo desafio.

## 1. Fontes e alcance desta consolidação

| Fonte | Contribuição | Limite da evidência |
|---|---|---|
| [Registro inicial do processo](../process-log/fontes/registro-processo-lead-scorer.md) | Entendimento do desafio, análise inicial, correções, PRD e pacote de transição para o IDE. | A construção no Antigravity é atribuída ao relato do responsável; o próprio registro não atesta implementação ou testes. |
| [M6 — documentação completa](../M6_DOCUMENTACAO_COMPLETA.md) | Desenvolvimento M1–M6, política, interface, testes, publicações e pendências de entrega. | Contém resultados históricos narrados e algumas conclusões que precisam ser reconciliadas com os registros da versão final. |
| [PRD](PRD.md), [prompts](../prompts/01-M1-ingestao.md) e [referências do desafio](../references/challenge.md) | Requisitos, sequência, contratos e critérios de aceite. | Parte dos documentos preserva o estado do kit anterior à implementação. |
| [Logs por módulo](../process-log/), código e configuração locais | Rastreabilidade das etapas e correspondência entre decisões registradas e artefatos. | Leitura de arquivos não comprova execução atual ou disponibilidade remota. |

**Convenção:** “registrado” significa descrito nas fontes anteriores; “verificado nesta consolidação” significa inspeção documental ou de integridade realizada agora; “procedimento” descreve como executar as próximas etapas. Os testes, a interface e os endereços públicos não foram executados ou revalidados nesta revisão. As regras do repositório foram consultadas nas cópias locais em `references/`.

A cópia do registro inicial foi preservada integralmente em `process-log/fontes/`, com SHA-256 igual ao arquivo recebido. Os cinco CSVs de `data/raw/` conferem com os hashes do manifesto inicial. Isso verifica sua integridade em relação ao kit, sem validar sua origem externamente.

## 2. Objetivo, escopo e método

O usuário principal é o vendedor que precisa saber quais oportunidades abertas revisar primeiro e compreender o motivo da prioridade. Manager e RevOps precisam filtrar e consultar suas carteiras. A entrega deve funcionar com os dados reais, oferecer uma priorização explicável além de preço e permitir reprodução por outra pessoa.

O método adotado é desenvolvimento assistido por IA com decomposição modular, correção de hipóteses, verificações reais e julgamento humano registrado. A stack escolhida é Python, pandas e Streamlit, com pytest. Plotly aparece como dependência posterior de visualização, sem substituir o framework da aplicação. Não há APIs de IA em runtime.

Regras permanentes:

- Preservar `data/raw/`; normalizações ocorrem na camada preparada e saídas derivadas vão para `outputs/`. Resolver caminhos pela raiz do projeto.
- Manter oportunidades sem conta. Ausências geram avisos e tratamento documentado, sem valores inventados.
- Tratar o score como prioridade heurística, preço de catálogo como referência e idade desde engajamento como contexto. Não convertê-los em probabilidade, receita esperada ou inatividade.
- Usar `2017-12-31` como referência demonstrativa histórica, sem apresentá-la como snapshot oficial. Resultados históricos só podem compor análises até o corte permitido.
- Manter ingestão, análise, scoring e filtros separados da interface. Filtros selecionam uma fila já pontuada; não recalculam o score nem sua posição global.
- Trabalhar M1 → M2 → M3 → M4 → M5 → M6, encerrando cada módulo com evidências e revisão antes de avançar. A preparação antecede M1; não é um módulo adicional.
- Registrar o processo durante o trabalho. Publicação, mensagens externas, commit, push e PR exigem confirmação no escopo correspondente. Capturas e exports exigem consentimento e não podem expor segredos.

## 3. Narrativa consolidada do trabalho registrado

### Preparação — do desafio ao plano de execução

O registro inicial descreve a leitura do challenge, guia de submissão e template, seguida da obtenção dos quatro CSVs operacionais e de uma exploração inicial. O objetivo foi delimitado como solução funcional de priorização com documentação e process log.

A análise inicial passou por depuração antes da construção. Conforme a seção 4.3 do PRD, foram corrigidas interpretações sobre estágio, duração de fechamento, idade do aberto, médias de valores e causas de dados ausentes. A intervenção humana destacada foi exigir um PRD modular antes de avançar para scoring e construção.

O resultado foi um pacote de especificação e dados: PRD, arquitetura proposta, baseline corrigida, instruções ao agente, prompts M1–M6, checklist e modelo de log. Naquele momento, o pacote não continha aplicação pronta. A exploração inicial não substituía a análise reproduzível exigida em M2.

O registro inicial atribui a construção seguinte ao Antigravity IDE por relato do responsável. Os logs locais posteriores identificam Codex como agente utilizado. A narrativa mantém essas atribuições separadas: IDE e agente são papéis distintos, e as fontes não comprovam que toda interação ocorreu em um único ambiente.

### Construção — módulos e resultados relatados

| Etapa | Trabalho registrado | Resultado e fonte |
|---|---|---|
| M1 — Ingestão | Validação dos arquivos, tipos e chaves; normalização `GTXPro` → `GTX Pro`; joins à esquerda sem eliminar contas ausentes. | 8.800 IDs, 2.089 abertos, 1.425 contas ausentes preservadas e 1.480 aliases identificados. [Log M1](../process-log/M1-ingestao.md). |
| M2 — Análise | EDA reproduzível com referência declarada, separação de abertos/fechados e médias Won distintas das médias dos fechados. | 6.711 fechados, 4.238 Won e win rate descritivo aproximado de 63,15%; saída em `outputs/m2_eda.json`; `6 passed`. [Log M2](../process-log/M2-analise.md). |
| M3 — Scoring | Aprovação registrada de `heuristic-v1`, configuração versionada e motor independente da UI. | 2.089 abertos pontuados, 1.589 scores 70 e 500 scores 40; avisos em 1.588 linhas; `10 passed`. [Log M3](../process-log/M3-scoring.md). |
| M4 — Interface | Filtros, fila, detalhe e estados vazios; depois dashboard BI, gráficos, busca, exportação e tema escuro. | Versão inicial com `14 passed` e inicialização do Streamlit; refinamentos com `15 passed`. [M4 inicial](../process-log/M4-streamlit.md), [refinamento](../process-log/M4-ui-refinement.md), [visual](../process-log/M4-ui-visual.md) e [ajuste final](../process-log/M4-ajuste-final-interface.md). |
| M5 — Validação | Suíte integrada, invariância sob filtros, comparação com preço e revisão de uma versão publicada. | `14 passed` após ajuste do temporário do pytest; HTTP 200 e revisão visual relatados. [Log M5](../process-log/M5-validacao.md). |
| M6 — Documentação | Consolidação de setup, lógica, resultados, limitações e evidências. | O M6 registra `17 passed in 1.86s`, importação do app e a correção de explicabilidade; a organização da submissão continua pendente. [M6](../M6_DOCUMENTACAO_COMPLETA.md). |

As contagens 6 → 10 → 14 → 15 representam a evolução registrada da suíte; não são execuções desta revisão. A ordem das linhas acima representa as dependências dos módulos. Os refinamentos de M4 e as verificações de M5 formam ciclos de revisão, sem uma cronologia completa de todas as interações disponível.

### Erros, correções e contribuição humana

| Tipo | Problema registrado | Correção ou decisão |
|---|---|---|
| Interpretação analítica | Score × preço tratado como receita esperada; duração final ou idade tratadas como inatividade. | Separar prioridade, referência de preço, idade e resultado posterior. Não alegar capacidade preditiva. [PRD, seção 4.3](PRD.md#43-depuração-da-análise-inicial--correções-que-orientam-o-produto). |
| Interpretação analítica | Médias de todos os fechados apresentadas como ticket Won; causa de conta ausente e força do estágio afirmadas sem comprovação. | Recalcular denominadores; manter causas desconhecidas; tratar estágio como escolha comercial. Mesma seção do PRD. |
| Referência temporal | Corte inicial de 30/11/2017 produzia idades negativas. | Adotar 31/12/2017 como convenção de demonstração, sem alegar snapshot oficial. [Dados](DADOS.md). |
| Ambiente | Python indisponível no PATH e instalação com `WinError 5`. | Uso de ambiente virtual no projeto. [M1](../process-log/M1-ingestao.md) e [M2](../process-log/M2-analise.md). |
| Ambiente de testes | Erros de permissão no temporário padrão do pytest. | Reexecução com `--basetemp` no projeto e registro do resultado. [M5](../process-log/M5-validacao.md). |
| Interface | Excesso de texto técnico e cards truncados. | Pedido humano de simplificação, modo escuro e cards maiores. A explicação amigável dos fatores foi reincorporada após a revisão de aceite. [Ajuste final](../process-log/M4-ajuste-final-interface.md) e [correção de explicabilidade](../process-log/M4-explainability-correction.md). |

As contribuições humanas registradas incluem exigir a especificação antes do scoring, escolher Streamlit, aprovar a política e orientar as revisões visuais. São decisões relatadas nas fontes; não foram inventadas novas aprovações nesta consolidação. Não há contagem confiável do total de prompts ou iterações, nem validação comercial com vendedores documentada.

## 4. Procedimento único para execução e continuidade

Em cada módulo, repetir este ciclo: **definir objetivo e contrato → instruir a IA → revisar o artefato → executar verificações → corrigir → registrar evidências e decisão → encerrar para revisão**. A pessoa responsável aprova escolhas de produto e negócio; a IA prepara, implementa, verifica e relata limites.

### Preparação — enquadrar antes de implementar

Ler `START_HERE.md`, `AGENTS.md`, PRD, arquitetura, dados, scoring, decisões e referências oficiais locais. Resumir problema, usuário, escopo, dados disponíveis, exclusões, pendências e critérios de sucesso. Classificar cada conclusão como observação, hipótese ou decisão comercial. Produzir PRD e plano modular para revisão. Não tratar a escolha da tecnologia como aprovação de pesos.

### M1 — Ingestão e qualidade

**Entrada:** quatro CSVs operacionais e dicionário auxiliar `metadata.csv`.

**Executar:** validar arquivos, colunas, tipos e chaves; preservar `product_raw`; normalizar o alias somente na preparação; fazer left joins `many_to_one`; diagnosticar ausências e falhas de correspondência.

**Entregar e verificar:** [ingestão](../src/ingest.py), [testes](../tests/test_ingest.py), diagnóstico e campos documentados. Reconciliar 8.800 IDs únicos, 2.089 abertos e contas ausentes preservadas; verificar alias e erros legíveis para arquivos/colunas ausentes. Executar os testes e registrar a saída real. Encerrar para revisão antes de M2. [Prompt M1](../prompts/01-M1-ingestao.md).

### M2 — Análise reproduzível

**Entrada:** dados preparados e `reference_date=2017-12-31`.

**Executar:** separar abertos e fechados; recalcular estágios, ausências, idade conhecida e valores com denominadores explícitos. Distinguir médias Won de médias entre todos os fechados. Não usar duração final para estimar inatividade nem associação para afirmar causalidade. Para outro corte, selecionar explicitamente apenas resultados já conhecidos naquele instante.

**Entregar e verificar:** [análise](../src/analyze.py), [testes](../tests/test_analyze.py), [relatório derivado](../outputs/m2_eda.json), sinais aceitos/rejeitados e proposta completa de política. Reconciliar a baseline, verificar ausência de idades negativas no corte demonstrativo e restrições temporais. Submeter a política à aprovação antes de M3. [Prompt M2](../prompts/02-M2-analise.md).

### M3 — Política e motor de prioridade

**Entrada:** saída de M2 e aprovação explícita registrada. A aprovação histórica de `heuristic-v1` já consta nos logs; esta consolidação não a reabre. Mudanças de fatores, pesos, faixas ou desempate exigem nova decisão.

**Política registrada:** base 10; `Engaging +60 = 70`; `Prospecting +30 = 40`; faixa 0–100. Somente estágio contribui pontos. Ausências geram avisos neutros. Ordenação por score decrescente, preço de catálogo decrescente com ausentes por último e `opportunity_id` crescente.

**Entregar e verificar:** [configuração](../config/scoring_policy.json), [motor](../src/scoring.py) e [testes](../tests/test_scoring.py). Produzir por aberto: ID, score, fatores, avisos, versão, referência e rank. Verificar finitude, reconciliação de contribuições, determinismo, desempates, preservação de missing e ausência de campos futuros. Se a política usar clipping, a explicação deve reconciliar também o ajuste de limite. Comparar descritivamente com preço e estágio, sem alegar ganho de conversão. Encerrar para revisão antes de M4. [Prompt M3](../prompts/03-M3-scoring.md).

### M4 — Experiência do vendedor

**Entrada:** fila pontuada e contexto comercial preparado.

**Executar:** construir filtros combináveis, fila de abertos, detalhe por ID, avisos e estados vazios. A interface consome as camadas próprias; pode associar contexto preparado à fila, sem duplicar a lógica de negócio. Validar o fluxo **selecionar carteira → consultar fila → abrir oportunidade → compreender prioridade → decidir manualmente**.

**Entregar e verificar:** [app](../app.py), [filtros](../src/filters.py) e [testes](../tests/test_filters.py). Iniciar Streamlit e revisar o fluxo no navegador quando disponível. Confirmar score e rank invariáveis sob filtros, leitura das ausências e motivo compreensível da prioridade. Uma mudança visual que retire informação exigida deve gerar revisão explícita dos requisitos e do aceite. Encerrar para revisão antes de M5. [Prompt M4](../prompts/04-M4-streamlit.md).

### M5 — Validação integrada da versão final

**Entrada:** M1–M4 e identificação da versão a verificar.

**Executar:** instalação seguindo o setup, suíte completa e revisão real da interface. Cobrir integridade, ausências, dados desconhecidos, pontuação, contribuições, limites, empates, estabilidade, filtros e restrições temporais. Comparar com rankings simples e registrar também quando forem equivalentes.

**Entregar e verificar:** evidências de AC01–AC09, com falhas, correções e limitações. Separar resultado de testes, importação, inicialização do servidor, resposta HTTP e jornada visual. Após mudanças de UI, revisar os critérios afetados na nova versão. M5 prepara o aceite técnico e de uso; AC10 é concluído em M6. Não afirmar ganho comercial. Encerrar para revisão antes de M6. [Prompt M5](../prompts/05-M5-validacao.md).

### M6 — Documentação e preparação da submissão

**Entrada:** artefatos verificados, decisões e evidências acumuladas.

**Executar:** preencher o README preservando os títulos do [template oficial](../references/submission-template.md):

- Sobre mim; Executive Summary.
- Solução → Abordagem; Resultados / Findings; Recomendações; Limitações.
- Process Log — Como usei IA → Ferramentas usadas; Workflow; Onde a IA errou e como corrigi; O que eu adicionei que a IA sozinha não faria.
- Evidências; indicação “Submissão enviada em” com a data efetiva do envio.

Incluir setup, lógica, proveniência e limitações. Usar apenas dados do autor informados e resultados efetivos. Não preencher a data de envio como se a submissão já tivesse ocorrido.

**Entregar e verificar:** pacote em `submissions/<identificador>/` no repositório de destino, com `README.md`, `solution/`, `process-log/` e `docs/` quando necessário. Levar dados/licença/proveniência ou instruções reproduzíveis de obtenção. Reexecutar setup, testes e inicialização após reorganizar; concluir AC10 e revisar os critérios afetados. Manter alterações do PR exclusivamente na pasta pessoal. Preparar o resultado revisável antes de solicitar autorização para commit, push e PR. [Prompt M6](../prompts/06-M6-entrega.md) e [CONTRIBUTING](../references/CONTRIBUTING.md).

## 5. Como registrar evidências e decisões

Usar o [modelo de log](../process-log/TEMPLATE.md) em cada etapa, com:

1. Objetivo, entrada e critério de conclusão.
2. Ferramenta/agente efetivamente utilizado e prompt real ou referência à conversa. Não reconstruir um prompt como se fosse transcrição.
3. Arquivos produzidos e identificação da versão verificada; hash local quando não houver commit.
4. Comando executado, resultado, data/hora quando disponíveis e alcance da verificação. Se a saída não foi preservada, declarar.
5. Falha observada, correção aplicada e verificação posterior.
6. Decisão humana, responsável e evidência da aprovação, distinguindo proposta de aprovação.
7. Pendências, limitações e decisão de passagem para a etapa seguinte.

Na seção “Ferramentas de IA”, separar agente de ambiente e dependências: Codex é o agente identificado nos logs; Antigravity é o IDE citado no relato inicial; PowerShell, pandas, pytest, Streamlit e Plotly cumprem funções de execução, dados, testes e interface. Não são evidência de uso de um modelo específico. GitHub e hospedagem são serviços de publicação.

A narrativa escrita é formato aceito pelo guia de submissão; screenshots não são obrigatórios. Quando houver captura ou export, obter consentimento e remover segredos. M6 consolida e aponta para registros existentes; não cria retroativamente evidências ausentes.

## 6. Divergências identificadas e tratamento proposto

| Divergência ou lacuna | Tratamento no processo único |
|---|---|
| README, START_HERE, PRD, arquitetura e outros textos ainda descrevem o kit inicial. | Preservar esse contexto como histórico e distinguir especificação de estado posterior. A sincronização dos documentos operacionais permanece como ação de continuidade; os originais não foram reescritos nesta análise. |
| O cabeçalho do M6 passou a informar Felipe Navaar e LinkedIn durante esta análise, mas recomendações e checklist ainda os tratam como ausentes. | Considerar os campos do cabeçalho como informados e sincronizar as pendências em atualização posterior. O identificador da pasta pessoal permanece não definido. A alteração do M6 foi detectada por hash e não foi realizada por esta tarefa. |
| `DECISOES.md` registra aprovação e ainda lista pesos pendentes; `SCORING.md` mantém o título de política pendente. | Considerar `heuristic-v1` como aprovação histórica registrada em M3, sem apresentar isso como nova validação comercial. Em atualização posterior, retirar a pendência superada e vincular a aprovação à evidência original se disponível. |
| A versão escura inicialmente removeu explicações técnicas, mas o challenge, PRD e AC09 exigem entendimento da prioridade pelo vendedor. | Correção concluída: a ficha da oportunidade agora exibe os fatores calculados em linguagem comercial, mantendo a interface limpa e o aceite de explicabilidade demonstrável. O histórico da decisão visual permanece registrado em `process-log/M4-explainability-correction.md`. |
| O checklist marca AC01–AC09, mas também contém texto antigo dizendo que testes são metas e cenários “a testar”. | Não usar checkboxes isolados como prova. Associar cada critério à versão, evidência e limite; reabrir somente critérios afetados ou sem comprovação suficiente. |
| M6 reúne testes, importação, HTTP 200 e revisão visual como validação abrangente. | Relatar cada verificação separadamente. HTTP 200 não comprova a versão publicada; importar não percorre a jornada. A revisão visual relatada com fatores não comprova a interface escura posterior, que os retirou. |
| Publicação visual tem log com autorização e commit; outro commit final é citado somente no M6. | O [log de publicação](../process-log/M4-publicacao-visual.md) registra autorização e commit `64fd8b1…`; a publicação do tema final `d00500a…` tem rastreabilidade menos detalhada. Isso é lacuna de evidência, não prova de publicação sem autorização. Vincular cada publicação a versão, escopo autorizado e verificação. |
| A política usa apenas estágio e preço/ID para desempate. | Explicitar a simplicidade: a ordem é equivalente à ordenação pelo estágio nessa precedência, depois preço e ID. As 2.069 posições diferentes frente ao preço puro, relatadas em M5, não comprovam superioridade frente ao estágio nem impacto comercial. |
| Contratos de clipping e de cortes históricos alternativos são mais amplos que a evidência disponível. | A leitura do motor indica que clipping efetivo não reconciliaria as contribuições originais; 40/70 não acionam o limite. A análise usa o corte para idade, mas não filtra fechados por `close_date <= corte`. Antes de ampliar esses usos, corrigir e testar os contratos. Não inferir vazamento no corte padrão apenas dessa limitação. |

## 7. Aceite e próximos passos

| Critério | Estado documental consolidado | Ação necessária para encerramento |
|---|---|---|
| AC01–AC02 — Dados e joins | Evidências narradas em M1/M2 e testes presentes. Integridade dos CSVs verificada nesta consolidação. | Vincular as execuções à versão final empacotada. |
| AC03–AC05 — Score, explicação e ranking | Política, motor e resultados registrados; fronteiras/clipping e alguns cenários previstos carecem de comprovação específica. | Conferir cobertura do contrato e registrar comparação com estágio e preço. |
| AC06–AC07 — Filtros e temporalidade | Testes e verificações registrados; corte padrão declarado. | Confirmar a versão empacotada; não estender conclusões para retrospectivas com cortes anteriores. |
| AC08 — Execução | Instalação, testes e inicialização em etapas anteriores são relatados. | Reproduzir setup e execução após reorganização e preservar saídas. |
| AC09 — Usabilidade e explicação | Há revisão de uma versão anterior; a mudança final retirou a explicação exigida. | Resolver o conflito de requisito e revisar a jornada na versão final identificada. |
| AC10 — Entrega | Pendente conforme M6 e checklist; nome e LinkedIn já constam no cabeçalho atualizado. | Definir identificador, montar pasta pessoal, validar instruções e obter autorização para envio. |

Ordem de continuidade recomendada:

1. **Explicabilidade e aceite:** resolvidos com a exibição dos fatores calculados na ficha da oportunidade; manter a linguagem comercial e a rastreabilidade técnica sem reintroduzir jargão na interface.
2. **Sincronizar documentação e evidências:** atualizar estados antigos, conferir contratos ainda sem comprovação e relacionar testes/revisão visual à versão final.
3. **Preparar a submissão:** usar os dados do autor já informados no M6, obter o identificador da pasta pessoal, organizar o pacote e reproduzir a execução. Sincronizar os itens de nome/LinkedIn que ainda constam como pendentes no checklist antigo.
4. **Enviar após confirmação:** seguir fork/branch/PR conforme CONTRIBUTING, um PR por pessoa e título `[Submission] Nome — Challenge 003`. Publicação da demonstração e submissão ao challenge são entregas distintas.

**Estado desta consolidação:** processo documental unificado produzido; nenhuma fonte anterior foi editada por esta tarefa; nenhuma alteração no aplicativo, na política ou nos dados. A conclusão da submissão e da validação comercial não é afirmada.

## 8. Referências de execução

- [Instruções do projeto](../AGENTS.md) e [entrada inicial](../START_HERE.md).
- [PRD](PRD.md), [arquitetura](ARQUITETURA.md), [dados](DADOS.md), [scoring](SCORING.md), [decisões](DECISOES.md) e [aceite](ACEITE.md).
- [Challenge](../references/challenge.md), [guia de submissão](../references/submission-guide.md), [template](../references/submission-template.md) e [regras de contribuição](../references/CONTRIBUTING.md).
- [Registro desta consolidação e verificações](../process-log/CONSOLIDACAO-PROCESSO.md).
