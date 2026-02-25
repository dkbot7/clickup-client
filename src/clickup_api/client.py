import os
import requests
from dotenv import load_dotenv
from rich import print
from typing import Optional, List, Dict, Any, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

        # Configurar session com retry automático
        self.session = requests.Session()

        # Estratégia de retry com backoff exponencial
        retries = Retry(
            total=5,  # Máximo de 5 tentativas
            backoff_factor=1,  # Backoff exponencial: 0.5s, 1s, 2s, 4s, 8s
            status_forcelist=[429, 500, 502, 503, 504],  # Status codes para retry
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]  # Métodos HTTP
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Método interno para fazer requisições HTTP com tratamento de erros.

        Features:
        - Retry automático com backoff exponencial
        - Tratamento de rate limiting (429)
        - Handling de erros HTTP

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API (ex: "task/123")
            **kwargs: Parâmetros adicionais para requests

        Returns:
            JSON response ou None em caso de erro
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            # Usar session com retry automático
            response = self.session.request(method, url, headers=self.headers, **kwargs)

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

    def _get_all_paginated(
        self,
        endpoint: str,
        data_key: str = "tasks",
        **params
    ) -> List[Dict]:
        """
        Helper genérico para buscar todos os itens com paginação automática.

        A API do ClickUp limita respostas a 100 itens por página.
        Este método busca todas as páginas automaticamente.

        Args:
            endpoint: Endpoint da API (ex: "list/123/task")
            data_key: Chave dos dados na response (ex: "tasks", "lists", "spaces")
            **params: Parâmetros adicionais da requisição

        Returns:
            Lista completa de items de todas as páginas

        Example:
            >>> all_tasks = client._get_all_paginated("list/123/task", "tasks")
            >>> print(f"Total: {len(all_tasks)} tasks")
        """
        all_items = []
        page = 0

        while True:
            # Adicionar número da página aos parâmetros
            params["page"] = page

            # Fazer requisição
            response = self._request("GET", endpoint, params=params)

            # Verificar se há dados
            if not response or data_key not in response:
                break

            items = response[data_key]
            all_items.extend(items)

            # Verificar se é a última página
            # ClickUp retorna last_page=true ou menos de 100 itens
            is_last_page = response.get("last_page", False)
            has_less_than_limit = len(items) < 100

            if is_last_page or has_less_than_limit:
                break

            page += 1

        return all_items

    def _iter_paginated(
        self,
        endpoint: str,
        data_key: str = "tasks",
        **params
    ):
        """
        Generator para iterar sobre items paginados (lazy loading).

        Mais eficiente em memória que _get_all_paginated para grandes volumes.

        Args:
            endpoint: Endpoint da API
            data_key: Chave dos dados na response
            **params: Parâmetros adicionais

        Yields:
            Dict: Item individual

        Example:
            >>> for task in client._iter_paginated("list/123/task", "tasks"):
            ...     process_task(task)
        """
        page = 0

        while True:
            params["page"] = page
            response = self._request("GET", endpoint, params=params)

            if not response or data_key not in response:
                break

            items = response[data_key]

            for item in items:
                yield item

            is_last_page = response.get("last_page", False)
            has_less_than_limit = len(items) < 100

            if is_last_page or has_less_than_limit:
                break

            page += 1

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

    def get_tasks(
        self,
        list_id: str,
        paginate: bool = False,
        **filters
    ) -> Union[Optional[Dict], List[Dict]]:
        """
        Lista tasks de uma lista com filtros opcionais.

        Aceita filtros em PORTUGUÊS ou INGLÊS!

        Args:
            list_id: ID da lista
            paginate: Se True, busca TODAS as páginas automaticamente
            **filters: Filtros opcionais

        Filtros aceitos (PT ou EN):
            - archived/arquivada: true/false
            - page/página: Número da página (ignorado se paginate=True)
            - order_by/ordenar_por: Campo para ordenação
            - include_closed/incluir_fechadas: true/false
            - subtasks/incluir_subtasks: true/false

        Exemplos:
            # Buscar primeira página (padrão)
            tasks = client.get_tasks("list_id", arquivada=False)

            # Buscar TODAS as tasks (paginação automática)
            all_tasks = client.get_tasks("list_id", paginate=True)
            print(f"Total: {len(all_tasks)} tasks")

            # Com filtros em português
            tasks = client.get_tasks(
                "list_id",
                paginate=True,
                arquivada=False,
                incluir_fechadas=False
            )

        Returns:
            Se paginate=False: dict com lista de tasks (1 página)
            Se paginate=True: list com TODAS as tasks (todas as páginas)
        """
        # Traduz filtros PT → EN
        filters_translated = translate_params(filters, to_english=True)

        if paginate:
            # Buscar todas as páginas automaticamente
            return self._get_all_paginated(
                f"list/{list_id}/task",
                data_key="tasks",
                **filters_translated
            )
        else:
            # Buscar apenas 1 página
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

    def post_task_comment(self, task_id: str, comment_text: str) -> Optional[Dict]:
        """Alias de create_task_comment para compatibilidade com scripts de automacao."""
        return self.create_task_comment(task_id, comment_text)

    def add_tag(self, task_id: str, tag_name: str) -> bool:
        """
        Adiciona uma tag a uma task.

        Args:
            task_id: ID da task
            tag_name: Nome da tag

        Returns:
            True se sucesso, False caso contrario
        """
        result = self._request("POST", f"task/{task_id}/tag/{tag_name}")
        return result is not None

    def remove_tag(self, task_id: str, tag_name: str) -> bool:
        """
        Remove uma tag de uma task.

        Args:
            task_id: ID da task
            tag_name: Nome da tag

        Returns:
            True se sucesso, False caso contrario
        """
        result = self._request("DELETE", f"task/{task_id}/tag/{tag_name}")
        return result is not None

    # ================== A. CUSTOM FIELDS ==================

    def get_custom_fields(self, list_id: str) -> Optional[Dict]:
        """
        Obtém todos os custom fields de uma lista.

        Args:
            list_id: ID da lista

        Returns:
            dict com lista de custom fields
        """
        return self._request("GET", f"list/{list_id}/field")

    def set_custom_field(
        self,
        task_id: str,
        field_id: str,
        value: Any,
        **kwargs
    ) -> Optional[Dict]:
        """
        Define valor de um custom field em uma task.

        Args:
            task_id: ID da task
            field_id: UUID do custom field
            value: Valor a ser definido
            **kwargs: Parâmetros adicionais (ex: time=True para datas)

        Returns:
            dict com custom field atualizado
        """
        payload = {"value": value}
        payload.update(kwargs)

        result = self._request("POST", f"task/{task_id}/field/{field_id}", json=payload)

        if result:
            print(f"[green]✓ Custom field atualizado![/green]")

        return result

    def set_multiple_custom_fields(
        self,
        task_id: str,
        fields: Dict[str, Any]
    ) -> List[Optional[Dict]]:
        """
        Define múltiplos custom fields de uma task.

        Args:
            task_id: ID da task
            fields: Dicionário {field_id: value}

        Returns:
            Lista com resultados
        """
        results = []
        print(f"[yellow]⚠ Atualizando {len(fields)} custom fields...[/yellow]")

        for field_id, value in fields.items():
            result = self.set_custom_field(task_id, field_id, value)
            results.append(result)

        successful = sum(1 for r in results if r is not None)
        print(f"[green]✓ {successful}/{len(fields)} custom fields atualizados[/green]")

        return results

    # ================== B. TIME TRACKING ==================

    def create_time_entry(
        self,
        team_id: Optional[str] = None,
        duration: int = None,
        task_id: Optional[str] = None,
        description: Optional[str] = None,
        billable: bool = False,
        start: Optional[int] = None,
        tags: Optional[List[Dict]] = None
    ) -> Optional[Dict]:
        """
        Cria um registro de tempo manualmente.

        Args:
            team_id: ID do workspace
            duration: Duração em MILISSEGUNDOS
            task_id: ID da task
            description: Descrição do trabalho
            billable: Se é faturável
            start: Timestamp Unix em ms
            tags: Lista de tags

        Returns:
            dict com time entry criado
        """
        tid = team_id or self.team_id

        if not duration:
            print("[red]✗ Duração é obrigatória[/red]")
            return None

        payload = {"duration": duration, "billable": billable}

        if task_id:
            payload["tid"] = task_id
        if description:
            payload["description"] = description
        if start:
            payload["start"] = start
        if tags:
            payload["tags"] = tags

        result = self._request("POST", f"team/{tid}/time_entries", json=payload)

        if result:
            duration_hours = duration / 1000 / 3600
            print(f"[green]✓ Time entry criado: {duration_hours:.2f}h[/green]")

        return result

    def start_timer(
        self,
        task_id: str,
        team_id: Optional[str] = None,
        description: Optional[str] = None,
        billable: bool = False,
        tags: Optional[List[Dict]] = None
    ) -> Optional[Dict]:
        """
        Inicia um timer em tempo real.

        Args:
            task_id: ID da task
            team_id: ID do workspace
            description: Descrição
            billable: Se é faturável
            tags: Tags do time entry

        Returns:
            dict com timer iniciado
        """
        tid = team_id or self.team_id

        payload = {"tid": task_id, "billable": billable}

        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = tags

        result = self._request("POST", f"team/{tid}/time_entries/start", json=payload)

        if result:
            print(f"[green]✓ Timer iniciado na task {task_id}[/green]")

        return result

    def stop_timer(self, team_id: Optional[str] = None) -> Optional[Dict]:
        """
        Para o timer em execução.

        Args:
            team_id: ID do workspace

        Returns:
            dict com timer parado
        """
        tid = team_id or self.team_id

        result = self._request("POST", f"team/{tid}/time_entries/stop")

        if result:
            duration_ms = int(result.get("duration", 0))
            duration_hours = duration_ms / 1000 / 3600
            print(f"[green]✓ Timer parado: {duration_hours:.2f}h registradas[/green]")

        return result

    def get_running_timer(self, team_id: Optional[str] = None) -> Optional[Dict]:
        """
        Obtém o timer atualmente em execução.

        Args:
            team_id: ID do workspace

        Returns:
            dict com timer rodando ou None
        """
        tid = team_id or self.team_id

        result = self._request("GET", f"team/{tid}/time_entries/current")

        if result and result.get("data"):
            timer = result["data"][0] if isinstance(result["data"], list) else result["data"]
            print(f"[yellow]⏱ Timer rodando: {timer.get('description', 'Sem descrição')}[/yellow]")
            return timer

        print("[blue]ℹ Nenhum timer em execução[/blue]")
        return None

    def get_time_entries(
        self,
        team_id: Optional[str] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        assignee: Optional[List[int]] = None,
        task_id: Optional[str] = None,
        **filters
    ) -> Optional[Dict]:
        """
        Busca time entries filtrados.

        Args:
            team_id: ID do workspace
            start_date: Timestamp Unix em ms
            end_date: Timestamp Unix em ms
            assignee: Lista de user IDs
            task_id: ID da task
            **filters: Outros filtros

        Returns:
            dict com lista de time entries
        """
        from datetime import datetime, timedelta

        tid = team_id or self.team_id

        params = {}

        if not start_date:
            start_date = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)
        if not end_date:
            end_date = int(datetime.now().timestamp() * 1000)

        params["start_date"] = start_date
        params["end_date"] = end_date

        if assignee:
            params["assignee"] = ",".join(map(str, assignee))
        if task_id:
            params["task_id"] = task_id

        params.update(filters)

        result = self._request("GET", f"team/{tid}/time_entries", params=params)

        if result:
            count = len(result.get("data", []))
            print(f"[green]✓ {count} time entries encontrados[/green]")

        return result

    def update_time_entry(
        self,
        timer_id: str,
        team_id: Optional[str] = None,
        **updates
    ) -> Optional[Dict]:
        """
        Atualiza um time entry.

        Args:
            timer_id: ID do time entry
            team_id: ID do workspace
            **updates: Campos a atualizar

        Returns:
            dict com time entry atualizado
        """
        tid = team_id or self.team_id

        result = self._request("PUT", f"team/{tid}/time_entries/{timer_id}", json=updates)

        if result:
            print(f"[green]✓ Time entry atualizado[/green]")

        return result

    def delete_time_entry(
        self,
        timer_id: str,
        team_id: Optional[str] = None
    ) -> bool:
        """
        Deleta um time entry.

        Args:
            timer_id: ID do time entry
            team_id: ID do workspace

        Returns:
            True se deletado
        """
        tid = team_id or self.team_id

        result = self._request("DELETE", f"team/{tid}/time_entries/{timer_id}")

        if result is not None:
            print(f"[green]✓ Time entry deletado[/green]")
            return True

        return False

    # ================== C. ATTACHMENTS ==================

    def upload_attachment(self, task_id: str, file_path: str) -> Optional[Dict]:
        """
        Faz upload de anexo para uma task.

        Args:
            task_id: ID da task
            file_path: Caminho do arquivo local

        Returns:
            dict com dados do attachment
        """
        import os

        if not os.path.exists(file_path):
            print(f"[red]✗ Arquivo não encontrado: {file_path}[/red]")
            return None

        filename = os.path.basename(file_path)

        # Para upload, usar headers sem Content-Type (requests define automaticamente)
        headers = {"Authorization": self.token}

        with open(file_path, 'rb') as f:
            files = {"attachment": (filename, f)}

            url = f"{self.base_url}/task/{task_id}/attachment"

            try:
                response = requests.post(url, files=files, headers=headers)

                if response.status_code >= 400:
                    print(f"[red]✗ Erro {response.status_code}: {response.text}[/red]")
                    return None

                result = response.json() if response.text else {}

                if result:
                    print(f"[green]✓ Anexo enviado: {filename}[/green]")

                return result

            except Exception as e:
                print(f"[red]✗ Erro no upload: {str(e)}[/red]")
                return None

    # ================== D. CHECKLISTS ==================

    def create_checklist(self, task_id: str, name: str) -> Optional[Dict]:
        """
        Cria checklist em uma task.

        Args:
            task_id: ID da task
            name: Nome do checklist

        Returns:
            dict com checklist criado
        """
        payload = {"name": name}
        result = self._request("POST", f"task/{task_id}/checklist", json=payload)

        if result:
            print(f"[green]✓ Checklist criada: {name}[/green]")

        return result

    def add_checklist_item(
        self,
        checklist_id: str,
        name: str,
        assignee: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Adiciona item a um checklist.

        Args:
            checklist_id: ID do checklist
            name: Nome do item
            assignee: User ID (opcional)

        Returns:
            dict com item criado
        """
        payload = {"name": name}

        if assignee:
            payload["assignee"] = assignee

        result = self._request("POST", f"checklist/{checklist_id}/checklist_item", json=payload)

        if result:
            print(f"[green]✓ Item adicionado: {name}[/green]")

        return result

    def complete_checklist_item(
        self,
        checklist_id: str,
        item_id: str
    ) -> Optional[Dict]:
        """
        Marca item como concluído.

        Args:
            checklist_id: ID do checklist
            item_id: ID do item

        Returns:
            dict com item atualizado
        """
        return self._request(
            "PUT",
            f"checklist/{checklist_id}/checklist_item/{item_id}",
            json={"resolved": True}
        )

    def delete_checklist(self, checklist_id: str) -> bool:
        """
        Deleta um checklist.

        Args:
            checklist_id: ID do checklist

        Returns:
            True se deletado
        """
        result = self._request("DELETE", f"checklist/{checklist_id}")

        if result is not None:
            print(f"[green]✓ Checklist deletado[/green]")
            return True

        return False

    # ================== E. GOALS ==================

    def create_goal(
        self,
        name: str,
        team_id: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[int] = None,
        color: Optional[str] = None,
        owners: Optional[List[int]] = None
    ) -> Optional[Dict]:
        """
        Cria uma meta (goal) no workspace.

        Args:
            name: Nome da meta
            team_id: ID do workspace
            description: Descrição
            due_date: Timestamp Unix em ms
            color: Cor em hex
            owners: Lista de user IDs

        Returns:
            dict com goal criado
        """
        tid = team_id or self.team_id

        payload = {"name": name}

        if description:
            payload["description"] = description
        if due_date:
            payload["due_date"] = due_date
        if color:
            payload["color"] = color
        if owners:
            payload["owners"] = owners
            payload["multiple_owners"] = len(owners) > 1

        result = self._request("POST", f"team/{tid}/goal", json=payload)

        if result:
            print(f"[green]✓ Meta criada: {name}[/green]")

        return result

    def get_goals(self, team_id: Optional[str] = None) -> Optional[Dict]:
        """
        Lista todas as metas do workspace.

        Args:
            team_id: ID do workspace

        Returns:
            dict com lista de goals
        """
        tid = team_id or self.team_id
        return self._request("GET", f"team/{tid}/goal")

    def get_goal(self, goal_id: str) -> Optional[Dict]:
        """
        Busca meta específica com seus targets.

        Args:
            goal_id: ID da meta

        Returns:
            dict com goal
        """
        return self._request("GET", f"goal/{goal_id}")

    # ================== F. MEMBERS ==================

    def get_list_members(self, list_id: str) -> Optional[Dict]:
        """
        Lista membros com acesso a uma lista.

        Args:
            list_id: ID da lista

        Returns:
            dict com membros
        """
        result = self._request("GET", f"list/{list_id}/member")

        if result:
            members = result.get("members", [])
            print(f"[green]✓ {len(members)} membros encontrados[/green]")

        return result

    def get_task_members(self, task_id: str) -> Optional[Dict]:
        """
        Lista membros com acesso a uma task.

        Args:
            task_id: ID da task

        Returns:
            dict com membros
        """
        result = self._request("GET", f"task/{task_id}/member")

        if result:
            members = result.get("members", [])
            print(f"[green]✓ {len(members)} membros encontrados[/green]")

        return result

    def add_assignees(
        self,
        task_id: str,
        user_ids: List[int]
    ) -> Optional[Dict]:
        """
        Adiciona assignees a uma task.

        Args:
            task_id: ID da task
            user_ids: Lista de user IDs

        Returns:
            dict com task atualizada
        """
        payload = {"assignees": {"add": user_ids, "rem": []}}

        result = self._request("PUT", f"task/{task_id}", json=payload)

        if result:
            print(f"[green]✓ {len(user_ids)} assignees adicionados[/green]")

        return result

    def remove_assignees(
        self,
        task_id: str,
        user_ids: List[int]
    ) -> Optional[Dict]:
        """
        Remove assignees de uma task.

        Args:
            task_id: ID da task
            user_ids: Lista de user IDs

        Returns:
            dict com task atualizada
        """
        payload = {"assignees": {"add": [], "rem": user_ids}}

        return self._request("PUT", f"task/{task_id}", json=payload)

    # ================== G. WEBHOOKS ==================

    def create_webhook(
        self,
        endpoint_url: str,
        events: List[str],
        team_id: Optional[str] = None,
        space_id: Optional[str] = None,
        folder_id: Optional[str] = None,
        list_id: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Cria um webhook.

        Args:
            endpoint_url: URL que receberá os eventos
            events: Lista de eventos
            team_id: ID do workspace
            space_id: Filtrar por space
            folder_id: Filtrar por folder
            list_id: Filtrar por list

        Returns:
            dict com webhook criado
        """
        tid = team_id or self.team_id

        payload = {"endpoint": endpoint_url, "events": events}

        if space_id:
            payload["space_id"] = space_id
        elif folder_id:
            payload["folder_id"] = folder_id
        elif list_id:
            payload["list_id"] = list_id

        result = self._request("POST", f"team/{tid}/webhook", json=payload)

        if result:
            webhook_id = result.get("id")
            print(f"[green]✓ Webhook criado: {webhook_id}[/green]")

        return result

    def get_webhooks(self, team_id: Optional[str] = None) -> Optional[Dict]:
        """
        Lista todos os webhooks.

        Args:
            team_id: ID do workspace

        Returns:
            dict com lista de webhooks
        """
        tid = team_id or self.team_id
        return self._request("GET", f"team/{tid}/webhook")

    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Deleta um webhook.

        Args:
            webhook_id: ID do webhook

        Returns:
            True se deletado
        """
        result = self._request("DELETE", f"webhook/{webhook_id}")

        if result is not None:
            print(f"[green]✓ Webhook deletado[/green]")
            return True

        return False

    # ================== H. VIEWS ==================

    def get_list_views(self, list_id: str) -> Optional[Dict]:
        """
        Lista views de uma lista.

        Args:
            list_id: ID da lista

        Returns:
            dict com views
        """
        result = self._request("GET", f"list/{list_id}/view")

        if result:
            views = result.get("views", [])
            print(f"[green]✓ {len(views)} views encontradas[/green]")

        return result

    def get_view(self, view_id: str) -> Optional[Dict]:
        """
        Busca view específica.

        Args:
            view_id: ID da view

        Returns:
            dict com view
        """
        return self._request("GET", f"view/{view_id}")

    def get_view_tasks(
        self,
        view_id: str,
        page: int = 0
    ) -> Optional[Dict]:
        """
        Busca tasks de uma view.

        Args:
            view_id: ID da view
            page: Página

        Returns:
            dict com tasks da view
        """
        params = {"page": page}
        result = self._request("GET", f"view/{view_id}/task", params=params)

        if result:
            tasks = result.get("tasks", [])
            print(f"[green]✓ {len(tasks)} tasks na view[/green]")

        return result

    def update_view(
        self,
        view_id: str,
        name: Optional[str] = None,
        grouping: Optional[Dict] = None,
        sorting: Optional[Dict] = None,
        filters: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Atualiza configurações de uma view.

        Args:
            view_id: ID da view
            name: Novo nome
            grouping: Agrupamento
            sorting: Ordenação
            filters: Filtros

        Returns:
            dict com view atualizada
        """
        payload = {}

        if name:
            payload["name"] = name
        if grouping:
            payload["grouping"] = grouping
        if sorting:
            payload["sorting"] = sorting
        if filters:
            payload["filters"] = filters

        result = self._request("PUT", f"view/{view_id}", json=payload)

        if result:
            print(f"[green]✓ View atualizada[/green]")

        return result


# Alias para compatibilidade
ClickUpClient = KaloiClickUpClient
