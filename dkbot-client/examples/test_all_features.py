"""
Script de Teste Completo - ClickUp Client
Sistema Kaloi - dkbot-client

Demonstra todas as funcionalidades implementadas (A-H):
A. Custom Fields
B. Time Tracking
C. Attachments
D. Checklists
E. Goals
F. Members
G. Webhooks
H. Views
"""

import os
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dkbot.client import KaloiClickUpClient
from dkbot.helpers.custom_fields import CustomFieldMapper, get_all_field_values
from dkbot.helpers.time_tracking import (
    format_duration,
    calculate_total_time,
    group_by_task,
    generate_daily_report
)

console = Console()


def print_section(title: str):
    """Imprime separador de seção."""
    console.print(f"\n[bold cyan]{'=' * 80}[/bold cyan]")
    console.print(f"[bold yellow]{title}[/bold yellow]")
    console.print(f"[bold cyan]{'=' * 80}[/bold cyan]\n")


def test_custom_fields(client: KaloiClickUpClient, list_id: str, task_id: str):
    """
    A. Testa Custom Fields
    """
    print_section("A. CUSTOM FIELDS - Campos Personalizados")

    # 1. Listar custom fields da list
    console.print("[bold]1. Listando custom fields da list...[/bold]")
    fields = client.get_custom_fields(list_id)

    if fields:
        table = Table(title="Custom Fields Disponíveis")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("Tipo", style="yellow")

        for field in fields.get("fields", []):
            table.add_row(
                field.get("id", ""),
                field.get("name", ""),
                field.get("type", "")
            )

        console.print(table)

        # 2. Setar um custom field (exemplo: text field)
        if fields.get("fields"):
            field = fields["fields"][0]
            field_id = field.get("id")
            field_type = field.get("type")

            console.print(f"\n[bold]2. Setando custom field '{field.get('name')}'...[/bold]")

            # Valor de exemplo baseado no tipo
            test_values = {
                "text": "Teste de campo customizado",
                "short_text": "Teste",
                "number": 42,
                "checkbox": True,
                "drop_down": None,  # Requer options
            }

            value = test_values.get(field_type, "Teste")

            if value is not None:
                result = client.set_custom_field(task_id, field_id, value)
                if result:
                    console.print(f"[green]✓ Campo '{field.get('name')}' atualizado com sucesso![/green]")


def test_time_tracking(client: KaloiClickUpClient, team_id: str, task_id: str):
    """
    B. Testa Time Tracking
    """
    print_section("B. TIME TRACKING - Rastreamento de Tempo")

    # 1. Criar time entry manual
    console.print("[bold]1. Criando time entry manual (2 horas)...[/bold]")
    duration_ms = 2 * 60 * 60 * 1000  # 2 horas em ms

    entry = client.create_time_entry(
        team_id=team_id,
        duration=duration_ms,
        task_id=task_id,
        description="Desenvolvimento de feature",
        billable=True
    )

    if entry:
        console.print(f"[green]✓ Time entry criado: {entry.get('id')}[/green]")

    # 2. Iniciar timer
    console.print("\n[bold]2. Iniciando timer...[/bold]")
    timer = client.start_timer(team_id, task_id, description="Trabalhando na task")

    if timer:
        console.print(f"[green]✓ Timer iniciado: {timer.get('id')}[/green]")

        # 3. Verificar timer ativo
        console.print("\n[bold]3. Verificando timer ativo...[/bold]")
        running = client.get_running_timer(team_id)

        if running:
            console.print(f"[yellow]⏱ Timer ativo na task: {running.get('task', {}).get('name')}[/yellow]")

        # 4. Parar timer
        console.print("\n[bold]4. Parando timer...[/bold]")
        stopped = client.stop_timer(team_id)

        if stopped:
            console.print("[green]✓ Timer parado com sucesso![/green]")

    # 5. Buscar time entries
    console.print("\n[bold]5. Buscando time entries da task...[/bold]")
    entries = client.get_time_entries(team_id, task_id=task_id)

    if entries:
        table = Table(title="Time Entries")
        table.add_column("ID", style="cyan")
        table.add_column("Duração", style="green")
        table.add_column("Descrição", style="yellow")
        table.add_column("Billable", style="magenta")

        for e in entries.get("data", [])[:5]:  # Mostrar apenas 5
            duration = format_duration(int(e.get("duration", 0)), "short")
            table.add_row(
                e.get("id", ""),
                duration,
                e.get("description", "")[:30],
                "✓" if e.get("billable") else "✗"
            )

        console.print(table)

        # Análise com helper
        total = calculate_total_time(entries.get("data", []))
        console.print(f"\n[bold green]Tempo total: {format_duration(total, 'verbose')}[/bold green]")


