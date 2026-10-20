# LeadScore G4

Painel comercial interativo para explorar e priorizar oportunidades abertas a partir de dados reais de CRM.

## Sobre o projeto

O LeadScore G4 organiza uma carteira de oportunidades em um dashboard visual e acionável. A aplicação permite filtrar a carteira por vendedor, manager, região, estágio e produto, consultar indicadores consolidados, explorar gráficos interativos, abrir o detalhe de uma oportunidade e exportar uma seleção em CSV.

O projeto foi desenvolvido para apoiar a rotina de vendas e Revenue Operations, oferecendo uma visão rápida de onde concentrar a revisão comercial e quais informações ainda precisam de atenção.

## Acesso rápido

- **Aplicação online:** [abrir o LeadScore G4 no Streamlit](https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/)
- **Dashboard:** visão executiva, fila de oportunidades, detalhe individual e cobertura dos dados.
- **Dados:** pipeline histórico real com dimensões de contas, produtos e equipe comercial.

## Funcionalidades

- Dashboard em modo escuro, responsivo e orientado à leitura executiva.
- Cards com volume da seleção, prioridades, valor de catálogo e informações pendentes.
- Filtros combináveis por vendedor, manager, região, estágio e produto.
- Busca por oportunidade, conta, produto ou vendedor.
- Faixa ajustável de prioridade.
- Gráficos interativos por estágio, região, manager e produto.
- Fila priorizada com posição global e contexto da oportunidade.
- Ficha individual com prioridade, conta, produto, vendedor, manager e região.
- Motivos da prioridade apresentados na ficha de cada oportunidade.
- Aba de cobertura dos dados para apoiar a revisão da carteira.
- Exportação da seleção filtrada em CSV.

## Como executar localmente

Requer Python 3.15 ou compatível.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Para validar o projeto:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Dados e escopo

O projeto utiliza o dataset público [CRM Sales Predictive Analytics](https://www.kaggle.com/datasets/agungpambudi/crm-sales-predictive-analytics), com licença declarada como CC0 no challenge.

Os CSVs originais estão em `data/raw/`. A aplicação preserva oportunidades sem conta e apresenta campos ausentes para revisão. A referência histórica da demonstração é 31/12/2017.

O sistema é uma ferramenta de apoio à revisão comercial. Ele não substitui o CRM, não envia mensagens, não cria tarefas e não realiza integrações externas durante a execução.

## Estrutura principal

```text
app.py                         # dashboard Streamlit
src/ingest.py                  # ingestão e preparação dos dados
src/analyze.py                 # análise reproduzível
src/scoring.py                 # priorização versionada
src/filters.py                 # filtros da fila
config/scoring_policy.json     # configuração da política
data/raw/                      # dados originais
tests/                         # testes automatizados
outputs/                       # saídas derivadas
process-log/                   # registros do desenvolvimento
M6_DOCUMENTACAO_COMPLETA.md   # documentação consolidada
```

## Documentação

- [Documentação completa do projeto e do M6](M6_DOCUMENTACAO_COMPLETA.md)
- [Política de priorização](config/scoring_policy.json)
- [Checklist de aceite](docs/ACEITE.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Dicionário e cuidados dos dados](docs/DADOS.md)
- [Registros do processo](process-log/)

## Stack

Python, pandas, Streamlit, Plotly e pytest.
