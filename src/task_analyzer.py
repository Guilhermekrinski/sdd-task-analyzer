"""Módulo de análise de tarefas do TaskAnalyzer."""

from datetime import datetime
from typing import Any


class TaskValidationError(ValueError):
    """Representa erros de validação dos dados de uma tarefa."""


def analyze_tasks(tarefas: list[dict[str, Any]]) -> dict[str, Any]:
    """Analisa tarefas e calcula métricas de conclusão.

    Args:
        tarefas: Lista de tarefas com identificador, título, prioridade,
            data de criação, data de conclusão e status.

    Returns:
        Dicionário com totais e tempo médio de conclusão geral e por prioridade.

    Raises:
        TaskValidationError: Se os dados de uma tarefa forem inválidos.
    """
    total_tarefas = len(tarefas)
    total_concluidas = 0
    total_pendentes = 0
    tempos_conclusao: list[float] = []
    tempos_por_prioridade: dict[str, list[float]] = {}

    for tarefa in tarefas:
        campos_obrigatorios = {
            "id",
            "titulo",
            "prioridade",
            "data_criacao",
            "data_conclusao",
            "status",
        }

        if not isinstance(tarefa, dict):
            raise TaskValidationError("Cada tarefa deve ser um dicionário.")

        campos_ausentes = campos_obrigatorios - tarefa.keys()
        if campos_ausentes:
            raise TaskValidationError(
                f"Campos obrigatórios ausentes: {', '.join(sorted(campos_ausentes))}."
            )

        status = tarefa["status"]
        if status not in {"concluida", "pendente"}:
            raise TaskValidationError(
                "O status deve ser 'concluida' ou 'pendente'."
            )

        if not isinstance(tarefa["prioridade"], str) or not tarefa["prioridade"].strip():
            raise TaskValidationError("A prioridade deve ser um texto não vazio.")

        if status == "pendente":
            if tarefa["data_conclusao"] is not None:
                raise TaskValidationError(
                    "Tarefas pendentes devem ter data_conclusao igual a None."
                )
            total_pendentes += 1
            continue

        if tarefa["data_conclusao"] is None:
            raise TaskValidationError(
                "Tarefas concluídas precisam de uma data de conclusão."
            )

        try:
            data_criacao = datetime.fromisoformat(tarefa["data_criacao"])
            data_conclusao = datetime.fromisoformat(tarefa["data_conclusao"])
        except (TypeError, ValueError) as erro:
            raise TaskValidationError(
                "As datas devem estar no formato ISO 8601."
            ) from erro

        if data_conclusao < data_criacao:
            raise TaskValidationError(
                "A data de conclusão não pode ser anterior à data de criação."
            )

        if data_criacao.tzinfo != data_conclusao.tzinfo:
            raise TaskValidationError(
                "As datas devem usar o mesmo padrão de fuso horário."
            )

        duracao_horas = (
            data_conclusao - data_criacao
        ).total_seconds() / 3600

        tempos_conclusao.append(duracao_horas)
        prioridade = tarefa["prioridade"]
        tempos_por_prioridade.setdefault(prioridade, []).append(duracao_horas)
        total_concluidas += 1

    tempo_medio = (
        sum(tempos_conclusao) / len(tempos_conclusao)
        if tempos_conclusao
        else 0.0
    )

    tempo_medio_por_prioridade = {
        prioridade: sum(tempos) / len(tempos)
        for prioridade, tempos in tempos_por_prioridade.items()
    }

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": tempo_medio,
        "tempo_medio_conclusao_horas_por_prioridade": tempo_medio_por_prioridade,
    }
