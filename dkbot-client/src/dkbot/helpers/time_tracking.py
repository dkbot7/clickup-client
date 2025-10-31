"""
Time Tracking Helper - ClickUp API Client
Sistema Kaloi - dkbot-client

Helpers para trabalhar com Time Tracking do ClickUp.
Cálculos, formatação e análises de tempo.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


def milliseconds_to_duration(milliseconds: int) -> str:
    """
    Converte milissegundos para string legível (HH:MM:SS).

    Args:
        milliseconds: Duração em milissegundos

    Returns:
        String formatada "HH:MM:SS"

    Example:
        >>> milliseconds_to_duration(3661000)
        "01:01:01"
    """
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def duration_to_milliseconds(duration_str: str) -> int:
    """
    Converte string de duração para milissegundos.

    Args:
        duration_str: String no formato "HH:MM:SS" ou "HH:MM"

    Returns:
        Duração em milissegundos

    Example:
        >>> duration_to_milliseconds("01:30:00")
        5400000
    """
    parts = duration_str.split(":")

    if len(parts) == 2:  # HH:MM
        hours, minutes = int(parts[0]), int(parts[1])
        seconds = 0
    elif len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        raise ValueError(f"Formato inválido: {duration_str}. Use HH:MM ou HH:MM:SS")

    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds * 1000


def calculate_total_time(time_entries: List[Dict]) -> int:
    """
    Calcula tempo total de uma lista de time entries.

    Args:
        time_entries: Lista de time entries retornados pela API

    Returns:
        Tempo total em milissegundos
    """
    total = 0
    for entry in time_entries:
        duration = entry.get("duration")
        if duration:
            total += int(duration)

    return total


def format_duration(milliseconds: int, format_type: str = "verbose") -> str:
    """
    Formata duração em diferentes formatos.

    Args:
        milliseconds: Duração em milissegundos
        format_type: Tipo de formatação
            - "verbose": "2 horas, 30 minutos, 15 segundos"
            - "short": "2h 30m 15s"
            - "clock": "02:30:15"
            - "decimal": "2.50 horas"

    Returns:
        String formatada
    """
    seconds = milliseconds // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if format_type == "verbose":
        parts = []
        if hours > 0:
            parts.append(f"{hours} hora" + ("s" if hours != 1 else ""))
        if minutes > 0:
            parts.append(f"{minutes} minuto" + ("s" if minutes != 1 else ""))
        if secs > 0 or not parts:
            parts.append(f"{secs} segundo" + ("s" if secs != 1 else ""))
        return ", ".join(parts)

    elif format_type == "short":
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        return " ".join(parts)

    elif format_type == "clock":
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    elif format_type == "decimal":
        decimal_hours = seconds / 3600
        return f"{decimal_hours:.2f} horas"

    else:
        raise ValueError(f"Formato desconhecido: {format_type}")


def calculate_billable_time(time_entries: List[Dict]) -> Tuple[int, int]:
    """
    Calcula tempo billable vs não-billable.

    Args:
        time_entries: Lista de time entries

    Returns:
        Tupla (billable_ms, non_billable_ms)
    """
    billable = 0
    non_billable = 0

    for entry in time_entries:
        duration = int(entry.get("duration", 0))
        is_billable = entry.get("billable", False)

        if is_billable:
            billable += duration
        else:
            non_billable += duration

    return (billable, non_billable)


def group_by_task(time_entries: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa time entries por task.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {task_id: [entries]}
    """
    grouped = defaultdict(list)

    for entry in time_entries:
        task = entry.get("task")
        if task:
            task_id = task.get("id")
            if task_id:
                grouped[task_id].append(entry)

    return dict(grouped)


