# -*- coding: utf-8 -*-
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from src.clickup_api.client import KaloiClickUpClient


def main():
    """
    Script principal de teste do Sistema Kaloi - Integração ClickUp

    Testa autenticação e exibe informações do workspace
    """
    print("=" * 60)
    print("Sistema Kaloi - ClickUp Integration Test")
    print("=" * 60)
    print()

    # Inicializa o cliente customizado
    client = KaloiClickUpClient()

    # Valida autenticação e mostra workspaces
    print("Validando autenticacao...")
    print()
    teams = client.validate_auth()

    if teams:
        print()
        print("=" * 60)

        # Obtém informações detalhadas do usuário
        print()
        print("Informacoes do usuario:")
        print()
        client.get_user_info()

        print()
        print("=" * 60)
        print("Cliente ClickUp do Sistema Kaloi esta operacional!")
        print("=" * 60)
    else:
        print()
        print("Falha na autenticacao. Verifique o token no arquivo .env")


if __name__ == "__main__":
    main()
