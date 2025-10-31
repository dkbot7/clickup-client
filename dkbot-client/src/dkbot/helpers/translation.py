# -*- coding: utf-8 -*-
"""
Módulo de tradução PT ↔ EN para parâmetros do ClickUp.

Permite que usuários brasileiros usem o cliente 100% em português,
com tradução automática interna para inglês antes de enviar à API.
"""

from typing import Dict, Any, Union


# Tradução de nomes de parâmetros PT → EN
PARAM_NAMES_PT_TO_EN = {
    # Campos principais
    "nome": "name",
    "descrição": "description",
    "descricao": "description",

    # Datas
    "data_vencimento": "due_date",
    "data_inicio": "start_date",
    "data_criacao": "date_created",
    "data_atualizacao": "date_updated",
    "data_fechamento": "date_closed",

    # Status e prioridade
    "status": "status",
    "prioridade": "priority",

    # Pessoas
    "responsáveis": "assignees",
    "responsaveis": "assignees",
    "criador": "creator",
    "observadores": "watchers",

    # Tags e categorias
    "etiquetas": "tags",
    "tags": "tags",

    # Filtros
    "arquivada": "archived",
    "arquivado": "archived",
    "página": "page",
    "pagina": "page",
    "ordenar_por": "order_by",
    "incluir_fechadas": "include_closed",
    "incluir_subtasks": "subtasks",

    # Estimativas
    "tempo_estimado": "time_estimate",
    "tempo_gasto": "time_spent",

    # Outros
    "conteúdo": "content",
    "conteudo": "content",
    "texto": "text",
    "cor": "color",
}


# Tradução de valores de STATUS PT → EN
STATUS_PT_TO_EN = {
    # Estados comuns
    "fazer": "to do",
    "a fazer": "to do",
    "pendente": "to do",
    "aberto": "open",
    "em progresso": "in progress",
    "em andamento": "in progress",
    "fazendo": "in progress",
    "revisão": "review",
    "revisao": "review",
    "em revisão": "in review",
    "em revisao": "in review",
    "concluído": "complete",
    "concluido": "complete",
    "finalizado": "complete",
    "feito": "done",
    "fechado": "closed",
    "cancelado": "cancelled",
    "bloqueado": "blocked",
}


# Tradução de valores de PRIORIDADE PT → EN
# ClickUp usa: 1=urgent, 2=high, 3=normal, 4=low
PRIORITY_PT_TO_EN = {
    "urgente": 1,
    "alta": 2,
    "normal": 3,
    "baixa": 4,

    # Variações em texto
    "urgent": 1,
    "high": 2,
    "medium": 3,
    "low": 4,
}


# Tradução EN → PT para exibição de resultados
PARAM_NAMES_EN_TO_PT = {v: k for k, v in PARAM_NAMES_PT_TO_EN.items() if k == k.lower()}
STATUS_EN_TO_PT = {v: k for k, v in STATUS_PT_TO_EN.items() if k == k.lower()}


def translate_param_name(param: str, to_english: bool = True) -> str:
    """
    Traduz nome de parâmetro entre PT e EN.

    Args:
        param: Nome do parâmetro
        to_english: Se True, traduz PT → EN. Se False, traduz EN → PT

    Returns:
        Parâmetro traduzido ou original se não encontrado

    Exemplos:
        >>> translate_param_name("nome")
        "name"

        >>> translate_param_name("data_vencimento")
        "due_date"

        >>> translate_param_name("name", to_english=False)
        "nome"
    """
    param_lower = param.lower()

    if to_english:
        return PARAM_NAMES_PT_TO_EN.get(param_lower, param)
    else:
        return PARAM_NAMES_EN_TO_PT.get(param_lower, param)


def translate_status(status: str, to_english: bool = True) -> str:
    """
    Traduz valor de status entre PT e EN.

    Args:
        status: Valor do status
        to_english: Se True, traduz PT → EN. Se False, traduz EN → PT

    Returns:
        Status traduzido ou original se não encontrado

    Exemplos:
        >>> translate_status("em progresso")
        "in progress"

        >>> translate_status("concluído")
        "complete"
    """
    status_lower = status.lower()

    if to_english:
        return STATUS_PT_TO_EN.get(status_lower, status)
    else:
        return STATUS_EN_TO_PT.get(status_lower, status)


def translate_priority(priority: Union[str, int], to_english: bool = True) -> Union[str, int]:
    """
    Traduz valor de prioridade entre PT e EN.

    Args:
        priority: Valor da prioridade (texto ou número)
        to_english: Se True, traduz PT → EN. Se False, traduz EN → PT

    Returns:
        Prioridade traduzida (sempre número para EN)

    Exemplos:
        >>> translate_priority("alta")
        2

        >>> translate_priority("urgente")
        1

        >>> translate_priority(2, to_english=False)
        "alta"
    """
    if to_english:
        # Se já é número, retorna como está
        if isinstance(priority, int):
            return priority

        # Se é string, tenta traduzir
        priority_lower = str(priority).lower()
        return PRIORITY_PT_TO_EN.get(priority_lower, priority)
    else:
        # EN → PT: converte número para texto em português
        priority_map_reverse = {1: "urgente", 2: "alta", 3: "normal", 4: "baixa"}
        return priority_map_reverse.get(priority, priority)


def translate_params(params: Dict[str, Any], to_english: bool = True) -> Dict[str, Any]:
    """
    Traduz um dicionário completo de parâmetros.

    - Traduz chaves (nomes de parâmetros)
    - Traduz valores conhecidos (status, prioridade)
    - Mantém valores desconhecidos intactos

    Args:
        params: Dicionário com parâmetros
        to_english: Se True, traduz PT → EN. Se False, traduz EN → PT

    Returns:
        Novo dicionário com traduções aplicadas

    Exemplos:
        >>> translate_params({"nome": "Tarefa", "prioridade": "alta"})
        {"name": "Tarefa", "priority": 2}

        >>> translate_params({"status": "em progresso", "data_vencimento": "amanhã"})
        {"status": "in progress", "due_date": "amanhã"}
    """
    translated = {}

    for key, value in params.items():
        # Traduz a chave
        new_key = translate_param_name(key, to_english)

        # Traduz o valor se for status ou prioridade
        if new_key in ["status"] and isinstance(value, str):
            new_value = translate_status(value, to_english)
        elif new_key in ["priority", "prioridade"] and (isinstance(value, (str, int))):
            new_value = translate_priority(value, to_english)
        else:
            new_value = value

        translated[new_key] = new_value

    return translated


def is_portuguese_param(param: str) -> bool:
    """
    Verifica se um parâmetro está em português.

    Args:
        param: Nome do parâmetro

    Returns:
        True se é português, False caso contrário

    Exemplos:
        >>> is_portuguese_param("nome")
        True

        >>> is_portuguese_param("name")
        False
    """
    return param.lower() in PARAM_NAMES_PT_TO_EN