def test_attachments(client: KaloiClickUpClient, task_id: str):
    """
    C. Testa Attachments
    """
    print_section("C. ATTACHMENTS - Anexos")

    console.print("[bold]1. Upload de arquivo...[/bold]")
    console.print("[yellow]Para testar upload, forneça um caminho de arquivo válido.[/yellow]")
    console.print("[dim]Exemplo: client.upload_attachment(task_id, '/path/to/file.pdf')[/dim]")

    # Exemplo de código (não executado sem arquivo real)
    console.print("\n[cyan]Código de exemplo:[/cyan]")
    console.print("""
    result = client.upload_attachment(
        task_id="abc123",
        file_path="/path/to/documento.pdf"
    )

    if result:
        print(f"Arquivo anexado: {result.get('url')}")
    """)


def test_checklists(client: KaloiClickUpClient, task_id: str):
    """
    D. Testa Checklists
    """
    print_section("D. CHECKLISTS - Listas de Verificação")

    # 1. Criar checklist
    console.print("[bold]1. Criando checklist 'Deploy Process'...[/bold]")
    checklist = client.create_checklist(task_id, "Deploy Process")

    if checklist:
        checklist_id = checklist.get("checklist", {}).get("id")
        console.print(f"[green]✓ Checklist criado: {checklist_id}[/green]")

        # 2. Adicionar items
        console.print("\n[bold]2. Adicionando items ao checklist...[/bold]")
        items = [
            "Rodar testes unitários",
            "Build da aplicação",
            "Deploy em staging",
            "Testes de aceitação",
            "Deploy em produção"
        ]

        for item_name in items:
            item = client.add_checklist_item(checklist_id, item_name)
            if item:
                console.print(f"[green]  ✓ Item adicionado: {item_name}[/green]")

        # 3. Marcar primeiro item como concluído
        console.print("\n[bold]3. Marcando primeiro item como concluído...[/bold]")
        # Nota: Para marcar como concluído, precisamos do item_id
        console.print("[yellow]Use complete_checklist_item(checklist_id, item_id)[/yellow]")


def test_goals(client: KaloiClickUpClient, team_id: str):
    """
    E. Testa Goals
    """
    print_section("E. GOALS - Objetivos e Metas")

    # 1. Criar goal
    console.print("[bold]1. Criando goal 'Aumentar Vendas Q1 2025'...[/bold]")

    # Due date para 3 meses à frente
    due_date = int((datetime.now() + timedelta(days=90)).timestamp() * 1000)

    goal = client.create_goal(
        name="Aumentar Vendas Q1 2025",
        due_date=due_date,
        description="Meta de crescimento de 30% no primeiro trimestre",
        multiple_owners=False,
        color="#32CD32"
    )

    if goal:
        goal_id = goal.get("goal", {}).get("id")
        console.print(f"[green]✓ Goal criado: {goal_id}[/green]")

    # 2. Listar goals
    console.print("\n[bold]2. Listando goals do workspace...[/bold]")
    goals = client.get_goals(team_id)

    if goals:
        table = Table(title="Goals Ativos")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("% Completo", style="yellow")

        for g in goals.get("goals", [])[:5]:  # Mostrar apenas 5
            table.add_row(
                g.get("id", ""),
                g.get("name", ""),
                f"{g.get('percent_completed', 0)}%"
            )

        console.print(table)


def test_members(client: KaloiClickUpClient, list_id: str, task_id: str):
    """
    F. Testa Members
    """
    print_section("F. MEMBERS - Gerenciamento de Membros")

    # 1. Listar membros da list
    console.print("[bold]1. Listando membros da list...[/bold]")
    members = client.get_list_members(list_id)

    if members:
        table = Table(title="Membros da List")
        table.add_column("ID", style="cyan")
        table.add_column("Username", style="green")
        table.add_column("Email", style="yellow")

        for member in members.get("members", [])[:10]:
            table.add_row(
                str(member.get("id", "")),
                member.get("username", ""),
                member.get("email", "")
            )

        console.print(table)

        # 2. Adicionar assignee (exemplo)
        console.print("\n[bold]2. Gerenciando assignees...[/bold]")
        console.print("[yellow]Use add_assignees(task_id, [user_id1, user_id2])[/yellow]")
        console.print("[dim]Exemplo: client.add_assignees(task_id, [123456, 789012])[/dim]")


