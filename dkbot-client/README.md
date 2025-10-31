# dkbot-client - ClickUp Extended Client

**Cliente ClickUp estendido com funcionalidades avançadas (A-H)**

Sistema Kaloi - Extensão do ClickUp Client original

---

## 📦 O que é este pacote?

Este é o **pacote estendido** do ClickUp Client original, contendo implementações completas das funcionalidades avançadas:

- **A. Custom Fields** - 16 tipos de campos personalizados
- **B. Time Tracking** - Rastreamento de tempo com timers
- **C. Attachments** - Upload de arquivos
- **D. Checklists** - Listas de verificação
- **E. Goals** - Objetivos e metas
- **F. Members** - Gerenciamento de membros
- **G. Webhooks** - Eventos em tempo real
- **H. Views** - Visualizações customizadas

---

## 🚀 Instalação

```bash
# A partir do diretório raiz do projeto
cd dkbot-client

# Instalar dependências
pip install -r requirements.txt

# Copiar .env da raiz
cp ../.env .env
```

---

## 💡 Uso Rápido

```python
from src.dkbot.client import KaloiClickUpClient
from src.dkbot.helpers.custom_fields import CustomFieldMapper
from src.dkbot.helpers.time_tracking import format_duration

# Inicializar cliente
client = KaloiClickUpClient()

# Custom Fields
fields = client.get_custom_fields("list_id")
client.set_custom_field("task_id", "field_id", "Valor")

# Time Tracking
client.create_time_entry(
    duration=7200000,  # 2 horas
    task_id="task_id",
    billable=True
)

# Checklists
checklist = client.create_checklist("task_id", "Deploy")
client.add_checklist_item(checklist["checklist"]["id"], "Run tests")

# Goals
goal = client.create_goal(
    name="Q1 Sales Target",
    due_date=1735689600000
)

# Webhooks
webhook = client.create_webhook(
    endpoint_url="https://myapp.com/webhook",
    events=["taskCreated", "taskUpdated"]
)
```

---

## 📁 Estrutura

```
dkbot-client/
├── README.md              # Esta documentação
├── requirements.txt       # Dependências
├── .env                  # Configuração (copiar do projeto raiz)
│
├── src/
│   └── dkbot/
│       ├── __init__.py
│       ├── client.py     # Cliente estendido com A-H
│       ├── templates/    # Templates para automação
│       ├── validators/   # Validadores de dados
│       └── helpers/
│           ├── custom_fields.py    # Helpers de Custom Fields
│           ├── time_tracking.py    # Helpers de Time Tracking
│           ├── date_utils.py       # Parsing de datas
│           └── translation.py      # Tradução PT/EN
│
├── docs/                 # Documentação técnica
│   └── (links para docs principais)
│
└── examples/
    └── test_all_features.py  # Teste completo A-H
```

---

## 🧪 Testes

Execute o script de teste completo:

```bash
python examples/test_all_features.py
```

---

## 📚 Helpers Disponíveis

### custom_fields.py

```python
from src.dkbot.helpers.custom_fields import (
    CustomFieldMapper,
    get_field_value,
    get_all_field_values,
    find_field_by_name
)

# Mapear valores Python para ClickUp
mapper = CustomFieldMapper()
value = mapper.format_text("Texto")
value = mapper.format_number(42)
value = mapper.format_currency(99.99)  # Converte para centavos
value = mapper.format_date(datetime.now())

# Extrair valores de fields retornados pela API
field_data = {...}  # Retorno da API
value = get_field_value(field_data)

# Extrair todos os valores de custom fields
custom_fields = [...]  # Lista de fields da task
values = get_all_field_values(custom_fields)
# {'Field Name': 'Field Value', ...}
```

### time_tracking.py

```python
from src.dkbot.helpers.time_tracking import (
    format_duration,
    calculate_total_time,
    group_by_task,
    generate_daily_report,
    filter_billable_only
)

# Formatar duração
duration_ms = 7200000
format_duration(duration_ms, "verbose")   # "2 horas"
format_duration(duration_ms, "short")     # "2h"
format_duration(duration_ms, "clock")     # "02:00:00"
format_duration(duration_ms, "decimal")   # "2.00 horas"

# Calcular tempo total
entries = [...]  # Lista de time entries
total = calculate_total_time(entries)

# Agrupar por task
grouped = group_by_task(entries)
# {'task_id': [entries]}

# Relatório diário
report = generate_daily_report(entries, datetime.now())
# {'date': '2025-10-31', 'total_ms': ..., 'tasks': {...}}

# Filtrar apenas billable
billable = filter_billable_only(entries)
```

