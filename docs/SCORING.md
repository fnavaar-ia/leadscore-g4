# Política de scoring — pendente de aprovação

Não existe fórmula aprovada neste kit. Desenvolva a proposta apenas depois de M1 e M2. A escolha Streamlit não aprova pesos, thresholds ou premissas estatísticas.

## Requisitos
- Priority score 0–100, determinístico, explicável; não é chance percentual de fechar.
- Sinais de negócio devem ser rotulados como heurísticas. Associação histórica não prova causalidade.
- Estágio pode representar maturidade comercial por decisão explícita; não há conversão por estágio inicial comprovada.
- Idade é contexto; não penalizar automaticamente por “inatividade”.
- Se usar histórico de vendedor, mostrar amostra, suavização e fallback global; documentar corte temporal e viés de carteira. Não tornar esse componente obrigatório sem justificativa.
- Setor/porte/região: contexto por padrão, peso zero até justificativa aprovada.
- Preço de catálogo é referência, não receita esperada. Se entrar no score, limitar contribuição para não reduzir ranking a preço.
- Ausência de conta não é sinônimo de baixa qualidade. Não descartar o deal.
- Não usar close_value/close_date do próprio deal aberto ou duração final como feature.
- Filtros nunca mudam a política ou o score; empate resolvido de forma estável e documentada.

## Entrega da proposta antes do código
Apresentar: base; fatores; fórmulas; pesos; faixas; justificativas; fallbacks; soma e clipping; desempate; exemplos hipotéticos claramente marcados; limitações. Pedir aprovação, parar e só depois implementar M3.

## Validação
Comparar com ordenação por preço e por estágio para explicar diferenças. Essa comparação NÃO comprova melhoria de conversão. Avaliação retrospectiva exige reconstrução temporal adequada, indisponível de forma completa nos CSVs.

