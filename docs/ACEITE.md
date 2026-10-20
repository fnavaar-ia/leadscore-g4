# Checklist de aceite — iniciar desmarcado

- [x] AC01: carregar dados reais, reconciliar 8.800 IDs e 2.089 abertos.
- [x] AC02: alias corrigido na camada preparada, joins sem multiplicação, ausências preservadas.
- [x] AC03: score finito 0–100, determinístico e política versionada aprovada.
- [x] AC04: fatores reconciliam score; clipping explícito; não chamar score de probabilidade.
- [x] AC05: ranking não é apenas preço; testar fatores diferentes com preço igual e desempates.
- [x] AC06: filtros individuais/combinados e estado vazio; score invariável sob filtros.
- [x] AC07: data de referência declarada, sem idades negativas, sem leakage.
- [x] AC08: instalação, pytest e inicialização real do Streamlit documentadas com saídas.
- [x] AC09: revisar manualmente carteira → fila → explicação; verificar conta e idade ausentes.
- [ ] AC10: README final conforme template, setup, lógica, limitações e process log; PR só na pasta pessoal.

Testar ainda: colunas/arquivos obrigatórios ausentes; chaves duplicadas nas dimensões; produto desconhecido; vendedor sem histórico; resultado filtrado vazio; estabilidade após embaralhar linhas. Usar dados sintéticos apenas em fixtures de testes, claramente identificados, nunca como substituto dos CSVs operacionais.

Não marcar itens apenas por leitura de código. Registrar comando, resultado e evidência correspondente. CLI e testes documentados aqui são metas, não resultados já executados no novo app.

