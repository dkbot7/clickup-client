# -*- coding: utf-8 -*-
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix, fuzzy_time_to_seconds
from datetime import datetime


def test_fuzzy_dates():
    """
    Testa parsing de datas em linguagem natural (português e inglês)
    """
    print("=" * 70)
    print("TESTE DE DATAS EM LINGUAGEM NATURAL - Sistema Kaloi")
    print("=" * 70)
    print()

    # Testes em INGLÊS
    print("[INGLÊS] Exemplos de datas naturais:")
    print("-" * 70)

    test_cases_en = [
        "tomorrow",
        "next week",
        "next friday",
        "december 1st",
        "in 3 days",
        "2024-12-25",
    ]

    for date_str in test_cases_en:
        try:
            timestamp = fuzzy_time_to_unix(date_str)
            dt = datetime.fromtimestamp(timestamp / 1000)
            print(f"'{date_str:20}' -> {timestamp:15} -> {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"'{date_str:20}' -> ERRO: {e}")

    print()

    # Testes em PORTUGUÊS
    print("[PORTUGUÊS] Exemplos de datas naturais:")
    print("-" * 70)

    test_cases_pt = [
        "amanhã",
        "próxima semana",
        "próxima sexta",
        "1 de dezembro",
        "em 3 dias",
        "daqui a 2 semanas",
    ]

    for date_str in test_cases_pt:
        try:
            timestamp = fuzzy_time_to_unix(date_str)
            dt = datetime.fromtimestamp(timestamp / 1000)
            print(f"'{date_str:20}' -> {timestamp:15} -> {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"'{date_str:20}' -> ERRO: {e}")

    print()
    print("=" * 70)

    # Testes de DURAÇÕES
    print()
    print("[DURAÇÕES] Conversão para segundos:")
    print("-" * 70)

    duration_tests = [
        "2 hours",
        "30 minutes",
        "1 day",
        "2 horas",
        "30 minutos",
        "1 dia",
        "1 week",
        "1 semana",
    ]

    for duration_str in duration_tests:
        try:
            seconds = fuzzy_time_to_seconds(duration_str)
            hours = seconds / 3600
            print(f"'{duration_str:20}' -> {seconds:8} segundos ({hours:.2f} horas)")
        except Exception as e:
            print(f"'{duration_str:20}' -> ERRO: {e}")

    print()
    print("=" * 70)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 70)


if __name__ == "__main__":
    test_fuzzy_dates()
