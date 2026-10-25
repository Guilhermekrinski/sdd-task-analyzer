# TaskAnalyzer

Projeto do Bootcamp III desenvolvido com a abordagem Specification-Driven Development (SDD).

## Objetivo

Analisar tarefas e calcular métricas de conclusão e atraso.

## Funcionalidades

- Total de tarefas, concluídas e pendentes.
- Tempo médio de conclusão em horas.
- Tempo médio por prioridade.
- Taxa percentual de atraso.
- Validação de dados e tratamento de entradas inválidas.

## Tecnologias

- Python 3.11
- pytest
- Docker e Docker Compose
- GitHub Actions

## Estrutura

- `src/task_analyzer.py`: implementação.
- `tests/test_harness.py`: testes automatizados.
- `specs/task_analyzer_spec.md`: especificação.
- `specs/system_design_document.pdf`: documento de arquitetura.
- `CONTEXT_RULES.md`: regras de contexto e governança.
- `requirements.txt`: dependências Python.
- `requirements.yaml`: requisitos complementares.

## Executar os testes

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```
Para executar os testes, use `python -m pytest -v` após instalar as dependências com `python -m pip install -r requirements.txt`.

## Executar com Docker

Com Docker Desktop aberto, execute `docker compose run --rm task-analyzer-tests`.

## Limitações e governança

O sistema analisa tarefas em memória, sem banco de dados ou persistência em arquivos.

A taxa de atraso utiliza o campo adicional `data_prazo`. Essa regra ainda precisa ser validada com o professor.

O desenvolvimento segue a especificação e as regras de contexto documentadas em `CONTEXT_RULES.md`. Mudanças nas regras de negócio devem ser revisadas antes de serem incorporadas.
