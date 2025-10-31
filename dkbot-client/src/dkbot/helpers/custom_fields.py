"""
Custom Fields Helper - ClickUp API Client
Sistema Kaloi - dkbot-client

Helpers para trabalhar com Custom Fields do ClickUp.
Suporta 16 tipos de campos personalizados.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class CustomFieldMapper:
    """
    Mapeia valores Python para formato ClickUp Custom Fields.

    Suporta 16 tipos de campos:
    - text (short_text)
    - textarea (long_text)
    - number
    - currency
    - dropdown
    - labels (multi-select)
    - email
    - url
    - phone
    - date
    - checkbox
    - rating
    - location
    - users
    - automatic_progress
    - manual_progress
    """

    # Mapa de tipos Python -> ClickUp field type
    TYPE_MAP = {
        str: ["text", "textarea", "email", "url", "phone", "location"],
        int: ["number", "rating", "currency"],
        float: ["number", "currency"],
        bool: ["checkbox"],
        list: ["dropdown", "labels", "users"],
        datetime: ["date"],
    }

    @staticmethod
    def format_text(value: str) -> Dict[str, Any]:
        """Formata campo de texto curto."""
        return {"value": str(value)}

    @staticmethod
    def format_textarea(value: str) -> Dict[str, Any]:
        """Formata campo de texto longo."""
        return {"value": str(value)}

    @staticmethod
    def format_number(value: float) -> Dict[str, Any]:
        """Formata campo numérico."""
        return {"value": float(value)}

    @staticmethod
    def format_currency(value: float) -> Dict[str, Any]:
        """Formata campo de moeda (em centavos)."""
        # ClickUp espera valores em centavos
        cents = int(value * 100)
        return {"value": cents}

    @staticmethod
    def format_dropdown(value: str, options: List[Dict]) -> Dict[str, Any]:
        """
        Formata campo dropdown.

        Args:
            value: Label da opção selecionada
            options: Lista de opções disponíveis do campo

        Returns:
            Dict com value_options contendo o UUID da opção
        """
        # Encontrar UUID da opção pelo label
        option_uuid = None
        for opt in options:
            if opt.get("label") == value or opt.get("name") == value:
                option_uuid = opt.get("id") or opt.get("orderindex")
                break

        if not option_uuid:
            raise ValueError(f"Opção '{value}' não encontrada nas opções disponíveis")

        return {"value": option_uuid}

    @staticmethod
    def format_labels(values: List[str], options: List[Dict]) -> Dict[str, Any]:
        """
        Formata campo labels (multi-select).

        Args:
            values: Lista de labels selecionados
            options: Lista de opções disponíveis do campo

        Returns:
            Dict com value contendo lista de UUIDs
        """
        uuids = []
        for val in values:
            for opt in options:
                if opt.get("label") == val or opt.get("name") == val:
                    uuid = opt.get("id") or opt.get("orderindex")
                    uuids.append(uuid)
                    break

        if len(uuids) != len(values):
            raise ValueError(f"Algumas opções não foram encontradas: {values}")

        return {"value": uuids}

    @staticmethod
    def format_email(value: str) -> Dict[str, Any]:
        """Formata campo de email."""
        # Validação básica de email
        if "@" not in value:
            raise ValueError(f"Email inválido: {value}")
        return {"value": str(value)}

    @staticmethod
    def format_url(value: str) -> Dict[str, Any]:
        """Formata campo de URL."""
        # Validação básica de URL
        if not value.startswith(("http://", "https://")):
            raise ValueError(f"URL deve começar com http:// ou https://: {value}")
        return {"value": str(value)}

    @staticmethod
    def format_phone(value: str) -> Dict[str, Any]:
        """Formata campo de telefone."""
        return {"value": str(value)}

    @staticmethod
    def format_date(value: datetime) -> Dict[str, Any]:
        """
        Formata campo de data.

        Args:
            value: datetime Python

        Returns:
            Dict com timestamp Unix em milissegundos
        """
        timestamp_ms = int(value.timestamp() * 1000)
        return {"value": timestamp_ms}

    @staticmethod
    def format_checkbox(value: bool) -> Dict[str, Any]:
        """Formata campo checkbox."""
        return {"value": bool(value)}

    @staticmethod
    def format_rating(value: int, max_rating: int = 5) -> Dict[str, Any]:
        """
        Formata campo de rating (0-5).

        Args:
            value: Rating de 0 a max_rating
            max_rating: Rating máximo (padrão 5)
        """
        if not 0 <= value <= max_rating:
            raise ValueError(f"Rating deve estar entre 0 e {max_rating}")
        return {"value": int(value)}

    @staticmethod
    def format_location(value: str) -> Dict[str, Any]:
        """Formata campo de localização."""
        return {
            "value": {
                "location": str(value),
                "lat": None,
                "lng": None
            }
        }

    @staticmethod
    def format_users(user_ids: List[int]) -> Dict[str, Any]:
        """
        Formata campo de usuários.

        Args:
            user_ids: Lista de IDs de usuários (integers)
        """
        return {
            "value": {
                "add": [int(uid) for uid in user_ids],
                "rem": []
            }
        }

    @staticmethod
    def format_progress(value: int, field_type: str = "manual_progress") -> Dict[str, Any]:
        """
        Formata campo de progresso (0-100).

        Args:
            value: Progresso de 0 a 100
            field_type: "manual_progress" ou "automatic_progress"
        """
        if not 0 <= value <= 100:
            raise ValueError("Progresso deve estar entre 0 e 100")

        if field_type == "automatic_progress":
            raise ValueError("Automatic progress é calculado automaticamente pelo ClickUp")

        return {"value": int(value)}


def get_field_value(field_data: Dict) -> Any:
    """
    Extrai valor de um custom field retornado pela API.

    Args:
        field_data: Dados do campo retornados pela API

    Returns:
        Valor do campo em formato Python nativo
    """
    field_type = field_data.get("type")
    value = field_data.get("value")

    if value is None:
        return None

    # Text/textarea/email/url/phone/location
    if field_type in ["text", "short_text", "textarea", "long_text", "email", "url", "phone"]:
        return str(value)

    # Number/rating
    if field_type in ["number", "rating"]:
        return float(value) if "." in str(value) else int(value)

    # Currency (converter de centavos para reais)
    if field_type == "currency":
        return int(value) / 100

    # Checkbox
    if field_type == "checkbox":
        return bool(value)

    # Date (converter de Unix ms para datetime)
    if field_type == "date":
        return datetime.fromtimestamp(int(value) / 1000)

    # Dropdown
    if field_type == "drop_down":
        # value é o UUID, precisamos pegar o label das type_config.options
        options = field_data.get("type_config", {}).get("options", [])
        for opt in options:
            if opt.get("id") == value or opt.get("orderindex") == value:
                return opt.get("label") or opt.get("name")
        return value

    # Labels (multi-select)
    if field_type == "labels":
        options = field_data.get("type_config", {}).get("options", [])
        labels = []
        for val_uuid in value:
            for opt in options:
                if opt.get("id") == val_uuid or opt.get("orderindex") == val_uuid:
                    labels.append(opt.get("label") or opt.get("name"))
                    break
        return labels

    # Users
    if field_type == "users":
        # value já é lista de user objects
        return [u.get("id") for u in value] if isinstance(value, list) else []

    # Location
    if field_type == "location":
        if isinstance(value, dict):
            return value.get("location", "")
        return str(value)

    # Progress
    if field_type in ["manual_progress", "automatic_progress"]:
        return int(value.get("percent_complete", 0)) if isinstance(value, dict) else int(value)

    # Fallback
    return value


def get_all_field_values(custom_fields: List[Dict]) -> Dict[str, Any]:
    """
    Extrai todos os valores de custom fields em um dict.

    Args:
        custom_fields: Lista de custom fields da task

    Returns:
        Dict com {field_name: field_value}
    """
    result = {}
    for field in custom_fields:
        field_name = field.get("name")
        field_value = get_field_value(field)
        result[field_name] = field_value

    return result


def validate_field_type(field_type: str, value: Any) -> bool:
    """
    Valida se o valor é compatível com o tipo de campo.

    Args:
        field_type: Tipo do campo ClickUp
        value: Valor a validar

    Returns:
        True se válido, False caso contrário
    """
    type_validators = {
        "text": lambda v: isinstance(v, str),
        "short_text": lambda v: isinstance(v, str),
        "textarea": lambda v: isinstance(v, str),
        "long_text": lambda v: isinstance(v, str),
        "number": lambda v: isinstance(v, (int, float)),
        "currency": lambda v: isinstance(v, (int, float)),
        "email": lambda v: isinstance(v, str) and "@" in v,
        "url": lambda v: isinstance(v, str) and v.startswith(("http://", "https://")),
        "phone": lambda v: isinstance(v, str),
        "checkbox": lambda v: isinstance(v, bool),
        "date": lambda v: isinstance(v, (datetime, int)),
        "rating": lambda v: isinstance(v, int) and 0 <= v <= 5,
        "drop_down": lambda v: isinstance(v, str),
        "labels": lambda v: isinstance(v, list),
        "users": lambda v: isinstance(v, list),
        "location": lambda v: isinstance(v, str),
        "manual_progress": lambda v: isinstance(v, int) and 0 <= v <= 100,
        "automatic_progress": lambda v: False,  # Não pode ser setado manualmente
    }

    validator = type_validators.get(field_type)
    if not validator:
        return False

    return validator(value)


def find_field_by_name(custom_fields: List[Dict], field_name: str) -> Optional[Dict]:
    """
    Encontra um custom field pelo nome.

    Args:
        custom_fields: Lista de custom fields
        field_name: Nome do campo a buscar

    Returns:
        Dict com dados do campo ou None se não encontrado
    """
    for field in custom_fields:
        if field.get("name") == field_name:
            return field
    return None


def find_field_by_id(custom_fields: List[Dict], field_id: str) -> Optional[Dict]:
    """
    Encontra um custom field pelo ID.

    Args:
        custom_fields: Lista de custom fields
        field_id: ID do campo a buscar

    Returns:
        Dict com dados do campo ou None se não encontrado
    """
    for field in custom_fields:
        if field.get("id") == field_id:
            return field
    return None
