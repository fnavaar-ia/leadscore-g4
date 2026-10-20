# Arquitetura proposta — ainda não implementada

```text
app.py                   # interface Streamlit, sem regras de negócio embutidas
src/
  __init__.py
  ingest.py              # validação, tipagem, alias e joins
  analyze.py             # EDA reproduzível, denominadores e corte
  scoring.py             # regras versionadas e explicações
  filters.py             # filtros puros sobre fila já pontuada
tests/
  test_ingest.py
  test_analyze.py
  test_scoring.py
  test_filters.py
config/
  scoring_policy.json    # somente após aprovação da política
data/raw/                # originais presentes no kit
outputs/                 # dados derivados e diagnósticos
```

## Contratos propostos, não APIs existentes
- Ingestão recebe diretório de dados e devolve tabela enriquecida + diagnóstico. Preservar product_raw e campos originais quando normalizados; pandas merge com validate="many_to_one".
- Análise recebe tabela enriquecida + reference_date e devolve estatísticas descritivas com amostras/denominadores. Recalcular baseline de docs/EDA_BASELINE.json.
- Scoring recebe tabela, contexto histórico permitido e política aprovada; devolve uma linha por oportunidade aberta com opportunity_id, priority_score, score_factors, warnings, policy_version, reference_date e rank.
- Explicações devem permitir reconciliar base + contribuições + eventual clipping com score final. Usar representação serializável para fatores e avisos.
- Filtros recebem fila já pontuada e seleções; devolvem subconjunto, sem alterar score. Não usar valor exibido de posição filtrada como se fosse score.
- UI consome essas saídas e mostra erro legível, estado vazio, dados ausentes e limitações. Cache apenas onde não introduza estado obsoleto.

## Jornada
Abrir app → filtrar carteira → ver deals abertos priorizados → selecionar oportunidade → ler fatores e avisos → decidir manualmente.

Sem banco de dados ou API externa no MVP. Uma tela com sidebar de filtros, resumo, tabela priorizada e detalhes é suficiente. Não criar uma arquitetura de produção para um desafio offline.

