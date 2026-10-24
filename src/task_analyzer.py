
"""Módulo de análise de tarefas do TaskAnalyzer."""

from datetime import datetime
from typing import Any


class TaskValidationError(ValueError):
    """Representa erros de validação dos dados de uma tarefa."""


def analyze_tasks(tarefas: list[dict[str, Any]]) -> dict[str, Any]:
    """Analisa tarefas e calcula métricas de conclusão e atraso.

    Args:
        tarefas: Lista de tarefas com identificador, título, prioridade,
            datas e status.

    Returns:
        Dicionário com totais, tempos médios e taxa de atraso percentual.

    Raises:
        TaskValidationError: Se os dados de uma tarefa forem inválidos.
    """
    if not isinstance(tarefas, list):
        raise TaskValidationError(
            "A entrada deve ser uma lista de tarefas."
        )

    total_tarefas = len(tarefas)
    total_concluidas = 0
    total_pendentes = 0
    tarefas_atrasadas = 0
    tempos_conclusao: list[float] = []
    tempos_por_prioridade: dict[str, list[float]] = {}

    campos_obrigatorios = {
        "id",
        "titulo",
        "prioridade",
        "data_criacao",
        "data_conclusao",
        "status",
    }

    for tarefa in tarefas:
        if not isinstance(tarefa, dict):
            raise TaskValidationError(
                "Cada tarefa deve ser um dicionário."
            )

        campos_ausentes = campos_obrigatorios - tarefa.keys()
        if campos_ausentes:
            raise TaskValidationError(
                f"Campos obrigatórios ausentes: "
                f"{', '.join(sorted(campos_ausentes))}."
            )

        if (
            not isinstance(tarefa["titulo"], str)
            or not tarefa["titulo"].strip()
        ):
            raise TaskValidationError(
                "O título deve ser um texto não vazio."
            )

        status = tarefa["status"]
        if status not in {"concluida", "pendente"}:
            raise TaskValidationError(
                "O status deve ser 'concluida' ou 'pendente'."
            )

        prioridade = tarefa["prioridade"]
        if not isinstance(prioridade, str) or not prioridade.strip():
            raise TaskValidationError(
                "A prioridade deve ser um texto não vazio."
            )

        try:
            data_criacao = datetime.fromisoformat(
                tarefa["data_criacao"]
            )
        except (TypeError, ValueError) as erro:
            raise TaskValidationError(
                "A data de criação deve estar no formato ISO 8601."
            ) from erro

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

        if "data_prazo" not in tarefa:
            raise TaskValidationError(
                "Tarefas concluídas precisam informar data_prazo."
            )

        try:
            data_conclusao = datetime.fromisoformat(
                tarefa["data_conclusao"]
            )
            data_prazo = datetime.fromisoformat(
                tarefa["data_prazo"]
            )
        except (TypeError, ValueError) as erro:
            raise TaskValidationError(
                "As datas devem estar no formato ISO 8601."
            ) from erro

        if not (
            data_criacao.tzinfo
            == data_conclusao.tzinfo
            == data_prazo.tzinfo
        ):
            raise TaskValidationError(
                "As datas devem usar o mesmo padrão de fuso horário."
            )

        if data_conclusao < data_criacao:
            raise TaskValidationError(
                "A data de conclusão não pode ser anterior à data de criação."
            )

        if data_prazo < data_criacao:
            raise TaskValidationError(
                "O prazo não pode ser anterior à data de criação."
            )

        duracao_horas = (
            data_conclusao - data_criacao
        ).total_seconds() / 3600

        tempos_conclusao.append(duracao_horas)
        tempos_por_prioridade.setdefault(
            prioridade, []
        ).append(duracao_horas)
        total_concluidas += 1

        if data_conclusao > data_prazo:
            tarefas_atrasadas += 1

    tempo_medio = (
        sum(tempos_conclusao) / len(tempos_conclusao)
        if tempos_conclusao
        else 0.0
    )

    tempo_medio_por_prioridade = {
        prioridade: sum(tempos) / len(tempos)
        for prioridade, tempos in tempos_por_prioridade.items()
    }

    taxa_atraso_percentual = (
        tarefas_atrasadas / total_concluidas * 100
        if total_concluidas
        else 0.0
    )

    return {
        "total_tarefas": total_tarefas,
        "total_concluidas": total_concluidas,
        "total_pendentes": total_pendentes,
        "tempo_medio_conclusao_horas": tempo_medio,
        "tempo_medio_conclusao_horas_por_prioridade": (
            tempo_medio_por_prioridade
        ),
        "taxa_atraso_percentual": taxa_atraso_percentual,
    }
