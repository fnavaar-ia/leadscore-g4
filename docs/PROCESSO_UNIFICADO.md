# LeadScore G4 — processo de construção com IA

## Sobre mim

- **Nome:** Felipe Navaar
- **LinkedIn:** [Perfil profissional](https://www.linkedin.com/in/navaar-figueiredo-584500271/)
- **Challenge escolhido:** [003 — Lead Scorer](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/tree/main/challenges/build-003-lead-scorer)

## Executive Summary

Conduzi a criação do LeadScore G4 para ajudar vendedores a revisar oportunidades comerciais por prioridade. Comecei pelo entendimento do desafio e pela análise dos dados, transformei as conclusões em um PRD e preparei especificações e instruções para a construção com IA. Organizei a execução em módulos, acompanhei verificações e refinei a experiência do dashboard. O resultado documentado reúne uma aplicação Streamlit, código no GitHub e registros das decisões, com a submissão oficial ainda a concluir.

## Solução

### Abordagem

Organizei o trabalho para que cada etapa tivesse uma entrega verificável. Usei a IA na análise, na implementação e na documentação, mantendo sob minha responsabilidade as decisões de escopo, a aprovação da política de prioridade e a revisão da experiência do usuário.

### Resultados / Findings

- Dashboard com filtros, fila de oportunidades, gráficos, detalhes e exportação em CSV.
- Base de 8.800 oportunidades, com 2.089 abertas para priorização.
- Documentação de desenvolvimento com 17 testes aprovados e publicações registradas no GitHub.

### Recomendações

Concluir a organização da submissão. A explicação da prioridade foi reincorporada à ficha da oportunidade em linguagem comercial. Para evoluir o produto, incorporar histórico de atividades e validar sua utilidade com vendedores.

### Limitações

A base é histórica e o score representa uma regra de prioridade. O projeto não demonstrou aumento de conversão ou receita. A versão final simplifica a linguagem da interface, mas mostra os fatores calculados para que o vendedor entenda a prioridade da oportunidade.

## Process Log — Como usei IA

### Ferramentas usadas

| Ferramenta | Papel no processo |
|---|---|
| Codex | Apoio à implementação, revisão, testes e documentação, conforme os logs. |
| Antigravity IDE | Ambiente escolhido para a construção a partir do pacote de contexto. |
| Python, pandas e Streamlit | Preparação dos dados e desenvolvimento da aplicação. |
| pytest | Verificação automatizada dos módulos. |
| GitHub e Streamlit Cloud | Organização do código e publicação da aplicação. |

### Workflow

1. **Analisei o pedido.** Li o challenge, o guia de submissão e o template. Identifiquei a necessidade do vendedor e as entregas exigidas: solução funcional com dados reais, documentação e evidências do uso de IA. A pergunta orientadora foi: quais oportunidades revisar primeiro e por quê?

2. **Revisei os dados e construí o PRD.** Explorei as quatro tabelas, identifiquei oportunidades abertas, ausências e inconsistências e revisei interpretações da análise inicial. Com essa base, documentei problema, público, objetivo, escopo, limitações e critérios de aceite. Escolhi Python, pandas e Streamlit para o MVP.

3. **Transformei o PRD em specs.** Estruturei documentos de arquitetura, dados, scoring, decisões e aceite. Defini responsabilidades, entradas e saídas de cada camada. Incluí regras para preservar os dados originais, manter oportunidades sem conta e separar a lógica de prioridade da interface.

4. **Dividi a execução em módulos.** Organizei a sequência M1: ingestão, M2: análise, M3: scoring, M4: interface, M5: validação e M6: documentação. Cada módulo recebeu um prompt, entregáveis e critérios de conclusão. A política de scoring passou por aprovação explícita antes da implementação.

5. **Preparei o harness para o Antigravity.** Reuni o contexto necessário para orientar o agente: PRD, specs, CSVs, baseline analítica, prompts por módulo, checklist e modelo de process log. O `START_HERE.md` indicava a leitura inicial e a primeira tarefa. O `AGENTS.md` definia os limites permanentes. Esse conjunto orientou o que construir e como verificar cada entrega.

6. **Acompanhei a construção e as verificações.** A execução seguiu a divisão modular, com revisão dos arquivos, testes e registro de falhas e correções. Problemas de ambiente foram tratados com um ambiente virtual no projeto e ajustes no diretório temporário dos testes. Os registros preservam os comandos e resultados de cada etapa.

7. **Estruturei a página e refinei a experiência.** A primeira versão apresentou filtros, fila e detalhes. Depois, pedi uma evolução para dashboard BI, com indicadores, gráficos, busca e exportação. Revisei o visual com modo escuro, cards maiores e linguagem comercial. As iterações documentadas incluem versão funcional, refinamento BI e ajuste final de apresentação. O total de prompts não foi contabilizado.

8. **Organizei a evolução no GitHub.** O código, as dependências e os registros acompanharam as publicações da aplicação. A documentação registra commits de evolução visual e verificações após publicação. Separei essa entrega da submissão oficial, que ainda exige organizar a pasta pessoal, reproduzir o setup e abrir o Pull Request conforme as regras do challenge.

### Onde a IA errou e como corrigi

- **Interpretação dos dados:** revisei conclusões que confundiam score com probabilidade e preço de catálogo com receita esperada. Essas correções passaram a orientar o PRD e as regras do projeto.
- **Apresentação da interface:** identifiquei excesso de texto técnico e cards com conteúdo truncado. Pedi simplificação da linguagem, revisão da distribuição e ajuste de tipografia.

### O que eu adicionei que a IA sozinha não faria

Exigi um PRD modular antes da construção, escolhi a stack e aprovei a política de prioridade. Também direcionei as revisões visuais e defini quando uma sugestão precisava de correção ou de evidência. Minha participação manteve o desenvolvimento ligado ao problema comercial e aos critérios de entrega.

## Evidências

- [Registro da preparação](../process-log/fontes/registro-processo-lead-scorer.md) e [PRD](PRD.md).
- [Prompts por módulo](../prompts/) e [registros de desenvolvimento](../process-log/).
- [Documentação da implementação e resultados registrados](../M6_DOCUMENTACAO_COMPLETA.md).
- [Repositório da aplicação](https://github.com/fnavaar-ia/leadscore-g4) e [endereço da demonstração registrado no projeto](https://leadscore-g4-jk9owsqxk5hcymg8sbevjp.streamlit.app/).

Formato baseado no [guia de submissão](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/submission-guide.md) e no [template oficial](https://github.com/Gestao-Quatro-Ponto-Zero/ai-master-challenge/blob/main/templates/submission-template.md). Resultados de testes e publicação correspondem aos registros de desenvolvimento.

**Documento preparado em:** 20/10/2026. **Status:** submissão oficial pendente.
