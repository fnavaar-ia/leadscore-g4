# Submissão — Felipe Navaar — Challenge 003

> Documento independente de documentação final. Ele foi criado separadamente dos documentos anteriores do projeto e não substitui `README.md`, `docs/PRD.md`, `docs/ACEITE.md` ou os registros individuais de `process-log/`.

## Sobre mim

- **Nome:** Felipe Navaar
- **LinkedIn:** https://www.linkedin.com/in/navaar-figueiredo-584500271/
- **Challenge escolhido:** Challenge 003 — Lead Scorer.
- **Área:** Vendas / Revenue Operations.
- **Aplicação pública:** [LeadScore G4 no Streamlit](https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/).
- **Repositório da implementação:** [fnavaar-ia/leadscore-g4](https://github.com/fnavaar-ia/leadscore-g4).

---

## Executive Summary

O LeadScore G4 é um dashboard Streamlit para ajudar times comerciais a organizar e revisar uma carteira histórica de oportunidades abertas. A solução carrega quatro tabelas CSV reais, preserva registros sem conta, trata inconsistências conhecidas, prepara uma fila de 2.089 oportunidades abertas e apresenta essa fila em um dashboard interativo. A priorização é determinística, versionada e explicável: a ficha de cada oportunidade mostra os fatores calculados pelo backend em linguagem comercial. O resultado é uma aplicação publicada, com filtros, visualizações interativas, detalhe de oportunidade, análise de cobertura dos dados e exportação da seleção em CSV.

O projeto foi construído modularmente em seis preocupações: ingestão, análise, priorização, filtros, interface e validação. A versão atual foi validada com 17 testes automatizados aprovados, importação real do app e verificação HTTP da aplicação pública. A principal recomendação para evolução é conectar o produto a uma fonte operacional com histórico de atividades e transições de estágio, preservando a transparência e realizando uma avaliação temporal antes de transformar o índice atual em uma ferramenta de decisão comercial de produção.

---

## Solução

### Visão geral do produto

O produto é um painel para responder rapidamente a quatro perguntas:

1. Quantas oportunidades estão na seleção atual?
2. Como a carteira está distribuída por estágio, região, manager e produto?
3. Quais oportunidades merecem ser revisadas primeiro?
4. Quais dados estão faltando para uma análise mais completa?

O app não executa ações no CRM, não envia mensagens, não faz autenticação de produção e não depende de API externa ou modelo de IA durante o runtime. Ele lê os CSVs locais do projeto, processa os dados em memória e disponibiliza uma visão interativa para revisão humana.

### Requisitos atendidos

- Aplicação executável em Streamlit.
- Uso dos dados reais presentes em `data/raw/`.
- Priorização determinística das oportunidades abertas.
- Filtros por vendedor, manager, região, estágio e produto.
- Busca textual por oportunidade, conta, produto ou vendedor.
- Faixa de prioridade ajustável.
- Tabela com posição, prioridade, contexto comercial e preço de catálogo.
- Visão individual de uma oportunidade.
- Gráficos interativos com hover e exploração visual.
- Indicadores de cobertura dos dados.
- Exportação da seleção filtrada em CSV.
- Testes automatizados de ingestão, análise, priorização e filtros.
- Processo registrado em `process-log/`.
- Aplicação publicada no Streamlit.

### Abordagem

O desenvolvimento seguiu a sequência definida no kit do desafio:

```text
M1 — Ingestão e qualidade
        ↓
M2 — Análise reproduzível
        ↓
M3 — Política e motor de priorização
        ↓
M4 — Interface Streamlit e experiência do vendedor
        ↓
M5 — Testes e validação integrada
        ↓
M6 — Documentação e preparação da submissão
```

A separação foi importante porque impediu que a interface tomasse decisões de negócio diretamente. O app consome a saída das camadas de ingestão, priorização e filtros; ele não recria joins nem possui uma fórmula independente escondida dentro dos componentes visuais.

### Arquitetura da solução

```text
data/raw/*.csv
      │
      ▼
src/ingest.py
  valida schemas, tipos, chaves e joins
      │
      ▼
src/analyze.py
  calcula diagnóstico histórico reproduzível
      │
      ├──────────────► outputs/m2_eda.json
      │
      ▼
src/scoring.py + config/scoring_policy.json
  seleciona abertos, calcula prioridade e ranking
      │
      ▼
src/filters.py
  filtra a fila pronta sem recalcular valores
      │
      ▼
app.py
  KPIs, gráficos, tabela, detalhe, cobertura e exportação
```

### Fontes de dados e proveniência

O dataset utilizado é o **CRM Sales Predictive Analytics**, indicado pelo próprio challenge e declarado como CC0 na especificação fornecida.

Fonte indicada:

- [CRM Sales Predictive Analytics no Kaggle](https://www.kaggle.com/datasets/agungpambudi/crm-sales-predictive-analytics)
- Download indicado pelo kit: `https://www.kaggle.com/api/v1/datasets/download/agungpambudi/crm-sales-predictive-analytics`

Arquivos usados:

| Arquivo | Registros observados | Papel |
|---|---:|---|
| `accounts.csv` | 85 | Contexto das contas |
| `products.csv` | 7 | Catálogo, série e preço de referência |
| `sales_teams.csv` | 35 | Vendedor, manager e escritório regional |
| `sales_pipeline.csv` | 8.800 | Tabela central de oportunidades |
| `metadata.csv` | auxiliar | Dicionário original do dataset |

O pipeline é a tabela central. Os demais arquivos são associados por `account`, `product` e `sales_agent`. A ingestão parte do pipeline e usa `left join`, preservando oportunidades mesmo quando a conta está ausente.

### M1 — Ingestão e qualidade

#### Objetivo

Validar os CSVs originais, preparar os tipos, resolver a diferença conhecida entre `GTXPro` e `GTX Pro`, fazer joins sem multiplicar oportunidades e produzir um diagnóstico de qualidade.

#### Implementação

O módulo `src/ingest.py`:

- Resolve os caminhos a partir da raiz do projeto.
- Lê os CSVs de `data/raw/`.
- Valida colunas obrigatórias.
- Valida chaves únicas nas dimensões.
- Converte datas e campos numéricos.
- Preserva os campos de origem necessários para auditoria.
- Normaliza `GTXPro` para `GTX Pro` somente na camada preparada.
- Usa `validate="many_to_one"` nos joins dimensionais.
- Mantém linhas sem conta.
- Retorna tabela enriquecida e diagnóstico.

#### Evidências observadas

- 8.800 linhas no pipeline.
- 8.800 `opportunity_id` distintos.
- 2.089 oportunidades abertas.
- 1.425 oportunidades sem conta.
- 500 oportunidades `Prospecting` sem `engage_date`.
- 1.480 registros com o alias bruto `GTXPro`.
- Zero produtos sem correspondência após a normalização do alias.

#### Correções durante a etapa

Na primeira verificação, os comandos Python não estavam disponíveis no PATH. Posteriormente foi criado um ambiente virtual dentro do projeto, evitando depender de uma instalação global. Também houve uma tentativa de uso do Git no ambiente em que o executável não estava disponível; isso não impediu a implementação da ingestão.

Registro detalhado: `process-log/M1-ingestao.md`.

### M2 — Análise reproduzível

#### Objetivo

Recalcular a análise exploratória com uma data de referência declarada, separar oportunidades abertas de fechadas e não misturar estatísticas de Won com médias gerais de fechados.

#### Decisões analíticas

- Data de referência demonstrativa: `2017-12-31`.
- O corte é uma convenção de demonstração; não é apresentado como snapshot oficial.
- O universo operacional contém apenas `Engaging` e `Prospecting`.
- `Won` e `Lost` são resultados históricos conhecidos.
- A duração observada em negócios fechados não foi convertida em inatividade de negócios abertos.
- A ausência de `engage_date` não foi convertida em zero.
- Campos de fechamento não foram usados como informação futura para priorizar abertos.

#### Resultados observados

- 8.800 oportunidades no total.
- 2.089 oportunidades abertas.
- 6.711 oportunidades fechadas.
- 4.238 oportunidades Won.
- Win rate descritivo entre os fechados: aproximadamente 63,15%.

O relatório derivado foi escrito em `outputs/m2_eda.json`. O código está em `src/analyze.py` e os cenários estão em `tests/test_analyze.py`.

#### Correções durante a etapa

A instalação direta de pacotes na pasta de usuário falhou com `WinError 5`. A correção foi criar e usar `.venv` no diretório do projeto. Após isso, a análise e os testes foram executados dentro do ambiente virtual.

Registro detalhado: `process-log/M2-analise.md`.

### M3 — Política e motor de priorização

#### Aprovação humana

Antes da implementação, foi apresentada uma proposta de política ao usuário. O usuário aprovou explicitamente a política `heuristic-v1` em 20/10/2026.

#### Fórmula aprovada

A regra operacional é:

```text
prioridade = base + contribuição do estágio
```

Parâmetros:

| Elemento | Valor |
|---|---:|
| Base | 10 |
| `Prospecting` | +30 |
| `Engaging` | +60 |
| `Prospecting` final | 40 |
| `Engaging` final | 70 |
| Faixa permitida | 0 a 100 |

O campo ponderado é somente `deal_stage`. A política está versionada em `config/scoring_policy.json`.

#### Campos contextuais

Os seguintes campos aparecem para consulta, mas não acrescentam pontos diretamente:

- `engage_date`;
- `sales_price`;
- `account`;
- `sector`;
- `employees`;
- `regional_office`;
- `sales_agent`.

O preço de catálogo é usado apenas como desempate entre oportunidades com a mesma prioridade. O segundo desempate é `opportunity_id` em ordem crescente, garantindo estabilidade.

#### Tratamento de ausências

Ausências não eliminam oportunidades e não recebem informação inventada. Elas geram avisos para revisão, com tratamento neutro. Isso se aplica principalmente a:

- conta ausente;
- data de engajamento ausente;
- preço de catálogo ausente.

#### Proteções temporais

`close_value`, `close_date` e duração final de fechamento não entram na priorização operacional de oportunidades abertas. Esses campos representam informação posterior ao momento de decisão e poderiam causar vazamento temporal.

#### Limites de interpretação

O índice é uma prioridade operacional baseada em regra de negócio. Não deve ser interpretado como probabilidade calibrada de fechamento, previsão de receita ou garantia de resultado comercial. O preço de catálogo também não representa receita esperada.

O motor está em `src/scoring.py` e é coberto por `tests/test_scoring.py`.

#### Resultados reais

- 2.089 linhas abertas pontuadas.
- 2.089 IDs únicos na fila.
- Valores finitos entre 40 e 70.
- 1.589 oportunidades `Engaging` com prioridade 70.
- 500 oportunidades `Prospecting` com prioridade 40.
- 1.588 linhas com algum aviso de dados ausentes.
- Nenhuma oportunidade descartada por ausência de conta.

Registro detalhado: `process-log/M3-scoring.md`.

### M4 — Interface Streamlit

#### Primeira versão funcional

A primeira versão do app entregou a jornada mínima:

```text
abrir app → escolher filtros → ver fila → selecionar oportunidade → consultar detalhes
```

Ela foi criada com `app.py`, `src/filters.py` e `tests/test_filters.py`. A fila mostrava as oportunidades abertas em posição global, preservando o ranking original mesmo depois de aplicar filtros.

#### Filtros

Os filtros atuais permitem combinar:

- vendedor;
- manager;
- região;
- estágio;
- produto;
- faixa de prioridade;
- busca por oportunidade, conta, produto ou vendedor.

O estado vazio é tratado com uma mensagem clara. O botão de limpeza restaura os filtros da sessão.

#### Dashboard BI

Depois da primeira versão, a interface foi refinada para uma experiência mais próxima de BI:

- Cabeçalho visual com identidade do produto.
- Cards executivos no topo.
- Gráficos interativos com Plotly.
- Distribuição por estágio.
- Distribuição por região.
- Ranking de managers.
- Distribuição por produto.
- Tabela de oportunidades com limite inicial de 100 linhas.
- Opção para mostrar toda a seleção.
- Exportação dos dados filtrados em CSV.
- Ficha individual da oportunidade.
- Medidor visual de prioridade.
- Motivos da prioridade apresentados a partir dos fatores calculados pelo backend.
- Aba de cobertura dos campos.

#### Tema final

Após a revisão visual, a interface foi alterada para modo escuro:

- Fundo principal escuro.
- Sidebar escura com contraste elevado.
- Cabeçalho em gradiente azul.
- Cards com valores maiores e tipografia responsiva.
- Barras superiores coloridas nos cards.
- Gráficos Plotly com tema escuro.
- Tabelas e abas adaptadas para o novo contraste.
- Rótulos técnicos substituídos por linguagem comercial mais amigável.

Os cards foram reduzidos para quatro informações principais, evitando excesso de colunas e truncamento:

1. Oportunidades na seleção.
2. Alta prioridade.
3. Valor de catálogo.
4. Equipe na seleção e contas a revisar.

#### Decisão de comunicação da interface

O usuário solicitou que a interface não exibisse explicações técnicas sobre heurística, probabilidade, política ou composição interna. Essa decisão foi aplicada inicialmente na camada visual. Após a ressalva do challenge sobre explicabilidade, a ficha passou a exibir os fatores calculados pelo backend em linguagem comercial: ponto de partida e estágio comercial, com a contribuição de cada fator. O app continua sem jargão técnico, mas agora permite que o vendedor entenda por que a oportunidade está naquela prioridade.

Registros relacionados:

- `process-log/M4-streamlit.md`;
- `process-log/M4-ui-refinement.md`;
- `process-log/M4-ui-visual.md`;
- `process-log/M4-ajuste-final-interface.md`;
- `process-log/M4-publicacao-visual.md`.

### M5 — Testes e validação integrada

#### Testes automatizados

Os testes cobrem:

- validação de ingestão;
- contagem de registros;
- preservação de oportunidades sem conta;
- tratamento de aliases;
- análise e data de referência;
- pontuação somente de oportunidades abertas;
- reconciliação dos fatores;
- tratamento de valores ausentes;
- estabilidade do ranking;
- filtros individuais e combinados;
- preservação do score e da posição global após filtros;
- resultado vazio;
- busca textual.

#### Resultado final reproduzido

Comando executado:

```powershell
.\.venv\Scripts\python.exe -m compileall -q app.py src
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp .pytest-tmp-m6-final
.\.venv\Scripts\python.exe -c "import app; print('app importado com sucesso')"
```

Saída observada:

```text
17 passed in 1.86s
app importado com sucesso
```

O teste de importação exibiu apenas avisos esperados do Streamlit por estar sendo executado fora do runtime web, sem indicar falha da aplicação.

#### Validação integrada anterior

Na validação integrada registrada em M5:

- 2.089 oportunidades abertas foram carregadas.
- As prioridades ficaram entre 40 e 70.
- Um filtro combinado retornou 79 linhas.
- A prioridade permaneceu inalterada após o filtro.
- A política ponderou somente `deal_stage`.
- 1.588 linhas apresentaram avisos de dados ausentes.
- A ordem por prioridade não coincidiu com a ordem pura por preço em 2.069 de 2.089 posições.
- A aplicação publicada respondeu HTTP 200.

Foi encontrada uma falha de ambiente na primeira execução: 11 testes passaram e 3 tiveram erro de permissão no diretório temporário padrão do pytest. A suíte foi repetida com `--basetemp` dentro do projeto e terminou aprovada.

Registro detalhado: `process-log/M5-validacao.md`.

### Publicação

O repositório da aplicação é:

- [https://github.com/fnavaar-ia/leadscore-g4](https://github.com/fnavaar-ia/leadscore-g4)

A aplicação está publicada em:

- [https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/](https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/)

Publicações relevantes:

- `64fd8b1dccd15d48aac7307b08025b248e67dbeb` — upgrade visual do dashboard BI.
- `d00500a38aa21adf3e746ee77a489909304bceb2` — finalização da interface em modo escuro.

A disponibilidade pública foi verificada por requisição HTTP e retornou status 200. A publicação foi feita somente após autorização explícita do usuário.

---

## Estrutura do projeto

```text
LeadScore G4/
├── app.py                         # interface Streamlit
├── requirements.txt               # dependências do runtime e testes
├── config/
│   └── scoring_policy.json        # política versionada aprovada
├── data/
│   └── raw/                       # CSVs originais, preservados
│       ├── accounts.csv
│       ├── metadata.csv
│       ├── products.csv
│       ├── sales_pipeline.csv
│       └── sales_teams.csv
├── docs/
│   ├── ACEITE.md                  # checklist de aceite
│   ├── ARQUITETURA.md             # contratos e arquitetura
│   ├── DADOS.md                   # schemas e cuidados
│   ├── DECISOES.md                # decisões humanas registradas
│   ├── EDA_BASELINE.json          # baseline analítica
│   ├── PRD.md                     # especificação do produto
│   └── SCORING.md                 # restrições da política
├── outputs/
│   └── m2_eda.json                # saída derivada da análise
├── process-log/
│   ├── M1-ingestao.md
│   ├── M2-analise.md
│   ├── M3-scoring.md
│   ├── M4-streamlit.md
│   ├── M4-ui-refinement.md
│   ├── M4-ui-visual.md
│   ├── M4-ajuste-final-interface.md
│   ├── M4-publicacao-visual.md
│   ├── M5-validacao.md
│   ├── README.md
│   └── TEMPLATE.md
├── prompts/                       # instruções de M1 a M6
├── src/
│   ├── __init__.py
│   ├── analyze.py                 # análise reproduzível
│   ├── filters.py                 # filtros puros
│   ├── ingest.py                  # ingestão e joins
│   └── scoring.py                 # motor de priorização
├── tests/
│   ├── test_analyze.py
│   ├── test_filters.py
│   ├── test_ingest.py
│   └── test_scoring.py
├── MANIFEST.json                  # checksums do kit inicial
├── START_HERE.md                  # instrução inicial
├── AGENTS.md                      # regras do projeto
├── README.md                      # README inicial do kit
└── M6_DOCUMENTACAO_COMPLETA.md    # este documento independente
```

### Responsabilidade de cada camada

| Camada | Responsabilidade | O que não faz |
|---|---|---|
| `src/ingest.py` | Carrega, valida, tipa, normaliza aliases e faz joins | Não calcula prioridade |
| `src/analyze.py` | Gera estatísticas descritivas com corte declarado | Não pontua a fila operacional |
| `src/scoring.py` | Calcula prioridade, avisos e ranking | Não renderiza interface |
| `src/filters.py` | Devolve subconjuntos da fila pronta | Não recalcula prioridade |
| `app.py` | Exibe informações, gráficos e interações | Não deve conter regra de negócio independente |
| `tests/` | Verifica contratos e invariantes | Não substitui validação comercial |
| `process-log/` | Registra decisões, erros e evidências | Não é fonte de dados operacional |

---

## Setup

### Pré-requisitos

- Python instalado.
- Acesso ao diretório do projeto.
- Dependências de `requirements.txt`.
- Os arquivos CSV presentes em `data/raw/`.

### Windows PowerShell

Na raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Executar os testes:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Executar a aplicação:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Abrir no navegador o endereço exibido pelo Streamlit. No ambiente de desenvolvimento, a inicialização foi confirmada em `http://localhost:8501` em M4. A versão publicada está disponível no endereço do Streamlit informado acima.

### Ambiente efetivamente testado

```text
Python 3.15.0
pandas 3.0.6
plotly 7.1.0
streamlit 1.66.0
pytest 9.1.1
```

O arquivo `requirements.txt` mantém as dependências diretas do projeto:

```text
streamlit
pandas
plotly
pytest
```

### Caminhos e dados

Os módulos resolvem os arquivos relativos à raiz do projeto. Não há caminho absoluto embutido na aplicação, credencial, chave de API ou serviço externo necessário para o runtime. Os CSVs originais de `data/raw/` não são sobrescritos. A análise derivada é escrita em `outputs/`.

---

## Resultados / Findings

### Findings sobre os dados

- A base contém 8.800 oportunidades e 8.800 IDs únicos.
- O universo aberto tem 2.089 oportunidades.
- A ausência de conta ocorre em 1.425 registros e foi preservada.
- O alias `GTXPro` aparece em 1.480 linhas e é normalizado para `GTX Pro` na camada preparada.
- As oportunidades `Prospecting` somam 500 registros e não possuem `engage_date`.
- As oportunidades abertas não têm `close_date` e `close_value` disponíveis para decisão operacional.
- Existem 6.711 oportunidades fechadas, das quais 4.238 são Won.

### Findings sobre a priorização

- `Engaging` recebe prioridade 70 e `Prospecting` recebe prioridade 40, conforme política aprovada.
- O ranking não é uma ordenação direta por preço.
- O preço de catálogo só atua como desempate entre prioridades iguais.
- A comparação com preço puro produziu 2.069 posições diferentes em 2.089 oportunidades.
- A regra é simples de auditar e não depende de resultado futuro do próprio deal.

### Findings sobre a experiência

A experiência final passou por três níveis:

1. Uma fila operacional com filtros básicos.
2. Um dashboard BI com gráficos, KPIs, detalhes e exportação.
3. Uma interface em modo escuro com cards maiores, melhor contraste, valores responsivos e linguagem orientada ao usuário.

O resultado final privilegia leitura rápida e navegação. O usuário pode começar pelos indicadores, explorar os gráficos, filtrar a carteira, abrir a tabela e consultar uma oportunidade específica.

### Findings sobre qualidade

O projeto teve 17 testes aprovados na validação final, incluindo dois testes específicos para a explicação dos fatores na ficha da oportunidade. Também foi validado o carregamento do módulo principal e a disponibilidade HTTP da aplicação publicada. Os testes representam integridade técnica e consistência das regras; não representam prova de ganho de conversão ou aumento de receita.

---

## Lógica de priorização

Esta seção existe para a documentação da entrega e auditoria. A interface final exibe um resumo amigável dos fatores que formam a prioridade; a fórmula completa permanece documentada aqui para auditoria.

### Universo

Somente oportunidades com `deal_stage` em:

- `Engaging`;
- `Prospecting`.

`Won` e `Lost` são históricos e não entram na fila operacional.

### Cálculo

```text
base = 10

se deal_stage == "Engaging":
    prioridade = 10 + 60 = 70

se deal_stage == "Prospecting":
    prioridade = 10 + 30 = 40
```

O valor é limitado à faixa 0–100, embora os casos aprovados atuais resultem naturalmente em 40 ou 70.

### Ordenação

```text
1. prioridade decrescente
2. sales_price decrescente, com ausentes por último
3. opportunity_id crescente
```

O terceiro critério garante desempate estável mesmo quando duas oportunidades têm o mesmo estágio e o mesmo preço.

### O que não é usado como peso

- Conta.
- Setor.
- Número de funcionários.
- Região.
- Manager.
- Vendedor.
- Data de engajamento.
- Valor de fechamento.
- Data de fechamento.

Esses campos podem aparecer como contexto, filtro ou aviso, mas não são transformados em pontos pela política atual.

### Ausências

O projeto não fabrica valores para preencher ausências e não elimina deals sem conta. O registro permanece na fila e a interface informa a pendência em linguagem amigável.

### Interpretação correta

O número é um índice de prioridade definido por regra comercial. Ele não é uma probabilidade de fechamento, não é uma previsão de receita e não representa um resultado comercial já validado. A data `2017-12-31` é uma referência demonstrativa histórica, não a data atual nem um snapshot oficial comprovado.

---

## Recomendações

### Para o uso atual

1. Utilizar o dashboard como fila de revisão e organização da carteira.
2. Começar pela visão executiva para observar a distribuição da seleção.
3. Usar filtros de vendedor, manager e região para reuniões comerciais.
4. Exportar a seleção quando for necessário compartilhar uma lista operacional.
5. Revisar contas, datas e preços ausentes antes de tomar decisões de negócio.
6. Tratar a prioridade como apoio à decisão humana, e não como substituição do julgamento comercial.

### Para a próxima versão técnica

1. Adicionar histórico de atividades e interações.
2. Adicionar trilha de mudanças de estágio.
3. Registrar data de criação da oportunidade.
4. Integrar uma fonte de dados operacional ou pipeline de atualização controlado.
5. Definir uma avaliação temporal com features disponíveis no instante da decisão.
6. Medir impacto com critérios aprovados de negócio, como cobertura de follow-up, tempo de resposta e qualidade da fila.
7. Só considerar uma política mais sofisticada após validação com vendedores e RevOps.

### Para a submissão

1. Preencher nome do autor.
2. Adicionar LinkedIn somente se o autor desejar informá-lo.
3. Copiar este conteúdo para o `README.md` dentro de `submissions/<identificador>/` no repositório oficial do challenge.
4. Incluir uma cópia controlada da solução em `solution/`.
5. Incluir os registros necessários em `process-log/`.
6. Incluir documentos de apoio em `docs/`.
7. Executar novamente o setup a partir da estrutura reorganizada.
8. Criar uma branch de submissão e abrir o PR somente após confirmação do usuário.

---

## Limitações

### Limitações dos dados

- A base é histórica e offline.
- Não há trilha completa de atividades.
- Não há último contato confiável.
- `engage_date` ausente em parte de `Prospecting`.
- Há contas ausentes em oportunidades abertas.
- Não há quantidade de unidades.
- O preço de catálogo não é necessariamente o valor negociado.
- A ausência de conta não tem causa demonstrada.
- O corte de 31/12/2017 é demonstrativo.

### Limitações da priorização

- A regra atual usa apenas o estágio como componente ponderado.
- O resultado não foi calibrado como probabilidade.
- Não houve validação de ganho de conversão.
- Não houve experimento controlado com vendedores.
- Não há aprendizado automático.
- Não há ajuste por contexto de carteira.
- Preço não é utilizado como previsão de receita.

### Limitações da interface

- A aplicação não grava alterações no CRM.
- A aplicação não cria tarefas.
- A aplicação não envia notificações.
- Não há autenticação de produção.
- Não há controle de permissões por vendedor.
- O dataset é carregado localmente a cada ambiente/deploy.
- O relatório exportado é CSV; não há PDF ou integração com planilha.

### Limitações da validação

Os testes comprovam contratos técnicos, integridade dos dados, estabilidade e comportamento dos filtros. Eles não provam que a política aumentará receita, conversão ou produtividade. Essa conclusão exigiria dados prospectivos, definição de métrica, período de avaliação e comparação temporal adequada.

---

## Process Log — Como usei IA

### Ferramentas usadas

| Ferramenta | Para que foi usada |
|---|---|
| Codex | Leitura das instruções, decomposição modular, implementação, revisão, criação de testes e documentação |
| PowerShell | Inspeção de arquivos, execução de comandos, validações locais e verificação HTTP |
| Python / pandas | Ingestão, análise, preparação da fila e testes de dados |
| pytest | Execução da suíte automatizada |
| Streamlit | Construção e execução da aplicação interativa |
| Plotly | Gráficos interativos, medidor individual e visualizações de cobertura |
| GitHub Connector | Leitura do repositório oficial, publicação no repositório da aplicação e confirmação de commits |
| Streamlit Cloud | Deploy e disponibilidade pública da aplicação |

### Workflow

#### Etapa 0 — Leitura e escopo

O projeto começou com a leitura de `START_HERE.md`, `AGENTS.md`, PRD, arquitetura, dados, scoring, decisões e referências do challenge. A primeira decisão foi respeitar a sequência M1 → M2 → M3 → M4 → M5 → M6 e não tratar o kit inicial como se já contivesse uma implementação.

#### M1 — Dados

Foi solicitado que a IA validasse os CSVs reais, preservasse os originais e implementasse a ingestão. A saída foi um módulo de ingestão com diagnósticos e testes. Foram verificados contagem, IDs, chaves dimensionais, alias de produto, datas, números e ausências.

#### M2 — Análise

Foi solicitado que a IA corrigisse a análise temporal e separasse o histórico do universo aberto. Foi criada uma análise reproduzível, com saída JSON e testes. O corte correto de demonstração foi fixado em 31/12/2017.

#### M3 — Priorização

Antes do código, foi apresentada uma proposta de política. O usuário aprovou `heuristic-v1`. A política foi então colocada em JSON, implementada em módulo próprio e coberta por testes.

#### M4 — Interface

Foi criada a interface Streamlit com filtros, fila priorizada, detalhes e estados vazios. Depois, a interface evoluiu para um dashboard BI com Plotly, KPIs, exportação, cobertura de dados e ficha individual. Por decisão do usuário, os textos técnicos da regra foram removidos do app final, mas os motivos comerciais da prioridade passaram a ser exibidos na ficha da oportunidade após a revisão de aceite.

#### M5 — Validação

Foi executada a suíte completa, a validação integrada da fila, a invariância após filtros, a comparação com ordenação por preço e a verificação da aplicação publicada.

#### M6 — Documentação

Este documento consolida as decisões, a arquitetura, o setup, os resultados, as limitações, o processo e as evidências, seguindo a estrutura do template de submissão indicado pelo challenge.

### Onde a IA errou e como corrigi

#### Ambiente Python indisponível

No início, os comandos `python` e ferramentas associadas não estavam disponíveis no PATH. A correção foi instalar/configurar Python e criar `.venv` no projeto.

#### Instalação global com permissão negada

A tentativa de instalar dependências diretamente na pasta de usuário falhou com `WinError 5`. A instalação foi movida para `.venv`, que passou a ser usada nos comandos de teste e execução.

#### Diretório temporário do pytest sem permissão

Na primeira validação M5, 11 testes passaram e 3 tiveram erros de permissão no diretório temporário padrão. A suíte foi repetida com `--basetemp` dentro do projeto, produzindo resultado limpo de `14 passed` naquele estágio, `15 passed` após os refinamentos visuais e `17 passed` após os testes de explicabilidade.

#### Interface excessivamente técnica

A primeira evolução visual mostrava explicações técnicas de heurística e probabilidade, o que não correspondia ao objetivo de uma interface comercial simples. O usuário revisou essa decisão e solicitou remoção desses textos, modo escuro e cards mais legíveis. Depois, uma revisão de aceite identificou que retirar toda explicação também criava uma lacuna frente ao requisito de explicar a prioridade ao vendedor. A correção foi exibir os fatores calculados pelo backend com linguagem comercial, sem reintroduzir jargão técnico.

#### Truncamento dos cards

Os primeiros cards ficaram estreitos e exibiram reticências. A correção foi reduzir a quantidade de cards, aumentar o tamanho dos valores, usar CSS responsivo e permitir quebra controlada de textos.

#### Execução headless temporária bloqueada

Uma tentativa posterior de iniciar um servidor Streamlit temporário em outra porta foi bloqueada pela política do ambiente antes da inicialização. Isso foi registrado como limitação da verificação local. A inicialização real em M4 e a disponibilidade pública HTTP foram confirmadas em verificações separadas.

### O que eu adicionei que a IA sozinha não faria

As decisões humanas que orientaram o resultado foram:

- escolher Streamlit como stack;
- exigir uma construção modular antes de sofisticar a solução;
- aprovar explicitamente a política `heuristic-v1`;
- manter o preço de catálogo fora do cálculo principal;
- preservar oportunidades sem conta;
- exigir a referência histórica de 31/12/2017;
- pedir uma evolução visual com aparência de BI;
- solicitar modo escuro;
- remover detalhes técnicos da interface final;
- exigir cards maiores e legíveis;
- validar a aplicação publicada antes de avançar para M6.

Essas decisões não foram inferidas como fatos de negócio. Foram escolhas explícitas do responsável pelo projeto e estão refletidas no código e nos registros.

---

## Evidências

### Código e dados

- [Repositório da aplicação](https://github.com/fnavaar-ia/leadscore-g4)
- [Aplicação publicada](https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/)
- `app.py`
- `src/ingest.py`
- `src/analyze.py`
- `src/scoring.py`
- `src/filters.py`
- `config/scoring_policy.json`
- `data/raw/`
- `outputs/m2_eda.json`

### Testes

Comando final:

```powershell
.\.venv\Scripts\python.exe -m compileall -q app.py src
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp .pytest-tmp-m6-final
.\.venv\Scripts\python.exe -c "import app; print('app importado com sucesso')"
```

Resultado:

```text
17 passed in 1.86s
app importado com sucesso
```

### Registros de processo

- `process-log/M1-ingestao.md`
- `process-log/M2-analise.md`
- `process-log/M3-scoring.md`
- `process-log/M4-streamlit.md`
- `process-log/M4-ui-refinement.md`
- `process-log/M4-ui-visual.md`
- `process-log/M4-ajuste-final-interface.md`
- `process-log/M4-publicacao-visual.md`
- `process-log/M5-validacao.md`

### Commits públicos

- [Upgrade visual do dashboard BI](https://github.com/fnavaar-ia/leadscore-g4/commit/64fd8b1dccd15d48aac7307b08025b248e67dbeb)
- [Finalizar interface em modo escuro](https://github.com/fnavaar-ia/leadscore-g4/commit/d00500a38aa21adf3e746ee77a489909304bceb2)

### Evidências ainda não anexadas

- Screenshots da conversa com IA: não incluídos neste pacote.
- Screen recording do workflow: não produzido.
- Export completo de conversas: não produzido.

Esses itens não são apresentados como existentes. O documento utiliza os registros de processo, os testes, os commits e a URL pública como evidências disponíveis.

---

## Checklist final do documento

- [x] Estrutura baseada no template oficial.
- [x] Executive Summary incluído.
- [x] Abordagem descrita.
- [x] Resultados e findings reais incluídos.
- [x] Setup local documentado.
- [x] Lógica aprovada documentada.
- [x] Estrutura técnica explicada.
- [x] Interface e melhorias visuais descritas.
- [x] Testes e comandos reais registrados.
- [x] Limitações explicitadas.
- [x] Process log consolidado.
- [x] Evidências reais linkadas.
- [ ] Nome do autor preenchido.
- [ ] LinkedIn preenchido, se desejado.
- [ ] Pasta `submissions/<identificador>/` criada no repositório oficial.
- [ ] Solução reorganizada nessa pasta.
- [ ] Setup reexecutado após reorganização.
- [ ] Branch e PR de submissão criados após confirmação.

---

## Status do M6

Este arquivo é a documentação completa e independente do projeto atual. A aplicação está implementada, testada e publicada. A submissão formal no repositório do challenge ainda depende do identificador da pasta pessoal, do preenchimento dos dados do autor e da autorização para criar branch, publicar alterações no repositório de destino e abrir um Pull Request.

**Documento preparado em:** 20/10/2026.
