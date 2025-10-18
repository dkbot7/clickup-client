import os
import requests
from dotenv import load_dotenv
from rich import print
from typing import Optional, List, Dict, Any, Union

from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix, fuzzy_time_to_seconds

load_dotenv()


class KaloiClickUpClient:
    """
    Cliente customizado do Sistema Kaloi para integração com a API v2 do ClickUp.

    Funcionalidades:
    - Output formatado com Rich
    - Validação de autenticação com feedback visual
    - Métodos para tarefas, listas, spaces e teams
    - Rate limiting handling
    - Exception handling robusto

    Exemplo de uso:
        client = KaloiClickUpClient()
        client.validate_auth()
        task = client.create_task("list_id", name="Nova Task")
    """

    API_URL = "https://api.clickup.com/api/v2"

    def __init__(self):
        """Inicializa o cliente com token do .env"""
        self.token = os.getenv("CLICKUP_TOKEN")
        self.team_id = os.getenv("CLICKUP_TEAM_ID")
        self.base_url = os.getenv("CLICKUP_BASE_URL", self.API_URL)

        if self.token:
            self.token = self.token.strip()

        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Método interno para fazer requisições HTTP com tratamento de erros.

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API (ex: "task/123")
            **kwargs: Parâmetros adicionais para requests

        Returns:
            JSON response ou None em caso de erro
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)

            if response.status_code == 429:
                print(f"[yellow]⚠ Rate limit atingido. Aguarde alguns segundos.[/yellow]")
                return None

            if response.status_code >= 400:
                print(f"[red]✗ Erro {response.status_code}: {response.text}[/red]")
                return None

            return response.json() if response.text else {}

        except Exception as e:
            print(f"[red]✗ Erro na requisição: {str(e)}[/red]")
            return None

    # ================== AUTENTICAÇÃO ==================

    def validate_auth(self) -> Optional[Dict]:
        """
        Valida o token e retorna informações dos workspaces.

        Returns:
            dict com teams ou None em caso de erro
        """
        teams = self.get_teams()

        if teams:
            print(f"[green]✓ Autenticação bem-sucedida com o ClickUp![/green]")
            print(f"[bold]Workspaces disponíveis:[/bold]")

            for team in teams.get("teams", []):
                print(f"  • {team['name']} (ID: {team['id']})")

            return teams
        else:
            print(f"[red]✗ Falha na autenticação[/red]")
            print(f"[yellow]Dica: Verifique se o token no .env é válido[/yellow]")
            return None

    def get_user_info(self) -> Optional[Dict]:
        """
        Obtém informações detalhadas do usuário autenticado.

        Returns:
            dict com dados do usuário
        """
        data = self._request("GET", "user")

        if data and "user" in data:
            user = data["user"]
            print(f"[green]✓ Usuário autenticado:[/green]")
            print(f"  Nome: [bold]{user.get('username', 'N/A')}[/bold]")
            print(f"  E-mail: {user.get('email', 'N/A')}")
            print(f"  ID: {user.get('id', 'N/A')}")

        return data

    # ================== TEAMS / WORKSPACES ==================

    def get_teams(self) -> Optional[Dict]:
        """
        Retorna todos os workspaces (teams) do usuário.

        Returns:
            dict com lista de teams
        """
        return self._request("GET", "team")

    # ================== SPACES ==================

    def get_spaces(self, team_id: Optional[str] = None, archived: bool = False) -> Optional[Dict]:
        """
        Lista todos os spaces de um workspace.

        Args:
            team_id: ID do workspace (usa self.team_id se não fornecido)
            archived: Incluir spaces arquivados

        Returns:
            dict com lista de spaces
        """
        tid = team_id or self.team_id
        params = {"archived": str(archived).lower()}
        return self._request("GET", f"team/{tid}/space", params=params)

    def get_space(self, space_id: str) -> Optional[Dict]:
        """
        Busca um space específico.

        Args:
            space_id: ID do space

        Returns:
            dict com dados do space
        """
        return self._request("GET", f"space/{space_id}")

    # ================== FOLDERS ==================

    def get_folders(self, space_id: str) -> Optional[Dict]:
        """
        Lista todas as pastas de um space.

        Args:
            space_id: ID do space

        Returns:
            dict com lista de folders
        """
        return self._request("GET", f"space/{space_id}/folder")

    def get_folder(self, folder_id: str) -> Optional[Dict]:
        """
        Busca uma pasta específica.

        Args:
            folder_id: ID da pasta

        Returns:
            dict com dados da folder
        """
        return self._request("GET", f"folder/{folder_id}")

    # ================== LISTS ==================

    def get_lists(self, folder_id: str) -> Optional[Dict]:
        """
        Lista todas as listas de uma pasta.

        Args:
            folder_id: ID da pasta

        Returns:
            dict com lista de lists
        """
        return self._request("GET", f"folder/{folder_id}/list")

    def get_folderless_lists(self, space_id: str) -> Optional[Dict]:
        """
        Lista listas sem pasta (folderless) de um space.

        Args:
            space_id: ID do space

        Returns:
            dict com lista de lists
        """
        return self._request("GET", f"space/{space_id}/list")

    def get_list(self, list_id: str) -> Optional[Dict]:
        """
        Busca uma lista específica.

        Args:
            list_id: ID da lista

        Returns:
            dict com dados da list
        """
        return self._request("GET", f"list/{list_id}")

    # ================== TASKS ==================

    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        Busca uma task específica e exibe informações formatadas.

        Args:
            task_id: ID da task

        Returns:
            dict com dados da task
        """
        task = self._request("GET", f"task/{task_id}")

        if task:
            print(f"[cyan]📋 Task: {task.get('name')}[/cyan]")
            print(f"  ID: {task.get('id')}")
            print(f"  Status: {task.get('status', {}).get('status', 'N/A')}")
            print(f"  URL: {task.get('url')}")

        return task

    def get_tasks(self, list_id: str, **filters) -> Optional[Dict]:
        """
        Lista tasks de uma lista com filtros opcionais.

        Args:
            list_id: ID da lista
            **filters: Filtros (archived, page, order_by, etc.)

        Returns:
            dict com lista de tasks
        """
        return self._request("GET", f"list/{list_id}/task", params=filters)

    def create_task(
        self,
        list_id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict]:
        """
        Cria uma nova task com feedback visual.

        Args:
            list_id: ID da lista
            name: Nome/título da task
            description: Descrição opcional
            **kwargs: Outros parâmetros (priority, due_date, assignees, status, tags)

        Suporta datas em linguagem natural para due_date e start_date:
            - "tomorrow", "amanhã"
            - "next week", "próxima semana"
            - "december 1st", "1 de dezembro"
            - ISO 8601: "2024-12-01T00:00:00Z"
            - Unix timestamp: 1701388800000

        Returns:
            dict com dados da task criada
        """
        payload = {"name": name}

        if description:
            payload["description"] = description

        # Converte datas em linguagem natural para Unix timestamp
        if "due_date" in kwargs and isinstance(kwargs["due_date"], str):
            try:
                kwargs["due_date"] = fuzzy_time_to_unix(kwargs["due_date"])
            except Exception as e:
                print(f"[yellow]⚠ Aviso: Não foi possível converter due_date: {e}[/yellow]")

        if "start_date" in kwargs and isinstance(kwargs["start_date"], str):
            try:
                kwargs["start_date"] = fuzzy_time_to_unix(kwargs["start_date"])
            except Exception as e:
                print(f"[yellow]⚠ Aviso: Não foi possível converter start_date: {e}[/yellow]")

        payload.update(kwargs)

        task = self._request("POST", f"list/{list_id}/task", json=payload)

        if task:
            print(f"[green]✓ Task criada com sucesso![/green]")
            print(f"  Nome: [bold]{task.get('name')}[/bold]")
            print(f"  ID: {task.get('id')}")
            print(f"  URL: {task.get('url')}")

        return task

    def update_task(self, task_id: str, **updates) -> Optional[Dict]:
        """
        Atualiza uma task existente.

        Args:
            task_id: ID da task
            **updates: Campos a atualizar (name, description, status, priority, etc.)

        Returns:
            dict com dados da task atualizada
        """
        task = self._request("PUT", f"task/{task_id}", json=updates)

        if task:
            print(f"[green]✓ Task atualizada![/green]")

        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Deleta uma task.

        Args:
            task_id: ID da task

        Returns:
            True se deletada com sucesso
        """
        result = self._request("DELETE", f"task/{task_id}")

        if result is not None:
            print(f"[green]✓ Task deletada[/green]")
            return True

        return False

    # ================== COMMENTS ==================

    def get_task_comments(self, task_id: str) -> Optional[Dict]:
        """
        Lista comentários de uma task.

        Args:
            task_id: ID da task

        Returns:
            dict com lista de comments
        """
        return self._request("GET", f"task/{task_id}/comment")

    def create_task_comment(self, task_id: str, comment_text: str) -> Optional[Dict]:
        """
        Cria um comentário em uma task.

        Args:
            task_id: ID da task
            comment_text: Texto do comentário

        Returns:
            dict com dados do comment criado
        """
        payload = {"comment_text": comment_text}
        return self._request("POST", f"task/{task_id}/comment", json=payload)


# Alias para compatibilidade
ClickUpClient = KaloiClickUpClient