def group_by_user(time_entries: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Agrupa time entries por usuário.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {user_id: [entries]}
    """
    grouped = defaultdict(list)

    for entry in time_entries:
        user = entry.get("user")
        if user:
            user_id = user.get("id")
            if user_id:
                grouped[user_id].append(entry)

    return dict(grouped)


def group_by_date(time_entries: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa time entries por data (YYYY-MM-DD).

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {date_str: [entries]}
    """
    grouped = defaultdict(list)

    for entry in time_entries:
        start = entry.get("start")
        if start:
            # Converter Unix timestamp (ms) para datetime
            dt = datetime.fromtimestamp(int(start) / 1000)
            date_str = dt.strftime("%Y-%m-%d")
            grouped[date_str].append(entry)

    return dict(grouped)


def group_by_tag(time_entries: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Agrupa time entries por tag.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {tag_name: [entries]}
    """
    grouped = defaultdict(list)

    for entry in time_entries:
        tags = entry.get("tags", [])
        if tags:
            for tag in tags:
                tag_name = tag.get("name")
                if tag_name:
                    grouped[tag_name].append(entry)
        else:
            # Entries sem tags
            grouped["_sem_tag"].append(entry)

    return dict(grouped)


def calculate_time_per_task(time_entries: List[Dict]) -> Dict[str, Dict]:
    """
    Calcula tempo total por task com metadados.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {task_id: {
            "task_name": str,
            "total_ms": int,
            "total_formatted": str,
            "entries_count": int
        }}
    """
    grouped = group_by_task(time_entries)
    result = {}

    for task_id, entries in grouped.items():
        total = calculate_total_time(entries)
        task_name = entries[0].get("task", {}).get("name", "Task sem nome")

        result[task_id] = {
            "task_name": task_name,
            "total_ms": total,
            "total_formatted": format_duration(total, "short"),
            "entries_count": len(entries)
        }

    return result


def calculate_time_per_user(time_entries: List[Dict]) -> Dict[int, Dict]:
    """
    Calcula tempo total por usuário.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {user_id: {
            "username": str,
            "total_ms": int,
            "total_formatted": str,
            "entries_count": int,
            "billable_ms": int,
            "non_billable_ms": int
        }}
    """
    grouped = group_by_user(time_entries)
    result = {}

    for user_id, entries in grouped.items():
        total = calculate_total_time(entries)
        billable, non_billable = calculate_billable_time(entries)
        username = entries[0].get("user", {}).get("username", "Usuário desconhecido")

        result[user_id] = {
            "username": username,
            "total_ms": total,
            "total_formatted": format_duration(total, "short"),
            "entries_count": len(entries),
            "billable_ms": billable,
            "non_billable_ms": non_billable
        }

    return result


def calculate_time_per_date(time_entries: List[Dict]) -> Dict[str, Dict]:
    """
    Calcula tempo total por data.

    Args:
        time_entries: Lista de time entries

    Returns:
        Dict {date: {
            "total_ms": int,
            "total_formatted": str,
            "entries_count": int
        }}
    """
    grouped = group_by_date(time_entries)
    result = {}

    for date_str, entries in grouped.items():
        total = calculate_total_time(entries)

        result[date_str] = {
            "total_ms": total,
            "total_formatted": format_duration(total, "short"),
            "entries_count": len(entries)
        }

    return result


def filter_by_date_range(time_entries: List[Dict], start_date: datetime,
                         end_date: datetime) -> List[Dict]:
    """
    Filtra time entries por range de datas.

    Args:
        time_entries: Lista de time entries
        start_date: Data inicial (inclusive)
        end_date: Data final (inclusive)

    Returns:
        Lista filtrada de time entries
    """
    filtered = []

    for entry in time_entries:
        start = entry.get("start")
        if start:
            entry_dt = datetime.fromtimestamp(int(start) / 1000)

            if start_date <= entry_dt <= end_date:
                filtered.append(entry)

    return filtered


def filter_billable_only(time_entries: List[Dict]) -> List[Dict]:
    """Filtra apenas time entries billable."""
    return [e for e in time_entries if e.get("billable", False)]


def filter_by_task(time_entries: List[Dict], task_id: str) -> List[Dict]:
    """Filtra time entries por task específica."""
    return [e for e in time_entries if e.get("task", {}).get("id") == task_id]


def filter_by_user(time_entries: List[Dict], user_id: int) -> List[Dict]:
    """Filtra time entries por usuário específico."""
    return [e for e in time_entries if e.get("user", {}).get("id") == user_id]


def filter_by_tag(time_entries: List[Dict], tag_name: str) -> List[Dict]:
    """Filtra time entries por tag."""
    filtered = []
    for entry in time_entries:
        tags = entry.get("tags", [])
        for tag in tags:
            if tag.get("name") == tag_name:
                filtered.append(entry)
                break
    return filtered


def generate_daily_report(time_entries: List[Dict], date: datetime) -> Dict:
    """
    Gera relatório diário de time tracking.

    Args:
        time_entries: Lista de time entries
        date: Data do relatório

    Returns:
        Dict com estatísticas do dia
    """
    # Filtrar apenas entries da data especificada
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)

    daily_entries = filter_by_date_range(time_entries, start_of_day, end_of_day)

    if not daily_entries:
        return {
            "date": date.strftime("%Y-%m-%d"),
            "total_ms": 0,
            "total_formatted": "0h 0m 0s",
            "entries_count": 0,
            "billable_ms": 0,
            "non_billable_ms": 0,
            "tasks": {},
            "users": {}
        }

    total = calculate_total_time(daily_entries)
    billable, non_billable = calculate_billable_time(daily_entries)
    tasks = calculate_time_per_task(daily_entries)
    users = calculate_time_per_user(daily_entries)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "total_ms": total,
        "total_formatted": format_duration(total, "short"),
        "entries_count": len(daily_entries),
        "billable_ms": billable,
        "non_billable_ms": non_billable,
        "billable_formatted": format_duration(billable, "short"),
        "non_billable_formatted": format_duration(non_billable, "short"),
        "tasks": tasks,
        "users": users
    }


def generate_weekly_report(time_entries: List[Dict], start_date: datetime) -> Dict:
    """
    Gera relatório semanal de time tracking.

    Args:
        time_entries: Lista de time entries
        start_date: Data de início da semana (segunda-feira)

    Returns:
        Dict com estatísticas da semana
    """
    end_date = start_date + timedelta(days=6)
    weekly_entries = filter_by_date_range(time_entries, start_date, end_date)

    if not weekly_entries:
        return {
            "week_start": start_date.strftime("%Y-%m-%d"),
            "week_end": end_date.strftime("%Y-%m-%d"),
            "total_ms": 0,
            "total_formatted": "0h 0m 0s",
            "entries_count": 0,
            "billable_ms": 0,
            "non_billable_ms": 0,
            "daily_breakdown": {},
            "tasks": {},
            "users": {}
        }

    total = calculate_total_time(weekly_entries)
    billable, non_billable = calculate_billable_time(weekly_entries)
    tasks = calculate_time_per_task(weekly_entries)
    users = calculate_time_per_user(weekly_entries)

    # Breakdown por dia
    daily = calculate_time_per_date(weekly_entries)

    return {
        "week_start": start_date.strftime("%Y-%m-%d"),
        "week_end": end_date.strftime("%Y-%m-%d"),
        "total_ms": total,
        "total_formatted": format_duration(total, "short"),
        "entries_count": len(weekly_entries),
        "billable_ms": billable,
        "non_billable_ms": non_billable,
        "billable_formatted": format_duration(billable, "short"),
        "non_billable_formatted": format_duration(non_billable, "short"),
        "daily_breakdown": daily,
        "tasks": tasks,
        "users": users
    }


def calculate_average_daily_time(time_entries: List[Dict],
                                 start_date: datetime,
                                 end_date: datetime) -> int:
    """
    Calcula média de tempo por dia em um período.

    Args:
        time_entries: Lista de time entries
        start_date: Data inicial
        end_date: Data final

    Returns:
        Média de tempo por dia em milissegundos
    """
    filtered = filter_by_date_range(time_entries, start_date, end_date)
    total = calculate_total_time(filtered)

    days = (end_date - start_date).days + 1
    if days == 0:
        return 0

    return total // days


def is_timer_running(timer_data: Optional[Dict]) -> bool:
    """
    Verifica se há um timer ativo.

    Args:
        timer_data: Dados retornados por get_running_timer()

    Returns:
        True se timer está rodando, False caso contrário
    """
    if not timer_data:
        return False

    # Timer ativo tem "start" mas não tem "end"
    has_start = timer_data.get("start") is not None
    has_end = timer_data.get("end") is not None

    return has_start and not has_end


def get_timer_elapsed_time(timer_data: Dict) -> int:
    """
    Calcula tempo decorrido de um timer ativo.

    Args:
        timer_data: Dados do timer retornados pela API

    Returns:
        Tempo decorrido em milissegundos
    """
    if not is_timer_running(timer_data):
        return 0

    start = int(timer_data.get("start", 0))
    now = int(datetime.now().timestamp() * 1000)

    return now - start