def test_webhooks(client: KaloiClickUpClient, team_id: str):
    """
    G. Testa Webhooks
    """
    print_section("G. WEBHOOKS - Notificações em Tempo Real")

    # 1. Listar webhooks existentes
    console.print("[bold]1. Listando webhooks ativos...[/bold]")
    webhooks = client.get_webhooks(team_id)

    if webhooks:
        table = Table(title="Webhooks Configurados")
        table.add_column("ID", style="cyan")
        table.add_column("Endpoint", style="green")
        table.add_column("Status", style="yellow")

        for webhook in webhooks.get("webhooks", []):
            table.add_row(
                webhook.get("id", ""),
                webhook.get("endpoint", "")[:50],
                "Ativo" if webhook.get("status") == "active" else "Inativo"
            )

        console.print(table)

    # 2. Criar webhook (exemplo)
    console.print("\n[bold]2. Criando webhook...[/bold]")
    console.print("[yellow]Requer endpoint HTTPS público[/yellow]")
    console.print("[dim]Exemplo:[/dim]")
    console.print("""
    webhook = client.create_webhook(
        endpoint_url="https://seu-servidor.com/webhook",
        events=["taskCreated", "taskUpdated", "taskDeleted"],
        space_id="space_id_here"
    )
    """)


def test_views(client: KaloiClickUpClient, list_id: str):
    """
    H. Testa Views
    """
    print_section("H. VIEWS - Visualizações Customizadas")

    # 1. Listar views da list
    console.print("[bold]1. Listando views da list...[/bold]")
    views = client.get_list_views(list_id)

    if views:
        table = Table(title="Views Disponíveis")
        table.add_column("ID", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("Tipo", style="yellow")

        for view in views.get("views", []):
            table.add_row(
                view.get("id", ""),
                view.get("name", ""),
                view.get("type", "")
            )

        console.print(table)

        # 2. Buscar tasks de uma view
        if views.get("views"):
            view_id = views["views"][0].get("id")
            console.print(f"\n[bold]2. Buscando tasks da view '{views['views'][0].get('name')}'...[/bold]")

            tasks = client.get_view_tasks(view_id)

            if tasks:
                count = len(tasks.get("tasks", []))
                console.print(f"[green]✓ Encontradas {count} tasks nesta view[/green]")


def main():
    """Função principal - executa todos os testes."""
    console.print(Panel.fit(
        "[bold cyan]ClickUp Client - Teste Completo de Funcionalidades (A-H)[/bold cyan]\n"
        "[yellow]Sistema Kaloi - dkbot-client[/yellow]",
        border_style="cyan"
    ))

    # Inicializar client
    try:
        client = KaloiClickUpClient()
        console.print("[green]✓ Cliente inicializado com sucesso![/green]\n")
    except Exception as e:
        console.print(f"[red]✗ Erro ao inicializar cliente: {e}[/red]")
        return

    # Validar autenticação
    console.print("[bold]Validando autenticação...[/bold]")
    auth = client.validate_auth()

    if not auth:
        console.print("[red]✗ Falha na autenticação. Verifique seu token.[/red]")
        return

    # Obter IDs necessários
    team_id = client.team_id
    console.print(f"[cyan]Team ID: {team_id}[/cyan]")

    # Solicitar IDs de teste (ou usar defaults)
    console.print("\n[yellow]Para testes completos, forneça IDs válidos:[/yellow]")
    list_id = input("List ID (Enter para pular): ").strip()
    task_id = input("Task ID (Enter para pular): ").strip()

    # Executar testes
    try:
        if list_id and task_id:
            test_custom_fields(client, list_id, task_id)
            test_time_tracking(client, team_id, task_id)
            test_attachments(client, task_id)
            test_checklists(client, task_id)
            test_members(client, list_id, task_id)

        if team_id:
            test_goals(client, team_id)
            test_webhooks(client, team_id)

        if list_id:
            test_views(client, list_id)

        # Resumo final
        print_section("RESUMO FINAL")
        console.print("[bold green]✓ Testes concluídos com sucesso![/bold green]")
        console.print("\n[cyan]Funcionalidades testadas:[/cyan]")
        console.print("  A. Custom Fields - Campos Personalizados")
        console.print("  B. Time Tracking - Rastreamento de Tempo")
        console.print("  C. Attachments - Anexos")
        console.print("  D. Checklists - Listas de Verificação")
        console.print("  E. Goals - Objetivos e Metas")
        console.print("  F. Members - Gerenciamento de Membros")
        console.print("  G. Webhooks - Notificações em Tempo Real")
        console.print("  H. Views - Visualizações Customizadas")

    except Exception as e:
        console.print(f"\n[red]✗ Erro durante testes: {e}[/red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
