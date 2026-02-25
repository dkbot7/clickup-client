"""
Google API Client - Calendar, Sheets, Docs, Drive
Suporta leitura de credenciais via arquivo local ou variável de ambiente (GitHub Actions).
"""
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    # GitHub Actions: JSON completo na variável de ambiente
    json_content = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON_CONTENT")
    if json_content:
        info = json.loads(json_content)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    # Local: caminho para o arquivo JSON
    json_path = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_JSON",
        "credentials/google_service_account.json"
    )
    return service_account.Credentials.from_service_account_file(json_path, scopes=SCOPES)


def get_calendar_service():
    return build("calendar", "v3", credentials=get_credentials())


def get_sheets_service():
    return build("sheets", "v4", credentials=get_credentials())


def get_docs_service():
    return build("docs", "v1", credentials=get_credentials())


def get_drive_service():
    return build("drive", "v3", credentials=get_credentials())
