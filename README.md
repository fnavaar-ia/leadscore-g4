# Lead Scorer — kit de recriação em Streamlit

Este pacote reúne contexto, dados reais, PRD e prompts para construir o projeto no Antigravity IDE. **Não contém aplicativo implementado.** Não usa configurações proprietárias de IDE: são arquivos Markdown e CSV portáveis. Não pressupõe que AGENTS.md seja carregado automaticamente; peça explicitamente ao agente para lê-lo.

## Como começar
1. Extraia o ZIP e abra a pasta `lead-scorer-antigravity` no IDE.
2. Abra `START_HERE.md` e copie o prompt inicial para a conversa com o agente.
3. Execute um módulo por vez, seguindo os arquivos de `prompts/`.
4. Aprove a política de scoring antes de implementar M3.
5. Registre decisões e evidências reais no process log durante o trabalho.

## O que existe
- `docs/PRD.md`: especificação modular, adaptada para Streamlit.
- `docs/ARQUITETURA.md`: estrutura proposta, responsabilidades e contratos.
- `docs/DADOS.md`: schema, referências, cuidados e proveniência.
- `docs/EDA_BASELINE.json`: baseline recalculada dos CSVs, sem inferência preditiva.
- `docs/SCORING.md`: restrições e decisões ainda pendentes; não é uma fórmula aprovada.
- `docs/ACEITE.md`: checklist verificável.
- `docs/DECISOES.md`: decisões confirmadas e pendências.
- `references/`: cópias dos requisitos oficiais, guia e template.
- `data/raw/`: quatro tabelas do dataset e metadata.csv, sem alteração dos originais.
- `prompts/`: sequência de execução M1–M6.
- `process-log/`: modelo para registrar evidências.

## Stack escolhida
Python + pandas + Streamlit; pytest para testes. Dependências propostas em `requirements.txt`, sem versões inventadas. Validar compatibilidade no ambiente de destino e registrar versões efetivamente testadas.

Após o agente implementar os arquivos propostos, a rotina esperada será:
```sh
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```
**Hoje esses comandos de teste e app não têm implementação para executar neste kit.** O agente deve criá-la nos módulos correspondentes.

Não copiar este README como se fosse a submissão final: usar `references/submission-template.md`, preencher resultados reais e respeitar a pasta pessoal exigida pelo desafio.

