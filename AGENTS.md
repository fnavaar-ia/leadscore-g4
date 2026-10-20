# Instruções de projeto para o agente

- Leia START_HERE.md e os documentos do projeto. Trabalhe um módulo por vez, M1 → M2 → M3 → M4 → M5 → M6.
- Stack confirmada: Python, pandas, Streamlit; testes com pytest. Não adicione framework web alternativo.
- Este kit não contém implementação. Não afirme que app, testes ou scoring já existem.
- Separe ingestão, análise, scoring e filtros da interface Streamlit. Sem caminhos absolutos, credenciais ou APIs de IA em runtime.
- Preserve data/raw; escreva saídas derivadas em outputs/. Resolva caminhos relativamente à raiz do projeto, não ao diretório corrente.
- Use CSVs reais. Nunca substitua valores ausentes por informações fabricadas nem descarte deals sem conta.
- Score heurístico NÃO é probabilidade; preço de catálogo NÃO é receita esperada. Duração de fechamento NÃO é inatividade.
- Políticas comerciais e pesos precisam ser explicitamente aprovados antes do M3. Não ressuscite inferências corrigidas no PRD.
- Data de referência de demonstração: 2017-12-31, não snapshot oficial comprovado. Nunca use a data atual para envelhecer esses deals históricos.
- Estatísticas históricas só podem usar resultados conhecidos até o corte permitido. Uma avaliação retrospectiva exige features no instante da decisão, sem vazamento temporal.
- Filtros não recalculam score. Empates precisam de regra estável. Missing gera aviso e tratamento documentado.
- Teste e execute de verdade antes de afirmar conclusão; registre comandos e saídas reais. Não invente validação comercial.
- Mantenha process-log/ com prompts, verificações, erros, correções e decisões humanas reais. Capture evidências com consentimento, sem segredos.
- Não envie mensagens, publique, faça commit/push ou PR sem confirmação. A entrega final só modifica submissions/seu-nome/ no repositório de destino.

