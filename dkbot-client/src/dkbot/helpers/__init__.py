# -*- coding: utf-8 -*-
"""
Helpers para ClickUp Client Extended
Sistema Kaloi - Funcionalidades Avançadas A-H

Inclui:
- date_utils: Parsing de datas naturais
- translation: Tradução PT/EN automática
- custom_fields: Helpers para Custom Fields (16 tipos)
- time_tracking: Helpers para Time Tracking (cálculos, relatórios)
"""

# Date utils
from .date_utils import fuzzy_time_to_unix, fuzzy_time_to_seconds, parse_date

# Translation
from .translation import (
    translate_params,
    translate_param_name,
    translate_status,
    translate_priority
)

# Custom Fields helpers
from .custom_fields import (
    CustomFieldMapper,
    get_field_value,
    get_all_field_values,
    validate_field_type,
    find_field_by_name,
    find_field_by_id
)

# Time Tracking helpers
from .time_tracking import (
    format_duration,
    calculate_total_time,
    group_by_task,
    group_by_user,
    group_by_date,
    generate_daily_report,
    generate_weekly_report,
    filter_billable_only
)

__all__ = [
    # Date utils
    "fuzzy_time_to_unix",
    "fuzzy_time_to_seconds",
    "parse_date",
    # Translation
    "translate_params",
    "translate_param_name",
    "translate_status",
    "translate_priority",
    # Custom Fields
    "CustomFieldMapper",
    "get_field_value",
    "get_all_field_values",
    "validate_field_type",
    "find_field_by_name",
    "find_field_by_id",
    # Time Tracking
    "format_duration",
    "calculate_total_time",
    "group_by_task",
    "group_by_user",
    "group_by_date",
    "generate_daily_report",
    "generate_weekly_report",
    "filter_billable_only"
]
