# PRD — Lead Scorer

**Challenge 003 · Vendas / RevOps**  
**Versão:** 0.2 — kit de recriação; Streamlit confirmado, política de scoring pendente  
**Data:** 20/10/2026  
**Status:** EDA inicial executada; sistema e scoring ainda não implementados. Este PRD orienta a construção, não substitui o software exigido pelo desafio.

## 1. Executive Summary

O desafio pede uma solução funcional para orientar a priorização de oportunidades por vendedores, substituindo decisões exclusivamente intuitivas por critérios transparentes. A análise inicial identificou 8.800 oportunidades, das quais 2.089 estão abertas e são o universo operacional do MVP. Propomos uma aplicação simples, com pipeline ordenado, score explicável e filtros comerciais, apoiada em processamento reproduzível dos quatro CSVs. A recomendação é separar análise, preparação de dados, scoring, interface e validação em módulos, sem confundir hipóteses comerciais com resultados comprovados.

## 2. Problema, público e objetivo

**Problema:** vendedores não dispõem de uma fila consistente e explicável para escolher quais oportunidades trabalhar primeiro.

**Usuário principal:** vendedor, que precisa responder: “Quais deals devo revisar primeiro e por quê?”.  
**Usuários secundários:** manager e RevOps, para consultar carteiras e compreender critérios e limitações.

**Objetivo do MVP:** permitir selecionar a carteira, visualizar oportunidades abertas priorizadas e inspecionar os fatores que compõem a pontuação.

**Sucesso da entrega:** software executável, usando os dados reais, com priorização além de valor bruto, explicações auditáveis, instruções de execução e process log. Aumento de conversão e receita são resultados futuros desejados, não comprováveis com esta entrega offline.

## 3. Escopo

### Obrigatório no desafio
- Solução que rode, não apenas mockup, notebook ou documento.
- Uso dos dados reais do dataset indicado.
- Lógica de scoring/priorização além de ordenar por valor.
- Explicação compreensível do score por oportunidade.
- Documentação de setup, lógica e limitações.
- Process log com evidências de uso de IA.

### Escopo proposto para o MVP
- Aplicação web local, de uma tela principal e um painel de detalhes.
- Importação dos quatro CSVs, sem integração com CRM.
- Histórico Won/Lost para análise; somente Engaging/Prospecting na fila operacional.
- Filtros por vendedor, manager e região — bônus no desafio, incluído na proposta.
- Score heurístico versionado, avisos de dados ausentes e desempate determinístico.
- Valor de referência do catálogo exibido separadamente do score.

### Fora do MVP
- Autenticação e controle de acesso de produção.
- Escrita no CRM, disparos de mensagens e automações comerciais.
- Previsão probabilística calibrada, ML complexo e recomendação gerada por LLM.
- Estimativa de quantidade vendida, esforço comercial ou última atividade: campos não disponíveis.
- Deploy público obrigatório; execução local reproduzível atende ao escopo proposto.

**Stack confirmada pelo usuário:** Python + pandas + Streamlit, com motor de regras independente da interface. Streamlit é a escolha deste projeto, não exigência do repositório.

## 4. Abordagem e base analítica

### 4.1 Fontes e relações

| Fonte | Registros observados | Chave | Uso |
|---|---:|---|---|
| accounts.csv | 85 | account | Contexto da conta |
| products.csv | 7 | product | Série e preço de referência |
| sales_teams.csv | 35 | sales_agent | Vendedor, manager, região |
| sales_pipeline.csv | 8.800 | opportunity_id | Tabela central das oportunidades |

Joins à esquerda a partir do pipeline, preservando todas as oportunidades. O download também contém metadata.csv, auxiliar de interpretação, não uma quinta tabela operacional.

### 4.2 Resultados observados na EDA
- Won: 4.238; Lost: 2.473; Engaging: 1.589; Prospecting: 500.
- Win rate entre os 6.711 fechados: aproximadamente 63,1%.
- Nenhum opportunity_id duplicado na verificação realizada.
- 1.480 linhas usam `GTXPro`, enquanto o catálogo usa `GTX Pro`.
- 1.425 oportunidades não têm account; todas estão abertas.
- As 500 oportunidades Prospecting não têm engage_date.
- close_value e close_date estão ausentes nas 2.089 oportunidades abertas.
- O histórico mostra variação descritiva por vendedor e duração de fechamento. Isso não estabelece causalidade nem capacidade preditiva.
- Setor, região e porte apresentaram diferenças descritivas pequenas; não justificam pesos automáticos.

