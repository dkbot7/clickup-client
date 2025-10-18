# ClickUp Client - Sistema Kaloi

Cliente Python moderno e completo para integração com a API v2 do ClickUp.

## 🌟 Características

- ✅ **100% Bilíngue (PT/EN)** - Use parâmetros em português ou inglês!
- ✅ **100% compatível com Python 3.13**
- ✅ **Datas em linguagem natural** (português e inglês)
- ✅ **Tradução automática** PT → EN antes de enviar à API
- ✅ **Output formatado** com Rich
- ✅ **Type hints completos**
- ✅ **Exception handling robusto**
- ✅ **Rate limiting automático**
- ✅ **Sem dependências problemáticas** (sem Pendulum)

## 📦 Instalação

```bash
# Clone o repositório
git clone https://github.com/Danizk/clickup-client.git
cd clickup-client

# Instale as dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

1. Crie um arquivo `.env` na raiz do projeto:

```env
CLICKUP_TOKEN=pk_SEU_TOKEN_AQUI
CLICKUP_TEAM_ID=SEU_TEAM_ID
CLICKUP_BASE_URL=https://api.clickup.com/api/v2
```

2. Obtenha seu token em: [ClickUp Settings → Apps → API Token](https://app.clickup.com/settings/apps)

## 🚀 Uso Básico

### Autenticação e Validação

```python
from src.clickup_api.client import KaloiClickUpClient

# Inicializar cliente
client = KaloiClickUpClient()

# Validar autenticação
client.validate_auth()

# Obter informações do usuário
client.get_user_info()
```

### 🌐 Suporte Bilíngue (PT/EN)

**O cliente aceita parâmetros 100% em PORTUGUÊS ou INGLÊS!**

A tradução é feita automaticamente antes de enviar à API.

#### Exemplo em Português

```python
#  Use português naturalmente!
task = client.create_task(
    list_id="123456789",
    nome="Reunião importante",           # ← português!
    descrição="Discutir projeto Q1",     # ← português!
    prioridade="alta",                    # ← português!
    status="em progresso",                # ← português!
    data_vencimento="próxima segunda"     # ← português + linguagem natural!
)

# Atualizar task em português
client.update_task(
    "task_id",
    status="concluído",
    prioridade="baixa"
)

# Buscar tasks com filtros em português
tasks = client.get_tasks(
    "list_id",
    arquivada=False,
    página=0
)
```

#### Exemplo em Inglês

```python
# English works too!
task = client.create_task(
    list_id="123456789",
    name="Important meeting",
    description="Discuss Q1 project",
    priority="high",                      # or priority=2
    status="in progress",
    due_date="next monday"                # natural language!
)

# Update task in English
client.update_task(
    "task_id",
    status="complete",
    priority="low"
)

# Get tasks with English filters
tasks = client.get_tasks(
    "list_id",
    archived=False,
    page=0
)
```

#### Tabela de Tradução Automática

| Português | Inglês | Valor API |
|-----------|--------|-----------|
| **Prioridade** |
| urgente | urgent | 1 |
| alta | high | 2 |
| normal | normal | 3 |
| baixa | low | 4 |
| **Status** |
| fazer | to do | "to do" |
| em progresso | in progress | "in progress" |
| em revisão | in review | "in review" |
| concluído | complete | "complete" |
| **Parâmetros** |
| nome | name | name |
| descrição | description | description |
| prioridade | priority | priority |
| data_vencimento | due_date | due_date |
| data_inicio | start_date | start_date |
| responsáveis | assignees | assignees |
| etiquetas | tags | tags |

### Gerenciamento de Tasks

```python
# Criar task com data em linguagem natural
task = client.create_task(
    list_id="123456789",
    name="Reunião importante",
    description="Discutir o projeto X",
    due_date="amanhã",  # Suporta PT e EN!
    priority=3
)

# Buscar task
task = client.get_task("task_id")

# Atualizar task
client.update_task(
    "task_id",
    name="Novo nome",
    status="em progresso"
)

# Deletar task
client.delete_task("task_id")

# Listar tasks de uma lista
tasks = client.get_tasks("list_id")
```

### 📅 Datas em Linguagem Natural

O cliente suporta datas naturais em **português** e **inglês**:

```python
# Português
client.create_task(
    list_id="123",
    name="Task 1",
    due_date="amanhã"  # Tomorrow
)

client.create_task(
    list_id="123",
    name="Task 2",
    due_date="próxima semana"  # Next week
)

client.create_task(
    list_id="123",
    name="Task 3",
    due_date="1 de dezembro"  # December 1st
)

# Inglês
client.create_task(
    list_id="123",
    name="Task 4",
    due_date="tomorrow"
)

client.create_task(
    list_id="123",
    name="Task 5",
    due_date="next week"
)

client.create_task(
    list_id="123",
    name="Task 6",
    due_date="december 1st"
)

# Formatos tradicionais também funcionam
client.create_task(
    list_id="123",
    name="Task 7",
    due_date="2024-12-25"  # ISO 8601
)

