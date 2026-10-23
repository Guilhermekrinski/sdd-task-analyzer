
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
            "data_prazo": "2026-01-01T12:00:00",
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
            "data_prazo": "2026-01-01T12:00:00",
            "status": "concluida",
        },
        {
            "id": 2,
            "titulo": "Tarefa B",
            "prioridade": "alta",
            "data_criacao": "2026-01-02T09:00:00",
            "data_conclusao": "2026-01-02T13:00:00",
            "data_prazo": "2026-01-02T14:00:00",
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
            "data_prazo": "2026-01-02T11:00:00",
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

def test_taxa_de_atraso_percentual() -> None:
    """Verifica a taxa de atraso quando metade das tarefas atrasa."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa no prazo",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T12:00:00",
            "status": "concluida",
        },
        {
            "id": 2,
            "titulo": "Tarefa atrasada",
            "prioridade": "baixa",
            "data_criacao": "2026-01-02T09:00:00",
            "data_conclusao": "2026-01-02T15:00:00",
            "data_prazo": "2026-01-02T12:00:00",
            "status": "concluida",
        },
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["taxa_atraso_percentual"] == 50.0


def test_taxa_de_atraso_sem_tarefas_concluidas() -> None:
    """Verifica a taxa de atraso sem tarefas concluídas."""
    resultado = analyze_tasks([])

    assert resultado["taxa_atraso_percentual"] == 0.0


def test_taxa_de_atraso_com_todas_no_prazo() -> None:
    """Verifica a taxa de atraso quando todas estão no prazo."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa no prazo",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T12:00:00",
            "status": "concluida",
        },
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["taxa_atraso_percentual"] == 0.0

def test_tarefa_sem_campo_obrigatorio() -> None:
    """Verifica o erro quando falta um campo obrigatório."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa incompleta",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T12:00:00",
            # Campo status ausente
        },
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_data_em_formato_invalido() -> None:
    """Verifica o erro quando uma data não segue o formato esperado."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa com data inválida",
            "prioridade": "alta",
            "data_criacao": "data inválida",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T12:00:00",
            "status": "concluida",
        },
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_prazo_anterior_a_criacao() -> None:
    """Verifica o erro quando o prazo é anterior à criação."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa com prazo inválido",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T08:00:00",
            "status": "concluida",
        },
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_tarefa_nao_e_dicionario() -> None:
    """Verifica o erro quando um item não é um dicionário."""
    tarefas = ["tarefa inválida"]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


def test_status_invalido() -> None:
    """Verifica o erro quando o status não é reconhecido."""
    tarefas = [
        {
            "id": 1,
            "titulo": "Tarefa com status inválido",
            "prioridade": "alta",
            "data_criacao": "2026-01-01T09:00:00",
            "data_conclusao": "2026-01-01T11:00:00",
            "data_prazo": "2026-01-01T12:00:00",
            "status": "em andamento",
        },
    ]

    with pytest.raises(TaskValidationError):
        analyze_tasks(tarefas)