**Evidências neste kit:** CSVs em `data/raw/`, baseline recalculada em `docs/EDA_BASELINE.json`. A EDA e o script anteriores não foram incluídos, pois contêm inferências superadas pela seção 4.3. Recriar a análise no M2.

### 4.3 Depuração da análise inicial — correções que orientam o produto

| Afirmação inicial | Tratamento correto no PRD |
|---|---|
| Stage é um sinal empiricamente forte | Engaging acima de Prospecting é hipótese comercial; não há histórico de transições suficiente para medir a conversão por estágio inicial. |
| Duração de fechamento mede urgência do aberto | Duração até Won/Lost é conhecida após o resultado. Não aplicar suas faixas diretamente à idade de um aberto. |
| Dias desde engage_date indicam inatividade | Indicam idade desde engajamento, não tempo sem contato. Não mostrar “parado” sem dados de atividade. |
| Ticket Won de GTK 500 é US$ 16.024 e MG Special US$ 36 | Esses números eram médias de close_value entre todos os fechados, incluindo Lost com zero, não tickets médios apenas dos ganhos. |
| score × sales_price é valor esperado | Score heurístico não é probabilidade calibrada; o produto é, no máximo, um índice de prioridade ponderado por valor, não previsão de receita. |
| Ausência de account ocorre porque a conta é preenchida depois | Só foi observado que a ausência se concentra nos abertos. A causa não foi demonstrada. |
| Alternância mensal comprova artefato sintético | É um padrão suspeito, mas sua causa não foi comprovada. Mês futuro de fechamento não será usado. |
| Data de referência 30/11/2017 | A EDA utilizou esse corte incorretamente e gerou idades negativas. O maior close_date observado é 31/12/2017. Usar essa data como corte de demonstração declarado, sem alegar que é um snapshot oficial. |

As conclusões conflitantes da EDA inicial ficam superadas por esta seção. Corrigir o script e regenerar a EDA é pré-requisito da construção, não algo já realizado neste documento.

## 5. Módulos e contratos

### M1 — Ingestão e qualidade
**Entrada:** quatro CSVs originais.  
**Responsabilidades:** validar colunas, tipos, chaves e datas; normalizar `GTXPro` para `GTX Pro`; fazer joins many-to-one; preservar campos originais e sinalizar ausências.  
**Saída:** tabela enriquecida, dicionário de campos e diagnóstico de qualidade.  
**Aceite:** manter 8.800 IDs únicos após os joins; reconciliar 2.089 abertos; zerar falhas de correspondência de produto após o alias; não descartar oportunidades sem conta. Arquivo/coluna obrigatória ausente deve gerar erro legível.

### M2 — Análise reproduzível
**Entrada:** tabela preparada e data de referência declarada.  
**Responsabilidades:** separar histórico e fila aberta; regenerar EDA corrigida; calcular estatísticas com denominadores explícitos; distinguir associação, hipótese e evidência.  
**Saída:** diagnóstico reproduzível e catálogo de sinais aprovados/rejeitados.  
**Aceite:** médias Won separadas das médias entre fechados; nenhuma idade negativa no corte da demonstração; histórico final de fechamento não pode ser entrada do score de abertos. Não usar estatísticas futuras em eventual avaliação temporal.

### M3 — Scoring explicável
**Entrada:** oportunidades abertas, política de scoring e contexto histórico permitido.  
**Responsabilidades:** calcular score, fatores, avisos e ordenação de forma determinística. Regras isoladas da UI e identificadas por versão.  
**Saída por deal:** opportunity_id, score de prioridade 0–100, fatores com contribuição, avisos, versão da regra, data de referência e posição na fila.  
**Aceite:** todo deal aberto recebe saída válida; contribuições reconciliam com o score exibido; dados ausentes não geram NaN nem eliminação silenciosa; a mesma entrada e política produzem a mesma saída.

### M4 — Experiência do vendedor
**Entrada:** fila pontuada e dimensões comerciais.  
**Responsabilidades:** filtros combináveis; lista priorizada; detalhe “por que esta prioridade?”; avisos de qualidade e legenda do score.  
**Saída:** fila acionável para revisão humana, sem executar ações externas.  
**Aceite:** vendedor consegue filtrar sua carteira, consultar os primeiros deals e explicar a posição de um deles usando o painel. Filtro vazio mostra mensagem clara. Filtro modifica a visualização, não a pontuação do mesmo deal.

