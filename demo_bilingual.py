# -*- coding: utf-8 -*-
"""
Script de demonstração: Uso bilíngue do ClickUp Client

Mostra como o cliente aceita parâmetros em português E inglês.
"""

import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == "win32":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding='utf-8')

from src.clickup_api.client import KaloiClickUpClient
from rich import print


def demo_traducao():
    """Demonstra tradução de parâmetros PT → EN"""
    print("\n" + "=" * 70)
    print("[bold cyan]DEMONSTRAÇÃO: Cliente ClickUp Bilíngue (PT/EN)[/bold cyan]")
    print("=" * 70 + "\n")

    # Inicializa cliente
    client = KaloiClickUpClient()

    # Valida autenticação
    print("[bold]1. Validando autenticação...[/bold]")
    client.validate_auth()

    print("\n" + "-" * 70)
    print("[bold]2. Exemplos de uso em PORTUGUÊS:[/bold]\n")

    # Exemplo 1: Criar task em português
    print("[cyan]Exemplo 1: Criar task com parâmetros em português[/cyan]")
    print("""
client.create_task(
    list_id="sua_lista_id",
    nome="Reunião importante",
    descrição="Discutir projeto Q1 2025",
    prioridade="alta",
    status="em progresso",
    data_vencimento="próxima segunda"
)
    """)

    # Exemplo 2: Atualizar task em português
    print("\n[cyan]Exemplo 2: Atualizar task em português[/cyan]")
    print("""
client.update_task(
    "task_id",
    status="concluído",
    prioridade="baixa"
)
    """)

    # Exemplo 3: Buscar tasks com filtros em português
    print("\n[cyan]Exemplo 3: Buscar tasks com filtros em português[/cyan]")
    print("""
tasks = client.get_tasks(
    "list_id",
    arquivada=False,
    página=0,
    ordenar_por="updated"
)
    """)

    print("\n" + "-" * 70)
    print("[bold]3. Exemplos de uso em INGLÊS:[/bold]\n")

    # Exemplo 4: Criar task em inglês
    print("[cyan]Exemplo 4: Criar task com parâmetros em inglês[/cyan]")
    print("""
client.create_task(
    list_id="your_list_id",
    name="Important meeting",
    description="Discuss Q1 2025 project",
    priority="high",
    status="in progress",
    due_date="next monday"
)
    """)

    # Exemplo 5: Atualizar task em inglês
    print("\n[cyan]Exemplo 5: Atualizar task em inglês[/cyan]")
    print("""
client.update_task(
    "task_id",
    status="complete",
    priority="low"
)
    """)

    # Exemplo 6: Buscar tasks com filtros em inglês
    print("\n[cyan]Exemplo 6: Buscar tasks com filtros em inglês[/cyan]")
    print("""
tasks = client.get_tasks(
    "list_id",
    archived=False,
    page=0,
    order_by="updated"
)
    """)

    print("\n" + "-" * 70)
    print("[bold]4. Tabela de Traduções:[/bold]\n")

    print("[yellow]PARÂMETROS:[/yellow]")
    print("  PT               →  EN")
    print("  nome             →  name")
    print("  descrição        →  description")
    print("  prioridade       →  priority")
    print("  data_vencimento  →  due_date")
    print("  data_inicio      →  start_date")
    print("  responsáveis     →  assignees")
    print("  etiquetas        →  tags")
    print("  arquivada        →  archived")
    print("  página           →  page")
    print("  ordenar_por      →  order_by")

    print("\n[yellow]VALORES DE STATUS:[/yellow]")
    print("  PT               →  EN")
    print("  fazer            →  to do")
    print("  pendente         →  to do")
    print("  em progresso     →  in progress")
    print("  em revisão       →  in review")
    print("  concluído        →  complete")
    print("  fechado          →  closed")

    print("\n[yellow]VALORES DE PRIORIDADE:[/yellow]")
    print("  PT               →  EN (Número)")
    print("  urgente          →  1")
    print("  alta             →  2")
    print("  normal           →  3")
    print("  baixa            →  4")

    print("\n[yellow]DATAS EM LINGUAGEM NATURAL:[/yellow]")
    print("  PT                    →  EN")
    print("  amanhã                →  tomorrow")
    print("  próxima semana        →  next week")
    print("  próxima segunda       →  next monday")
    print("  próxima sexta         →  next friday")
    print("  em 3 dias             →  in 3 days")
    print("  1 de dezembro         →  december 1st")

    print("\n" + "=" * 70)
    print("[bold green]✓ Demonstração concluída![/bold green]")
    print("[green]O cliente traduz automaticamente PT → EN antes de enviar à API[/green]")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    demo_traducao()