---

## 🔗 Links para Documentação Completa

- **[README Principal](../README.md)** - Documentação completa do projeto
- **[Docs - Custom Fields](../docs/CUSTOM_FIELDS_SUMMARY.md)** - Resumo de Custom Fields
- **[Docs - Time Tracking](../docs/TIME_TRACKING_SUMMARY.md)** - Resumo de Time Tracking
- **[Docs - Funcionalidades Avançadas](../docs/ADVANCED_FEATURES_SUMMARY.md)** - Resumo C-H

---

## 📊 Resumo de Funcionalidades

| Feature | Métodos | Helpers | Complexidade |
|---------|---------|---------|--------------|
| **A. Custom Fields** | 3 | ✅ CustomFieldMapper | 🟡 Média |
| **B. Time Tracking** | 7 | ✅ Formatters, Filters | 🟢 Baixa |
| **C. Attachments** | 1 | - | 🟢 Baixa |
| **D. Checklists** | 4 | - | 🟢 Baixa |
| **E. Goals** | 3 | - | 🟡 Média |
| **F. Members** | 4 | - | 🟢 Baixa |
| **G. Webhooks** | 3 | - | 🟡 Média |
| **H. Views** | 4 | - | 🔴 Alta |

**Total: 29 métodos + 2 helpers especializados**

---

## ⚙️ Configuração

O pacote usa as mesmas variáveis de ambiente do projeto principal:

```env
CLICKUP_TOKEN=pk_SEU_TOKEN_AQUI
CLICKUP_TEAM_ID=SEU_TEAM_ID
CLICKUP_BASE_URL=https://api.clickup.com/api/v2
```

Copie o `.env` do diretório raiz ou crie um novo.

---

## 🎯 Casos de Uso

### 1. Rastreamento de Tempo Completo

```python
# Iniciar timer
client.start_timer(task_id, description="Desenvolvimento")

# ... trabalhar na task ...

# Parar timer
client.stop_timer()

# Buscar time entries do dia
from datetime import datetime
entries = client.get_time_entries(
    start_date=int(datetime.now().replace(hour=0).timestamp() * 1000)
)

# Gerar relatório
from src.dkbot.helpers.time_tracking import generate_daily_report
report = generate_daily_report(entries, datetime.now())

print(f"Total do dia: {report['total_formatted']}")
print(f"Billable: {report['billable_formatted']}")
```

### 2. Gerenciar Custom Fields

```python
# Listar fields disponíveis
fields = client.get_custom_fields("list_id")

# Setar múltiplos fields de uma vez
client.set_multiple_custom_fields("task_id", {
    "field_id_1": "Valor texto",
    "field_id_2": 100,
    "field_id_3": True
})

# Extrair valores com helper
from src.dkbot.helpers.custom_fields import get_all_field_values
task = client.get_task("task_id")
values = get_all_field_values(task["custom_fields"])
```

### 3. Automação com Webhooks

```python
# Criar webhook para task events
webhook = client.create_webhook(
    endpoint_url="https://myapp.com/clickup-webhook",
    events=["taskCreated", "taskUpdated", "taskStatusUpdated"],
    space_id="space_id"
)

# No seu servidor (Flask/FastAPI):
@app.post("/clickup-webhook")
def handle_webhook(request):
    data = request.json
    event = data.get("event")

    if event == "taskCreated":
        # Processar task criada
        task_id = data["task_id"]
        # Adicionar checklist automático
        checklist = client.create_checklist(task_id, "Workflow")
        client.add_checklist_item(checklist["id"], "Review")
        client.add_checklist_item(checklist["id"], "Test")
        client.add_checklist_item(checklist["id"], "Deploy")

    return {"status": "ok"}
```

---

## 👥 Autores

- **Dani Kaloi** - [@Danizk](https://github.com/Danizk)
- **Sistema Kaloi** - Arquitetura híbrida de IAs

---

## 📝 Licença

MIT License - Veja [LICENSE](../LICENSE) para detalhes

---

**Desenvolvido com ❤️ pelo Sistema Kaloi**