### M5 — Testes e validação
**Entrada:** M1–M4 e cenários controlados.  
**Responsabilidades:** testar integridade, regras, filtros e execução limpa; comparar ranking com alternativas simples; registrar falhas e correções.  
**Saída:** testes executáveis e evidências dos resultados.  
**Aceite:** todos os critérios da seção 9 atendidos. Não reivindicar ganho de conversão sem avaliação apropriada.

### M6 — Documentação e submissão
**Entrada:** aplicação verificada, decisões e evidências de cada módulo.  
**Responsabilidades:** README no template oficial, setup, lógica, limitações e process log; organizar tudo na pasta de submissão.  
**Saída:** pacote pronto para revisão e posterior PR.  
**Aceite:** outra pessoa consegue executar seguindo o README; evidências reais vinculadas; nenhum arquivo fora da pasta pessoal alterado no PR. Publicação depende de confirmação posterior.

## 6. Política de scoring — limites e decisões pendentes

**Definição:** score heurístico de prioridade, não percentual de chance de fechamento. Pesos e thresholds serão definidos e documentados na etapa M3, após a correção da análise. Não há fórmula aprovada neste PRD.

| Componente | Diretriz proposta | Condição de uso |
|---|---|---|
| Stage | Considerar maturidade comercial | Explicitar que é uma regra de negócio, não taxa de conversão comprovada. |
| Idade desde engage_date | Mostrar como contexto no MVP | Só pontuar se existir justificativa validada; não aplicar penalidade automática por “inatividade”. |
| Histórico do vendedor | Avaliar como sinal opcional | Exigir tamanho de amostra, suavização e corte temporal; não interpretar como qualidade causal do vendedor. |
| Conta/setor/porte/região | Contexto e filtros | Peso zero por padrão até surgir evidência suficiente. Conta ausente não equivale a conta ruim. |
| Preço do produto | Exibir potencial de referência | sales_price não é valor esperado nem valor total garantido do deal. Não usar close_value futuro como entrada. |

**Proposta de ordenação inicial:** score decrescente; preço de referência como desempate; opportunity_id para estabilidade final. É uma decisão proposta para evitar que o ticket domine todas as prioridades. Se for aprovado um ranking ponderado por valor, ele terá nome, fórmula e limitações próprios, sem ser chamado de receita esperada.

**Fallbacks:** dados ausentes geram aviso e tratamento neutro documentado; vendedor sem histórico usa referência global quando a regra histórica existir; produto desconhecido gera aviso explícito e preço indisponível, nunca preço zero inventado.

## 7. Jornada e requisitos de interface

1. Abrir o app e visualizar fonte, data de referência e aviso de demonstração offline.
2. Selecionar vendedor e, opcionalmente, manager/região.
3. Visualizar opportunities abertas em ordem de prioridade.
4. Abrir uma oportunidade e consultar fatores do score e dados ausentes.
5. Decidir manualmente qual deal revisar primeiro.

**Campos mínimos da lista:** posição, oportunidade, conta ou “não informada”, vendedor, produto, estágio, score e preço de referência.  
**Detalhes:** contribuições da regra, idade quando disponível, avisos e legenda de limitações.  
**Não inferir:** última interação, urgência real, chance calibrada ou próxima ação personalizada sem dados que sustentem essas informações.

## 8. Sequência de criação e dependências

| Ordem | Etapa | Depende de | Evidência para avançar |
|---|---|---|---|
| 0 | Aprovar este PRD e o recorte do MVP | — | Escopo e pendências aceitos |
| 1 | M1: preparar dados | PRD | Reconciliação de registros e joins |
| 2 | M2: corrigir e reproduzir EDA | M1 | Estatísticas corrigidas e sinais classificados |
| 3 | Definir política e construir M3 | M2 | Regras, pesos e casos explicados |
| 4 | Construir M4 | Contrato de M3 | Jornada executável com dados reais |
| 5 | Executar M5 | M1–M4 | Saída de testes e revisão da interface |
| 6 | Consolidar M6 | M5 | README, setup, limitações e evidências |
| 7 | Revisar e enviar PR | Pacote validado + confirmação | PR conforme CONTRIBUTING |

