# -*- coding: utf-8 -*-
"""
Utilitários para parsing de datas em linguagem natural.

Substitui o Pendulum usando dateparser (compatível com Python 3.13).
Suporta datas em português e inglês.
"""

import dateparser
from datetime import datetime
from typing import Union, Optional


def fuzzy_time_to_unix(text: Union[str, int]) -> int:
    """
    Converte data em linguagem natural para Unix timestamp (milissegundos).

    Compatível com ClickUp API que espera timestamps em milissegundos.

    Args:
        text: Data em formato legível ou timestamp Unix

    Suporta:
        - Linguagem natural: "tomorrow", "next week", "december 1st"
        - Português: "amanhã", "próxima semana", "1 de dezembro"
        - ISO 8601: "2024-12-01T00:00:00Z"
        - Timestamp Unix (retorna como está se já for número)

    Returns:
        Unix timestamp em milissegundos

    Exemplos:
        >>> fuzzy_time_to_unix("tomorrow")
        1701475200000

        >>> fuzzy_time_to_unix("amanhã")
        1701475200000

        >>> fuzzy_time_to_unix("next friday")
        1701993600000

        >>> fuzzy_time_to_unix("2024-12-01")
        1701388800000
    """
    # Se já é um timestamp (número ou string numérica)
    try:
        timestamp = int(text)
        # Se já está em milissegundos, retorna
        if timestamp > 10000000000:  # Timestamp em ms (ano > 2286)
            return timestamp
        # Se está em segundos, converte para ms
        return timestamp * 1000
    except (ValueError, TypeError):
        pass

    # Parse com dateparser (suporta português e inglês)
    dt = dateparser.parse(
        str(text),
        languages=['pt', 'en'],
        settings={
            'PREFER_DATES_FROM': 'future',  # Prefer datas futuras
            'RETURN_AS_TIMEZONE_AWARE': False
        }
    )

    if dt is None:
        raise ValueError(
            f"Não foi possível converter '{text}' para data. "
            f"Formatos suportados: 'amanhã', 'tomorrow', '2024-12-01', etc."
        )

    # Converte para Unix timestamp em milissegundos
    return int(dt.timestamp() * 1000)


def fuzzy_time_to_seconds(text: Union[str, int]) -> int:
    """
    Converte duração em linguagem natural para segundos.

    Args:
        text: Duração em formato legível

    Suporta:
        - Inglês: "2 hours", "30 minutes", "1 day"
        - Português: "2 horas", "30 minutos", "1 dia"
        - Números diretos (retorna como está)

    Returns:
        Duração em segundos

    Exemplos:
        >>> fuzzy_time_to_seconds("2 hours")
        7200

        >>> fuzzy_time_to_seconds("30 minutes")
        1800

        >>> fuzzy_time_to_seconds("1 day")
        86400
    """
    # Se já é um número, retorna
    try:
        return int(text)
    except (ValueError, TypeError):
        pass

    # Mapeamento de escalas de tempo
    SCALES = {
        # Inglês
        "second": 1,
        "seconds": 1,
        "sec": 1,
        "secs": 1,
        "minute": 60,
        "minutes": 60,
        "min": 60,
        "mins": 60,
        "hour": 3600,
        "hours": 3600,
        "hr": 3600,
        "hrs": 3600,
        "day": 86400,
        "days": 86400,
        "week": 604800,
        "weeks": 604800,
        "month": 2592000,  # 30 dias
        "months": 2592000,
        "year": 31536000,  # 365 dias
        "years": 31536000,

        # Português
        "segundo": 1,
        "segundos": 1,
        "seg": 1,
        "minuto": 60,
        "minutos": 60,
        "hora": 3600,
        "horas": 3600,
        "dia": 86400,
        "dias": 86400,
        "semana": 604800,
        "semanas": 604800,
        "mês": 2592000,
        "meses": 2592000,
        "ano": 31536000,
        "anos": 31536000,
    }

    text_lower = str(text).lower().strip()
    total_seconds = 0

    # Divide em palavras e processa
    words = text_lower.split()

    i = 0
    while i < len(words):
        # Tenta encontrar número + unidade
        if i + 1 < len(words):
            try:
                value = float(words[i])
                unit = words[i + 1]

                if unit in SCALES:
                    total_seconds += value * SCALES[unit]
                    i += 2
                    continue
            except ValueError:
                pass

        i += 1

    if total_seconds > 0:
        return int(total_seconds)

    raise ValueError(
        f"Não foi possível converter '{text}' para segundos. "
        f"Exemplos: '2 hours', '30 minutes', '1 day'"
    )


def parse_date(text: Union[str, int, datetime], to_milliseconds: bool = True) -> Union[int, datetime]:
    """
    Função genérica para parsing de datas.

    Args:
        text: Data em qualquer formato suportado
        to_milliseconds: Se True, retorna timestamp em ms. Se False, retorna datetime

    Returns:
        Unix timestamp (ms) ou objeto datetime

    Exemplos:
        >>> parse_date("tomorrow", to_milliseconds=True)
        1701475200000

        >>> parse_date("2024-12-01", to_milliseconds=False)
        datetime.datetime(2024, 12, 1, 0, 0)
    """
    # Se já é datetime, retorna conforme solicitado
    if isinstance(text, datetime):
        if to_milliseconds:
            return int(text.timestamp() * 1000)
        return text

    # Parse com fuzzy_time_to_unix
    timestamp_ms = fuzzy_time_to_unix(text)

    if to_milliseconds:
        return timestamp_ms

    # Converte timestamp ms para datetime
    return datetime.fromtimestamp(timestamp_ms / 1000)
