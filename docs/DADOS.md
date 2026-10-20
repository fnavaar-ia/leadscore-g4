# Dados e proveniência

Fonte indicada pelo desafio: https://www.kaggle.com/datasets/agungpambudi/crm-sales-predictive-analytics
Download utilizado: https://www.kaggle.com/api/v1/datasets/download/agungpambudi/crm-sales-predictive-analytics
Licença declarada pelo desafio: CC0. Os CSVs incluídos são cópias sem alteração do download; checksums em MANIFEST.json.

## Schemas
- accounts.csv (85): account, sector, year_established, revenue, employees, office_location, subsidiary_of.
- products.csv (7): product, series, sales_price.
- sales_teams.csv (35): sales_agent, manager, regional_office.
- sales_pipeline.csv (8.800): opportunity_id, sales_agent, product, account, deal_stage, engage_date, close_date, close_value.
- metadata.csv: dicionário original auxiliar. Consultar para unidades e significado dos campos.

## Relações
Pipeline é o hub. Join à esquerda por account, product, sales_agent, com validação many-to-one e preservação de IDs. Não fazer inner join que elimina oportunidades sem conta.

## Tratamentos conhecidos
- Mapear GTXPro → GTX Pro somente na camada preparada; 1.480 registros afetados.
- 1.425 account ausentes: 1.088 Engaging e 337 Prospecting. Causa desconhecida.
- 500 Prospecting sem engage_date: idade desconhecida, não zero inventado.
- 2.089 abertos sem close_date/close_value: não preencher com resultados estimados.
- technolgy é grafia original do setor; se normalizar, documentar e preservar o original.
- subsidiary_of ausente não é erro obrigatório; não assumir relação societária.

## Temporalidade e interpretação
Corte demonstrativo 2017-12-31 corresponde ao maior close_date observado, não a um snapshot oficial comprovado. Idade desde engage_date não mede último contato. Futuros campos de fechamento não podem alimentar scoring operacional.

A baseline JSON foi recalculada para este pacote, incluindo médias apenas dos Won. Ela é um ponto de reconciliação, não uma EDA completa nem validação preditiva. Não levar para o novo projeto a antiga recomendação score × preço como receita esperada.

