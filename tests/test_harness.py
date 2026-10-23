"""Testes de aceitação do TaskAnalyzer."""

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks


def test_total_de_tarefas() -> None:
    """Verifica o total de tarefas recebidas."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa concluída",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "status": "concluida",
        },
        {
            "id": 2,
            "titulo": "Tarefa pendente",
            "prioridade": "baixa",
            "data_criacao": "2026-01-02T09:00:00",
            "data_conclusao": None,
            "status": "pendente",
        },
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["total_tarefas"] == 2
    assert resultado["total_concluidas"] == 1
    assert resultado["total_pendentes"] == 1


def test_tempo_medio_de_conclusao() -> None:
    """Verifica o tempo médio de conclusão em horas."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa A",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "status": "concluida",
        },
        {
            "id": 2,
            "titulo": "Tarefa B",
            "prioridade": "alta",
            "data_criacao": "2026-01-02T09:00:00",
            "data_conclusao": "2026-01-02T13:00:00",
            "status": "concluida",
        },
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["tempo_medio_conclusao_horas"] == 3.0


def test_datas_inconsistentes_geram_excecao() -> None:
    """Verifica a validação da ordem das datas."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa inválida",
            "prioridade": "alta",
            "data_criacao": "2026-01-02T12:00:00",
            "data_conclusao": "2026-01-02T10:00:00",
            "status": "concluida",
        },
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_lista_vazia() -> None:
    """Verifica o comportamento sem tarefas."""
    resultado = analyze_tasks([])

    assert resultado["total_tarefas"] == 0
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0


def test_apenas_tarefas_pendentes() -> None:
    """Verifica o comportamento quando não há tarefas concluídas."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa pendente",
            "prioridade": "média",
            "data_criacao": "2026-01-03T09:00:00",
            "data_conclusao": None,
            "status": "pendente",
        },
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["total_tarefas"] == 1
    assert resultado["total_concluidas"] == 0
    assert resultado["total_pendentes"] == 1
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
