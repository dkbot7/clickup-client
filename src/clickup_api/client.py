import os
import requests
from dotenv import load_dotenv
from rich import print
from typing import Optional, List, Dict, Any, Union

from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix, fuzzy_time_to_seconds
from src.clickup_api.helpers.translation import translate_params

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

        Aceita filtros em PORTUGUÊS ou INGLÊS!

        Args:
            list_id: ID da lista
            **filters: Filtros opcionais

        Filtros aceitos (PT ou EN):
            - archived/arquivada: true/false
            - page/página: Número da página
            - order_by/ordenar_por: Campo para ordenação
            - include_closed/incluir_fechadas: true/false
            - subtasks/incluir_subtasks: true/false

        Exemplos:
            # Português
            tasks = client.get_tasks(
                "list_id",
                arquivada=False,
                página=0
            )

            # Inglês
            tasks = client.get_tasks(
                "list_id",
                archived=False,
                page=0
            )

        Returns:
            dict com lista de tasks
        """
        # Traduz filtros PT → EN
        filters_translated = translate_params(filters, to_english=True)
        return self._request("GET", f"list/{list_id}/task", params=filters_translated)

    def create_task(
        self,
        list_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict]:
        """
        Cria uma nova task com feedback visual.

        Aceita parâmetros em PORTUGUÊS ou INGLÊS!

        Args:
            list_id: ID da lista
            name/nome: Nome/título da task
            description/descrição: Descrição opcional
            **kwargs: Outros parâmetros

        Parâmetros aceitos (PT ou EN):
            - priority/prioridade: "urgente"/"alta"/"normal"/"baixa" ou 1/2/3/4
            - status: "fazer"/"em progresso"/"concluído" ou "to do"/"in progress"/"complete"
            - due_date/data_vencimento: "amanhã", "próxima segunda", "tomorrow", "next monday"
            - start_date/data_inicio: Mesmos formatos de data
            - assignees/responsáveis: Lista de IDs de usuários
            - tags/etiquetas: Lista de tags

        Suporta datas em linguagem natural:
            - PT: "amanhã", "próxima semana", "próxima segunda", "1 de dezembro"
            - EN: "tomorrow", "next week", "next monday", "december 1st"
            - ISO 8601: "2024-12-01T00:00:00Z"
            - Unix timestamp: 1701388800000

        Exemplos:
            # Português
            client.create_task(
                list_id="123",
                nome="Reunião importante",
                prioridade="alta",
                status="em progresso",
                data_vencimento="próxima segunda"
            )

            # Inglês
            client.create_task(
                list_id="123",
                name="Important meeting",
                priority="high",
                status="in progress",
                due_date="next monday"
            )

        Returns:
            dict com dados da task criada
        """
        # Monta payload inicial
        payload = {}

        # Aceita "nome" em português
        if name:
            payload["name"] = name
        elif "nome" in kwargs:
            payload["name"] = kwargs.pop("nome")

        if description:
            payload["description"] = description
        elif "descrição" in kwargs or "descricao" in kwargs:
            payload["description"] = kwargs.pop("descrição", kwargs.pop("descricao", None))

        # Traduz parâmetros PT → EN
        kwargs_translated = translate_params(kwargs, to_english=True)

        # Converte datas em linguagem natural para Unix timestamp
        for date_field in ["due_date", "start_date", "data_vencimento", "data_inicio"]:
            if date_field in kwargs_translated and isinstance(kwargs_translated[date_field], str):
                try:
                    kwargs_translated[date_field] = fuzzy_time_to_unix(kwargs_translated[date_field])
                except Exception as e:
                    print(f"[yellow]⚠ Aviso: Não foi possível converter {date_field}: {e}[/yellow]")

        payload.update(kwargs_translated)

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

        Aceita parâmetros em PORTUGUÊS ou INGLÊS!

        Args:
            task_id: ID da task
            **updates: Campos a atualizar

        Parâmetros aceitos (PT ou EN):
            - name/nome: Novo nome
            - description/descrição: Nova descrição
            - status: "fazer"/"em progresso"/"concluído" ou "to do"/"in progress"/"complete"
            - priority/prioridade: "urgente"/"alta"/"normal"/"baixa" ou 1/2/3/4
            - due_date/data_vencimento: Datas em linguagem natural
            - start_date/data_inicio: Datas em linguagem natural

        Exemplos:
            # Português
            client.update_task(
                "task_id",
                status="concluído",
                prioridade="baixa"
            )

            # Inglês
            client.update_task(
                "task_id",
                status="complete",
                priority="low"
            )

        Returns:
            dict com dados da task atualizada
        """
        # Traduz parâmetros PT → EN
        updates_translated = translate_params(updates, to_english=True)

        # Converte datas em linguagem natural
        for date_field in ["due_date", "start_date"]:
            if date_field in updates_translated and isinstance(updates_translated[date_field], str):
                try:
                    updates_translated[date_field] = fuzzy_time_to_unix(updates_translated[date_field])
                except Exception as e:
                    print(f"[yellow]⚠ Aviso: Não foi possível converter {date_field}: {e}[/yellow]")

        task = self._request("PUT", f"task/{task_id}", json=updates_translated)

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