client.create_task(
    list_id="123",
    name="Task 8",
    due_date=1735095600000  # Unix timestamp (ms)
)
```

### Workspaces, Spaces e Folders

```python
# Listar workspaces
teams = client.get_teams()

# Listar spaces
spaces = client.get_spaces(team_id="123")

# Buscar space específico
space = client.get_space("space_id")

# Listar folders
folders = client.get_folders("space_id")

# Buscar folder
folder = client.get_folder("folder_id")
```

### Lists

```python
# Listar lists de um folder
lists = client.get_lists("folder_id")

# Listar lists sem folder (folderless)
lists = client.get_folderless_lists("space_id")

# Buscar list específica
list_data = client.get_list("list_id")
```

### Comentários

```python
# Listar comentários de uma task
comments = client.get_task_comments("task_id")

# Criar comentário
comment = client.create_task_comment(
    "task_id",
    "Ótimo progresso no projeto!"
)
```

## 📚 Métodos Disponíveis

### Autenticação
- `validate_auth()` - Valida token e lista workspaces
- `get_user_info()` - Informações do usuário autenticado

### Teams/Workspaces
- `get_teams()` - Lista todos os workspaces

### Spaces
- `get_spaces(team_id)` - Lista spaces de um workspace
- `get_space(space_id)` - Busca space específico

### Folders
- `get_folders(space_id)` - Lista folders de um space
- `get_folder(folder_id)` - Busca folder específico

### Lists
- `get_lists(folder_id)` - Lista lists de um folder
- `get_folderless_lists(space_id)` - Lists sem folder
- `get_list(list_id)` - Busca list específica

### Tasks
- `get_task(task_id)` - Busca task específica
- `get_tasks(list_id, **filters)` - Lista tasks com filtros
- `create_task(list_id, name, **kwargs)` - Cria nova task
- `update_task(task_id, **updates)` - Atualiza task
- `delete_task(task_id)` - Deleta task

### Comments
- `get_task_comments(task_id)` - Lista comentários
- `create_task_comment(task_id, text)` - Cria comentário

## 🧪 Testes

Execute o script de teste incluído:

```bash
# Teste de autenticação
python main.py

# Teste de datas em linguagem natural
python test_fuzzy_dates.py
```

## 📋 Datas Suportadas

### Formatos Aceitos

**Linguagem Natural (PT):**
- "amanhã", "hoje", "ontem"
- "próxima semana", "próximo mês"
- "em 3 dias", "em 2 semanas"
- "1 de dezembro", "25 de dezembro de 2024"

**Linguagem Natural (EN):**
- "tomorrow", "today", "yesterday"
- "next week", "next month"
- "in 3 days", "in 2 weeks"
- "december 1st", "december 25th 2024"

**Formatos Tradicionais:**
- ISO 8601: `"2024-12-25T00:00:00Z"`
- Unix timestamp (ms): `1735095600000`
- Unix timestamp (s): `1735095600`

### Durações

O helper `fuzzy_time_to_seconds()` converte durações:

```python
from src.clickup_api.helpers.date_utils import fuzzy_time_to_seconds

# Português
fuzzy_time_to_seconds("2 horas")      # 7200
fuzzy_time_to_seconds("30 minutos")   # 1800
fuzzy_time_to_seconds("1 dia")        # 86400

# Inglês
fuzzy_time_to_seconds("2 hours")      # 7200
fuzzy_time_to_seconds("30 minutes")   # 1800
fuzzy_time_to_seconds("1 day")        # 86400
```

## 🛠️ Tecnologias

- **Python 3.13+**
- **requests** - HTTP client
- **python-dotenv** - Variáveis de ambiente
- **rich** - Output formatado
- **dateparser** - Parsing de datas naturais

## 📁 Estrutura do Projeto

```
clickup-client/
├── .env                      # Credenciais (não versionado)
├── .env.example             # Template de configuração
├── .gitignore              # Arquivos ignorados
├── README.md               # Esta documentação
├── requirements.txt        # Dependências Python
├── main.py                # Script de teste principal
├── test_fuzzy_dates.py    # Teste de datas naturais
├── demo_bilingual.py      # Demonstração bilíngue (PT/EN)
│
└── src/
    └── clickup_api/
        ├── __init__.py
        ├── client.py      # Cliente principal (bilíngue)
        └── helpers/
            ├── __init__.py
            ├── date_utils.py      # Parsing de datas naturais
            └── translation.py     # Tradução PT ↔ EN
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Dani Kaloi** - [@Danizk](https://github.com/Danizk)
- **Sistema Kaloi** - Arquitetura híbrida de IAs

## 🔗 Links Úteis

- [Documentação Oficial do ClickUp API](https://clickup.com/api/)
- [ClickUp Developer Portal](https://developer.clickup.com/)
- [Criar Token de API](https://app.clickup.com/settings/apps)

## ⚠️ Aviso

Este cliente não é afiliado oficialmente ao ClickUp. É um projeto independente criado pela comunidade.

---

**Desenvolvido com ❤️ pelo Sistema Kaloi**
