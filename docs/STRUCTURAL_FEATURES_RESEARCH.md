# 🔬 Pesquisa Técnica: Funcionalidades Estruturais

**Sistema Kaloi - ClickUp Client**

Pesquisa sobre funcionalidades avançadas e estruturais para otimizar o cliente ClickUp.

---

## 📋 Índice

1. [Paginação Automática](#paginação-automática)
2. [Retry e Backoff Automático](#retry-e-backoff-automático)
3. [Batch Operations](#batch-operations)
4. [Async/Await](#asyncawait)
5. [Implementação Recomendada](#implementação-recomendada)
6. [Referências](#referências)

---

## 🔄 Paginação Automática

### Resumo

A API do ClickUp limita respostas a **100 itens por página**. Para recuperar grandes volumes de dados, é necessário implementar paginação automática.

### Como Funciona na API ClickUp

**Parâmetros de Paginação:**
- `page`: Número da página (começa em 0)
- `limit`: Máximo de itens por página (máximo: 100)

**Response:**
```json
{
  "tasks": [...],
  "last_page": false  // true quando não há mais páginas
}
```

### Implementação Recomendada

```python
def get_all_tasks(self, list_id: str, **filters) -> List[Dict]:
    """
    Busca todas as tasks com paginação automática.

    Args:
        list_id: ID da list
        **filters: Filtros adicionais

    Returns:
        Lista completa de tasks
    """
    all_tasks = []
    page = 0

    while True:
        # Buscar página atual
        response = self._request(
            "GET",
            f"list/{list_id}/task",
            params={"page": page, **filters}
        )

        if not response or "tasks" not in response:
            break

        tasks = response["tasks"]
        all_tasks.extend(tasks)

        # Verificar se há mais páginas
        if response.get("last_page", False) or len(tasks) < 100:
            break

        page += 1

    return all_tasks
```

### Estratégias de Paginação

#### 1. **Eager Loading** (padrão acima)
- Carrega todos os dados de uma vez
- **Vantagem**: Simples, todos os dados disponíveis imediatamente
- **Desvantagem**: Alto uso de memória para grandes datasets

#### 2. **Lazy Loading com Generator**
```python
def iter_tasks(self, list_id: str, **filters):
    """
    Itera sobre tasks usando generator (lazy loading).

    Yields:
        Dict: Task individual
    """
    page = 0

    while True:
        response = self._request(
            "GET",
            f"list/{list_id}/task",
            params={"page": page, **filters}
        )

        if not response or "tasks" not in response:
            break

        tasks = response["tasks"]

        for task in tasks:
            yield task

        if response.get("last_page", False) or len(tasks) < 100:
            break

        page += 1

# Uso
for task in client.iter_tasks("list_id"):
    process_task(task)
```

**Vantagens:**
- Baixo uso de memória
- Processa dados conforme carrega
- Ideal para grandes volumes

#### 3. **Chunked Loading**
```python
def get_tasks_chunked(self, list_id: str, chunk_size: int = 5, **filters):
    """
    Carrega tasks em chunks (grupos de páginas).

    Args:
        list_id: ID da list
        chunk_size: Número de páginas por chunk
        **filters: Filtros

    Yields:
        List[Dict]: Chunk de tasks
    """
    page = 0

    while True:
        chunk = []

        for _ in range(chunk_size):
            response = self._request(
                "GET",
                f"list/{list_id}/task",
                params={"page": page, **filters}
            )

            if not response or "tasks" not in response:
                break

            chunk.extend(response["tasks"])

            if response.get("last_page", False):
                yield chunk
                return

            page += 1

        if chunk:
            yield chunk
        else:
            break
```

### Limitações

- **Máximo de 100 itens por página** (não configurável)
- **Paginação baseada em página**, não cursor
- **Não há total_pages** na resposta (apenas `last_page`)

---

## 🔁 Retry e Backoff Automático

### Resumo

A API do ClickUp tem **rate limits** de:
- **100 requisições/min** (Free, Unlimited, Business)
- **1000 requisições/min** (Business Plus)

Responde com **HTTP 429** quando excedido.

### Implementação com urllib3.Retry

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class KaloiClickUpClient:
    def __init__(self):
        self.session = requests.Session()

        # Configurar retry automático
        retries = Retry(
            total=5,  # Máximo de 5 tentativas
            backoff_factor=1,  # Fator de backoff exponencial
            status_forcelist=[429, 500, 502, 503, 504],  # Status para retry
            allowed_methods=["GET", "POST", "PUT", "DELETE"]  # Métodos
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _request(self, method: str, endpoint: str, **kwargs):
        """Faz requisição com retry automático."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
```

### Cálculo do Backoff

Com `backoff_factor=1`, os delays são:
- 1ª tentativa: 0s (imediato)
- 2ª tentativa: 0.5s
- 3ª tentativa: 1s
- 4ª tentativa: 2s
- 5ª tentativa: 4s
- 6ª tentativa: 8s

**Fórmula:**
```
delay = backoff_factor * (2 ** (retry_number - 1))
```

### Implementação com backoff Library

```python
import backoff
import requests

class KaloiClickUpClient:
    @backoff.on_exception(
        backoff.expo,  # Exponential backoff
        requests.exceptions.RequestException,
        max_tries=5,
        giveup=lambda e: e.response is not None and e.response.status_code < 500
    )
    def _request(self, method: str, endpoint: str, **kwargs):
        """Requisição com backoff exponencial."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
```

### Rate Limiting Proativo

```python
from ratelimit import limits, sleep_and_retry

class KaloiClickUpClient:
    CALLS_PER_MINUTE = 100  # Ajustar conforme plano

    @sleep_and_retry
    @limits(calls=CALLS_PER_MINUTE, period=60)
    def _request(self, method: str, endpoint: str, **kwargs):
        """Requisição com rate limiting proativo."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
```

### Tratamento de Retry-After Header

```python
def _request(self, method: str, endpoint: str, **kwargs):
    """Requisição respeitando Retry-After header."""
    url = f"{self.base_url}/{endpoint}"

    while True:
        response = requests.request(method, url, **kwargs)

        if response.status_code == 429:
            # Verificar header Retry-After
            retry_after = response.headers.get("Retry-After")

            if retry_after:
                wait_time = int(retry_after)
                print(f"[yellow]⏱ Rate limit atingido. Aguardando {wait_time}s...[/yellow]")
                time.sleep(wait_time)
                continue
            else:
                # Backoff padrão se não houver header
                time.sleep(60)
                continue

        response.raise_for_status()
        return response.json()
```

---

## 📦 Batch Operations

### Resumo

**Importante:** A API do ClickUp **NÃO tem endpoint oficial de batch/bulk operations** para criar ou atualizar múltiplas tasks de uma vez.

### Limitações Atuais

- Não há endpoint `POST /tasks` (bulk create)
- Não há endpoint `PUT /tasks` (bulk update)
- Cada task deve ser criada/atualizada individualmente

### Estratégias de Otimização

#### 1. **Concurrent Requests com Threading**

```python
import concurrent.futures
from typing import List, Dict

class KaloiClickUpClient:
    def create_tasks_batch(
        self,
        list_id: str,
        tasks: List[Dict],
        max_workers: int = 5
    ) -> List[Dict]:
        """
        Cria múltiplas tasks concorrentemente.

        Args:
            list_id: ID da list
            tasks: Lista de dicts com dados das tasks
            max_workers: Máximo de threads concorrentes

        Returns:
            Lista de tasks criadas
        """
        def create_task(task_data):
            return self.create_task(list_id, **task_data)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(create_task, tasks))

        return results
```

**Vantagens:**
- Aproveita I/O wait
- Mais rápido que sequencial
- Simples de implementar

**Desvantagens:**
- Ainda faz N requisições
- Pode estourar rate limit rapidamente

#### 2. **Rate-Limited Batch Processing**

```python
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

class KaloiClickUpClient:
    @sleep_and_retry
    @limits(calls=90, period=60)  # 90 chamadas/min (margem de segurança)
    def _create_task_rate_limited(self, list_id: str, **task_data):
        """Cria task com rate limit."""
        return self.create_task(list_id, **task_data)

    def create_tasks_batch(
        self,
        list_id: str,
        tasks: List[Dict],
        show_progress: bool = True
    ) -> List[Dict]:
        """
        Cria tasks em lote respeitando rate limit.

        Args:
            list_id: ID da list
            tasks: Lista de tasks
            show_progress: Mostrar barra de progresso

        Returns:
            Lista de tasks criadas
        """
        results = []

        iterator = tqdm(tasks, desc="Criando tasks") if show_progress else tasks

        for task_data in iterator:
            result = self._create_task_rate_limited(list_id, **task_data)
            results.append(result)

        return results
```

#### 3. **Async Batch com asyncio** (veja seção async)

```python
import asyncio
import httpx

class AsyncKaloiClickUpClient:
    async def create_tasks_batch(
        self,
        list_id: str,
        tasks: List[Dict]
    ) -> List[Dict]:
        """Cria tasks assincronamente."""
        async with httpx.AsyncClient() as client:
            tasks_coros = [
                self._create_task_async(client, list_id, task_data)
                for task_data in tasks
            ]
            results = await asyncio.gather(*tasks_coros)

        return results
```

### Recomendações

1. **Para < 10 tasks:** Sequencial é suficiente
2. **Para 10-100 tasks:** Threading com rate limiting
3. **Para > 100 tasks:** Async com controle de concorrência

---

## ⚡ Async/Await

### Resumo

Implementar versão assíncrona do cliente para alto desempenho com múltiplas requisições concorrentes.

### Bibliotecas Recomendadas

- **httpx**: HTTP client async/sync
- **aiohttp**: Async HTTP client/server
- **asyncio**: Framework async do Python

### Implementação com httpx

```python
import asyncio
import httpx
from typing import Optional, Dict, Any

class AsyncKaloiClickUpClient:
    """Cliente ClickUp assíncrono."""

    def __init__(
        self,
        token: Optional[str] = None,
        team_id: Optional[str] = None,
        base_url: str = "https://api.clickup.com/api/v2"
    ):
        self.token = token or os.getenv("CLICKUP_TOKEN")
        self.team_id = team_id or os.getenv("CLICKUP_TEAM_ID")
        self.base_url = base_url

        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    async def _request(
        self,
        client: httpx.AsyncClient,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Optional[Dict]:
        """
        Faz requisição assíncrona.

        Args:
            client: Cliente httpx
            method: Método HTTP
            endpoint: Endpoint da API
            **kwargs: Parâmetros adicionais

        Returns:
            Response JSON ou None
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = await client.request(
                method,
                url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[red]✗ HTTP Error: {e}[/red]")
            return None

    async def get_task(self, task_id: str) -> Optional[Dict]:
        """Busca task assincronamente."""
        async with httpx.AsyncClient() as client:
            return await self._request(client, "GET", f"task/{task_id}")

    async def get_tasks(self, list_id: str, **filters) -> Optional[Dict]:
        """Busca tasks assincronamente."""
        async with httpx.AsyncClient() as client:
            return await self._request(
                client,
                "GET",
                f"list/{list_id}/task",
                params=filters
            )

    async def create_task(
        self,
        list_id: str,
        name: str,
        **kwargs
    ) -> Optional[Dict]:
        """Cria task assincronamente."""
        async with httpx.AsyncClient() as client:
            payload = {"name": name, **kwargs}
            return await self._request(
                client,
                "POST",
                f"list/{list_id}/task",
                json=payload
            )
```

### Batch Operations com Async

```python
class AsyncKaloiClickUpClient:
    async def get_multiple_tasks(
        self,
        task_ids: List[str]
    ) -> List[Optional[Dict]]:
        """
        Busca múltiplas tasks concorrentemente.

        Args:
            task_ids: Lista de IDs

        Returns:
            Lista de tasks
        """
        async with httpx.AsyncClient() as client:
            tasks = [
                self._request(client, "GET", f"task/{task_id}")
                for task_id in task_ids
            ]
            results = await asyncio.gather(*tasks)

        return results

    async def create_multiple_tasks(
        self,
        list_id: str,
        tasks_data: List[Dict]
    ) -> List[Optional[Dict]]:
        """
        Cria múltiplas tasks concorrentemente.

        Args:
            list_id: ID da list
            tasks_data: Lista de dicts com dados

        Returns:
            Lista de tasks criadas
        """
        async with httpx.AsyncClient() as client:
            tasks = [
                self._request(
                    client,
                    "POST",
                    f"list/{list_id}/task",
                    json=task_data
                )
                for task_data in tasks_data
            ]
            results = await asyncio.gather(*tasks)

        return results
```

### Controle de Concorrência

```python
import asyncio
from asyncio import Semaphore

class AsyncKaloiClickUpClient:
    async def create_tasks_controlled(
        self,
        list_id: str,
        tasks_data: List[Dict],
        max_concurrent: int = 10
    ) -> List[Optional[Dict]]:
        """
        Cria tasks com controle de concorrência.

        Args:
            list_id: ID da list
            tasks_data: Dados das tasks
            max_concurrent: Máximo de requisições simultâneas

        Returns:
            Lista de tasks criadas
        """
        semaphore = Semaphore(max_concurrent)

        async def create_with_limit(task_data):
            async with semaphore:
                async with httpx.AsyncClient() as client:
                    return await self._request(
                        client,
                        "POST",
                        f"list/{list_id}/task",
                        json=task_data
                    )

        tasks = [create_with_limit(data) for data in tasks_data]
        results = await asyncio.gather(*tasks)

        return results
```

### Uso do Cliente Async

```python
# Uso básico
async def main():
    client = AsyncKaloiClickUpClient()

    # Buscar task
    task = await client.get_task("task_id")

    # Criar múltiplas tasks
    tasks_data = [
        {"name": "Task 1", "description": "Desc 1"},
        {"name": "Task 2", "description": "Desc 2"},
        {"name": "Task 3", "description": "Desc 3"}
    ]

    results = await client.create_multiple_tasks("list_id", tasks_data)
    print(f"Criadas {len(results)} tasks")

# Executar
asyncio.run(main())
```

### Vantagens do Async

- **Performance**: 10-100x mais rápido para múltiplas requisições
- **Escalabilidade**: Suporta centenas de requisições concorrentes
- **Eficiência**: Melhor uso de recursos (CPU, memória)

### Desvantagens

- **Complexidade**: Código mais complexo
- **Debugging**: Mais difícil de debugar
- **Compatibilidade**: Requer Python 3.7+

---

## 🎯 Implementação Recomendada

### Prioridade 1: Retry e Backoff

**Motivo:** Essencial para produção, evita falhas por rate limit

```python
# Adicionar ao client.py existente
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class KaloiClickUpClient:
    def __init__(self):
        # ... código existente ...

        # Configurar session com retry
        self.session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _request(self, method: str, endpoint: str, **kwargs):
        # Usar self.session ao invés de requests diretamente
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        # ... resto do código ...
```

### Prioridade 2: Paginação Automática

**Motivo:** Crucial para lidar com grandes volumes de dados

```python
# Adicionar método auxiliar
def get_all_paginated(
    self,
    endpoint: str,
    data_key: str = "tasks",
    **params
) -> List[Dict]:
    """
    Helper genérico para paginação.

    Args:
        endpoint: Endpoint da API
        data_key: Chave dos dados na response
        **params: Parâmetros da requisição

    Returns:
        Lista completa de items
    """
    all_items = []
    page = 0

    while True:
        params["page"] = page
        response = self._request("GET", endpoint, params=params)

        if not response or data_key not in response:
            break

        items = response[data_key]
        all_items.extend(items)

        if response.get("last_page", False) or len(items) < 100:
            break

        page += 1

    return all_items

# Atualizar get_tasks para usar paginação
def get_tasks(self, list_id: str, paginate: bool = False, **filters):
    """
    Busca tasks de uma list.

    Args:
        list_id: ID da list
        paginate: Se True, busca todas as páginas
        **filters: Filtros

    Returns:
        Dict com tasks ou lista completa se paginate=True
    """
    if paginate:
        return self.get_all_paginated(
            f"list/{list_id}/task",
            data_key="tasks",
            **filters
        )
    else:
        return self._request("GET", f"list/{list_id}/task", params=filters)
```

### Prioridade 3: Batch Helper (Threading)

**Motivo:** Acelera operações em lote sem complexidade do async

```python
import concurrent.futures
from typing import Callable, List, Any

def batch_operation(
    self,
    operation: Callable,
    items: List[Any],
    max_workers: int = 5,
    show_progress: bool = True
) -> List[Any]:
    """
    Executa operação em lote com threading.

    Args:
        operation: Função a executar (ex: self.create_task)
        items: Lista de argumentos para a função
        max_workers: Threads concorrentes
        show_progress: Mostrar progresso

    Returns:
        Lista de resultados
    """
    from tqdm import tqdm

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        if show_progress:
            results = list(tqdm(
                executor.map(operation, items),
                total=len(items),
                desc="Processando"
            ))
        else:
            results = list(executor.map(operation, items))

    return results
```

### Prioridade 4: Async Client (Opcional)

**Motivo:** Para casos de alta performance, criar versão async separada

**Arquivo:** `src/clickup_api/async_client.py`

Criar cliente async completo conforme exemplos acima.

---

## 📚 Referências

### Documentação Oficial

- **ClickUp API Docs**: https://developer.clickup.com/
- **Rate Limits**: https://developer.clickup.com/docs/rate-limits
- **Pagination**: https://clickup.canny.io/feature-requests/p/pagination-through-the-api

### Bibliotecas Python

- **requests**: https://requests.readthedocs.io/
- **urllib3**: https://urllib3.readthedocs.io/
- **httpx**: https://www.python-httpx.org/
- **aiohttp**: https://docs.aiohttp.org/
- **backoff**: https://github.com/litl/backoff
- **ratelimit**: https://github.com/tomasbasham/ratelimit

### Tutoriais e Exemplos

- **Python Requests Retry**: https://scrapeops.io/python-web-scraping-playbook/python-requests-retry-failed-requests/
- **Async HTTP with httpx**: https://www.twilio.com/en-us/blog/asynchronous-http-requests-in-python-with-httpx-and-asyncio
- **ClickUp API with Python**: https://endgrate.com/blog/using-the-clickup-api-to-get-tasks-(with-python-examples)

---

**Criado em:** 2025-10-31
**Autor:** Sistema Kaloi
**Status:** ✅ Completo