O process log acompanha todas as etapas, não é escrito apenas no final. O orçamento de 4–6 horas é a orientação do desafio, não promessa de prazo. Não há cronograma ou automação criado por este PRD.

## 9. Critérios de aceite do MVP

- **AC01 — Dados:** quatro tabelas reais carregadas; 8.800 oportunidades reconciliadas; apenas 2.089 abertas na fila padrão.
- **AC02 — Joins:** alias de produto resolvido, sem multiplicação de IDs; ausência de conta preservada e sinalizada.
- **AC03 — Regras:** score entre 0 e 100, finito, determinístico e com composição auditável.
- **AC04 — Explicação:** soma de base/contribuições e eventuais limites explica o resultado; score não é apresentado como probabilidade.
- **AC05 — Ranking:** não equivale a mera ordenação por preço; política e desempates estão documentados e testados com cenários controlados.
- **AC06 — Interface:** filtros por vendedor/manager/região funcionam em conjunto; vazio e dados ausentes têm estados legíveis.
- **AC07 — Temporalidade:** corte declarado, sem idades negativas; close_date/close_value futuros e duração final não entram no scoring operacional.
- **AC08 — Execução:** executar instalação, testes e inicialização a partir das instruções, registrando resultados reais.
- **AC09 — Usabilidade:** revisão manual do fluxo de seleção → fila → explicação, sem depender de leitura do código.
- **AC10 — Entrega:** README no template oficial; setup, lógica, limitações e process log presentes; alterações confinadas à pasta pessoal.

**Validação analítica adicional:** comparar com ordenação por estágio e por preço para compreender diferenças do ranking. Se houver avaliação de acerto histórico, reconstruir features no instante da decisão e separar treino/avaliação temporalmente. Uma comparação em toda a base fechada não comprova desempenho futuro.

## 10. Recomendações e limitações

**Prioridade 1:** corrigir a EDA antes de transformar correlações em regras.  
**Prioridade 2:** aprovar um scoring mínimo, transparente e modular.  
**Prioridade 3:** construir primeiro o fluxo usado pelo vendedor; evitar infraestrutura desnecessária.

**Limitações conhecidas:** não há trilha de mudanças de estágio, histórico de atividades, data de criação para Prospecting ou quantidade de unidades. O corte de demonstração é uma convenção explícita, não snapshot confirmado. As associações da EDA não são evidência causal. Não existe modelo calibrado nem validação comercial com vendedores. Pesos e política final de ranking aguardam aprovação; não bloquear a definição dos contratos dos módulos por essas escolhas.

## 11. Formato de entrega exigido pelo contexto

Estrutura futura conforme CONTRIBUTING (não criada por este PRD):

```text
submissions/seu-nome/
├── README.md              # template oficial preenchido
├── solution/              # app, motor, dados ou instruções de obtenção, testes
├── process-log/           # narrativa e evidências reais de uso de IA
└── docs/                  # PRD e análise corrigida, se incluídos
```

**README final:** Sobre mim; Executive Summary (3–5 frases); Solução → Abordagem, Resultados/Findings, Recomendações e Limitações; Process Log → Ferramentas usadas, Workflow, Onde a IA errou e como corrigi, O que eu adicionei; Evidências; data da submissão. Acrescentar setup e lógica do scoring de forma clara.

**Process log por etapa:** objetivo → instrução dada à IA → resultado → verificação → erro/correção → decisão humana → link da evidência. Não inventar conversas, ferramentas, testes, capturas ou intervenções humanas. Decisão já observada: o usuário interrompeu a evolução para scoring/stack e exigiu PRD modular antes da construção.

**PR futuro:** fork, branch `submission/seu-nome`, uma pasta pessoal e um PR por pessoa; título `[Submission] Nome — Challenge XXX`. Não alterar arquivos fora de `submissions/seu-nome/`.

## 12. Referências

- [Challenge 003 — Lead Scorer](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/challenges/build-003-lead-scorer/README.md)
- [Guia de Submissão](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/submission-guide.md)
- [Template de Submissão](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/templates/submission-template.md)
- [CONTRIBUTING — instruções e regras do PR](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/CONTRIBUTING.md)
- [Dataset — CRM Sales Predictive Analytics](https://www.kaggle.com/datasets/agungpambudi/crm-sales-predictive-analytics)

