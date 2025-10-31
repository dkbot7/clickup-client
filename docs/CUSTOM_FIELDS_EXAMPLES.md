# 📘 Exemplos Práticos: Custom Fields

**Guia de uso de campos personalizados no ClickUp Client**

---

## 📋 Índice

1. [Setup Inicial](#setup-inicial)
2. [Obter Custom Fields Disponíveis](#obter-custom-fields-disponíveis)
3. [Exemplos por Tipo de Campo](#exemplos-por-tipo-de-campo)
4. [Casos de Uso Reais](#casos-de-uso-reais)
5. [Tratamento de Erros](#tratamento-de-erros)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Inicial

```python
from src.clickup_api.client import KaloiClickUpClient

# Inicializar cliente
client = KaloiClickUpClient()

# IDs necessários (obter do ClickUp)
list_id = "901234567"
task_id = "abc123xyz"
```

---

## 📋 Obter Custom Fields Disponíveis

### Listar todos os custom fields de uma lista

```python
# Obter custom fields da lista
fields = client.get_custom_fields(list_id)

print("Custom Fields disponíveis:")
for field in fields.get("fields", []):
    print(f"  • {field['name']} (ID: {field['id']}, Tipo: {field['type']})")
```

**Saída esperada:**
```
Custom Fields disponíveis:
  • Priority Level (ID: b955c4dc-a6a7-4c05-9051-8d5f7e4f2c55, Tipo: drop_down)
  • Budget (ID: c123d456-e789-0abc-def1-234567890abc, Tipo: currency)
  • Due Date (ID: d234e567-f890-1bcd-ef12-345678901bcd, Tipo: date)
  • Completed (ID: e345f678-9012-3cde-f123-456789012cde, Tipo: checkbox)
```

### Obter custom fields de uma task específica

```python
# Obter task com custom fields
task = client.get_task(task_id)

print(f"Task: {task['name']}")
print("\nCustom Fields:")
for field in task.get("custom_fields", []):
    print(f"  • {field['name']}: {field.get('value', 'N/A')}")
```

---

## 🎨 Exemplos por Tipo de Campo

### 1. Short Text / Text

```python
# Texto curto (1 linha)
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-1",
    value="Reunião com cliente"
)

# Texto longo (múltiplas linhas)
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-2",
    value="""Notas da reunião:
    - Aprovação do projeto fase 1
    - Orçamento definido: R$ 50.000
    - Próxima reunião: próxima segunda
    """
)

# EM PORTUGUÊS (com tradução automática)
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-3",
    value="Cliente solicitou alterações no layout"
)
```

### 2. Number

```python
# Número inteiro
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-4",
    value=42
)

# Número decimal
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-5",
    value=99.99
)

# Horas estimadas
client.set_custom_field(
    task_id="abc123",
    field_id="field-uuid-6",
    value=8.5  # 8 horas e 30 minutos
)
```

### 3. Currency (Moeda)

```python
# Valor em reais
client.set_custom_field(
    task_id="abc123",
    field_id="budget-field-id",
    value=15000.00  # R$ 15.000,00
)

# Orçamento do projeto
client.set_custom_field(
    task_id="abc123",
    field_id="project-budget-id",
    value=250000.50
)
```

### 4. Checkbox (Verdadeiro/Falso)

```python
# Marcar como concluído
client.set_custom_field(
    task_id="abc123",
    field_id="completed-field-id",
    value=True
)

# Desmarcar
client.set_custom_field(
    task_id="abc123",
    field_id="approved-field-id",
    value=False
)

# Cliente aprovou?
client.set_custom_field(
    task_id="abc123",
    field_id="client-approval-id",
    value=True
)
```

### 5. Date (Data)

```python
# Data simples (sem hora)
client.set_custom_field(
    task_id="abc123",
    field_id="delivery-date-id",
    value=1701388800000  # 01/12/2024 (Unix timestamp em ms)
)

# Data com hora
client.set_custom_field(
    task_id="abc123",
    field_id="meeting-datetime-id",
    value=1701442800000,  # 01/12/2024 15:00
    time=True  # Indica que inclui hora
)

# Usando helper de datas naturais
from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix

# Em português
timestamp = fuzzy_time_to_unix("próxima segunda")
client.set_custom_field(
    task_id="abc123",
    field_id="deadline-id",
    value=timestamp
)

# Em inglês
timestamp = fuzzy_time_to_unix("next friday")
client.set_custom_field(
    task_id="abc123",
    field_id="review-date-id",
    value=timestamp
)
```

### 6. Dropdown (Lista Suspensa)

```python
# Primeiro, obter as opções disponíveis
fields = client.get_custom_fields(list_id)
priority_field = next(f for f in fields["fields"] if f["name"] == "Priority Level")

print("Opções disponíveis:")
for option in priority_field["type_config"]["options"]:
    print(f"  • {option['name']} (ID: {option['id']})")

# Definir prioridade
client.set_custom_field(
    task_id="abc123",
    field_id=priority_field["id"],
    value="option-uuid-high"  # ID da opção "High"
)
```

**Exemplo completo com busca automática:**

```python
def set_dropdown_by_name(client, task_id, list_id, field_name, option_name):
    """Helper para definir dropdown pelo nome da opção"""
    # Obter campos
    fields = client.get_custom_fields(list_id)

    # Encontrar campo
    field = next((f for f in fields["fields"] if f["name"] == field_name), None)
    if not field:
        print(f"Campo '{field_name}' não encontrado")
        return

    # Encontrar opção
    option = next(
        (opt for opt in field["type_config"]["options"] if opt["name"] == option_name),
        None
    )
    if not option:
        print(f"Opção '{option_name}' não encontrada")
        return

    # Definir valor
    return client.set_custom_field(task_id, field["id"], option["id"])

# Uso
set_dropdown_by_name(
    client,
    task_id="abc123",
    list_id="901234567",
    field_name="Priority Level",
    option_name="High"
)
```

### 7. Labels (Etiquetas - Múltipla Seleção)

```python
# Adicionar labels
client.set_custom_field(
    task_id="abc123",
    field_id="labels-field-id",
    value={
        "add": [
            "label-uuid-1",  # "Urgente"
            "label-uuid-2"   # "Cliente VIP"
        ],
        "remove": []
    }
)

# Remover labels
client.set_custom_field(
    task_id="abc123",
    field_id="labels-field-id",
    value={
        "add": [],
        "remove": ["label-uuid-3"]  # Remover "Em Espera"
    }
)

# Substituir (remover antigas e adicionar novas)
client.set_custom_field(
    task_id="abc123",
    field_id="labels-field-id",
    value={
        "add": ["label-uuid-4"],     # Adicionar "Concluído"
        "remove": ["label-uuid-1"]   # Remover "Urgente"
    }
)
```

### 8. Users (Usuários)

```python
# Adicionar usuários
client.set_custom_field(
    task_id="abc123",
    field_id="reviewers-field-id",
    value={
        "add": [123456, 789012],  # IDs dos usuários
        "remove": []
    }
)

# Trocar responsável
client.set_custom_field(
    task_id="abc123",
    field_id="assignee-field-id",
    value={
        "add": [999888],      # Novo responsável
        "remove": [123456]    # Antigo responsável
    }
)
```

### 9. Email

```python
client.set_custom_field(
    task_id="abc123",
    field_id="contact-email-id",
    value="cliente@empresa.com.br"
)
```

### 10. Phone

```python
client.set_custom_field(
    task_id="abc123",
    field_id="contact-phone-id",
    value="+55 11 99999-9999"
)

# Outros formatos aceitos
client.set_custom_field(
    task_id="abc123",
    field_id="phone-field-id",
    value="(11) 98888-7777"
)
```

### 11. URL

```python
client.set_custom_field(
    task_id="abc123",
    field_id="project-url-id",
    value="https://www.exemplo.com.br/projeto"
)

# Link do Figma
client.set_custom_field(
    task_id="abc123",
    field_id="design-link-id",
    value="https://www.figma.com/file/abc123/Design"
)
```

### 12. Location (Localização)

```python
# Endereço completo
client.set_custom_field(
    task_id="abc123",
    field_id="location-field-id",
    value={
        "formatted_address": "Av. Paulista, 1578 - Bela Vista, São Paulo - SP, 01310-200",
        "place_id": "ChIJAbCDeFGH...",  # Google Place ID (opcional)
        "lat": -23.5617,
        "lng": -46.6561
    }
)

# Localização simples (sem coordenadas)
client.set_custom_field(
    task_id="abc123",
    field_id="location-field-id",
    value={
        "formatted_address": "São Paulo, SP, Brasil"
    }
)
```

### 13. Manual Progress (Progresso Manual)

```python
# Progresso de 0 a 100
client.set_custom_field(
    task_id="abc123",
    field_id="progress-field-id",
    value=75  # 75% completo
)

# Projeto iniciado
client.set_custom_field(
    task_id="abc123",
    field_id="progress-field-id",
    value=10
)

# Projeto concluído
client.set_custom_field(
    task_id="abc123",
    field_id="progress-field-id",
    value=100
)
```

### 14. Tasks (Relação com outras tasks)

```python
# Adicionar tasks relacionadas
client.set_custom_field(
    task_id="abc123",
    field_id="related-tasks-id",
    value={
        "add": ["task-id-1", "task-id-2"],
        "remove": []
    }
)

# Remover relação
client.set_custom_field(
    task_id="abc123",
    field_id="blocked-by-id",
    value={
        "add": [],
        "remove": ["task-id-3"]
    }
)
```

### 15. Emoji

```python
client.set_custom_field(
    task_id="abc123",
    field_id="status-emoji-id",
    value="✅"
)

client.set_custom_field(
    task_id="abc123",
    field_id="priority-emoji-id",
    value="🔥"
)
```

---

## 🎯 Casos de Uso Reais

### Caso 1: Configurar Task de Projeto Completa

```python
# 1. Criar a task
task = client.create_task(
    list_id="901234567",
    name="Desenvolvimento do Website - Cliente XYZ",
    description="Criar site institucional responsivo",
    priority=2,  # Alta
    due_date="próxima sexta"
)

task_id = task["id"]

# 2. Configurar custom fields
from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix

# Orçamento
client.set_custom_field(task_id, "budget-field-id", 25000.00)

# Data de kickoff
kickoff_date = fuzzy_time_to_unix("próxima segunda")
client.set_custom_field(task_id, "kickoff-date-id", kickoff_date, time=True)

# Cliente aprovado?
client.set_custom_field(task_id, "client-approval-id", True)

# Status do projeto
client.set_custom_field(task_id, "project-status-id", "option-id-in-progress")

# Email do cliente
client.set_custom_field(task_id, "client-email-id", "contato@clientexyz.com.br")

# Labels
client.set_custom_field(
    task_id,
    "labels-field-id",
    {"add": ["label-vip", "label-urgent"], "remove": []}
)

print("✓ Task configurada com sucesso!")
```

### Caso 2: Atualizar Múltiplos Campos de Uma Vez

```python
# Definir campos a atualizar
custom_fields = {
    "budget-field-id": 30000.00,
    "progress-field-id": 50,
    "approved-field-id": True,
    "notes-field-id": "Projeto aprovado pelo cliente em reunião"
}

# Atualizar todos
results = client.set_multiple_custom_fields(task_id, custom_fields)

print(f"✓ {len([r for r in results if r])} campos atualizados com sucesso")
```

### Caso 3: Copiar Custom Fields de uma Task para Outra

```python
def copy_custom_fields(client, source_task_id, target_task_id):
    """Copia custom fields de uma task para outra"""

    # Obter task origem
    source_task = client.get_task(source_task_id)

    # Copiar cada custom field
    for field in source_task.get("custom_fields", []):
        field_id = field["id"]
        value = field.get("value")

        if value is not None:
            print(f"Copiando: {field['name']}")
            client.set_custom_field(target_task_id, field_id, value)

    print("✓ Custom fields copiados!")

# Uso
copy_custom_fields(client, "task-origem-id", "task-destino-id")
```

### Caso 4: Atualizar Progresso Baseado em Subtasks

```python
def update_progress_from_subtasks(client, task_id):
    """Calcula e atualiza progresso baseado em subtasks concluídas"""

    task = client.get_task(task_id)

    # Contar subtasks
    subtasks = task.get("subtasks", [])
    if not subtasks:
        print("Nenhuma subtask encontrada")
        return

    total = len(subtasks)
    completed = sum(1 for st in subtasks if st.get("status") == "complete")

    # Calcular porcentagem
    progress = int((completed / total) * 100)

    print(f"Progresso: {completed}/{total} subtasks ({progress}%)")

    # Atualizar campo de progresso
    client.set_custom_field(task_id, "progress-field-id", progress)

# Uso
update_progress_from_subtasks(client, "abc123")
```

### Caso 5: Validar e Formatar Dados Antes de Enviar

```python
def set_custom_field_safe(client, task_id, field_id, value, field_type):
    """Define custom field com validação de tipo"""

    # Validações por tipo
    if field_type == "number":
        try:
            value = float(value)
        except ValueError:
            print(f"Erro: '{value}' não é um número válido")
            return None

    elif field_type == "checkbox":
        if not isinstance(value, bool):
            value = str(value).lower() in ["true", "1", "yes", "sim"]

    elif field_type == "currency":
        try:
            value = round(float(value), 2)
        except ValueError:
            print(f"Erro: '{value}' não é um valor monetário válido")
            return None

    elif field_type == "email":
        if "@" not in str(value):
            print(f"Erro: '{value}' não é um email válido")
            return None

    elif field_type == "manual_progress":
        value = max(0, min(100, int(value)))  # Limita entre 0-100

    # Enviar para API
    return client.set_custom_field(task_id, field_id, value)

# Uso
set_custom_field_safe(client, "abc123", "field-id", "75.5", "number")
set_custom_field_safe(client, "abc123", "field-id", "yes", "checkbox")
```

---

## ❌ Tratamento de Erros

### Verificar se Custom Field Existe

```python
def field_exists(client, list_id, field_name):
    """Verifica se um custom field existe na lista"""
    fields = client.get_custom_fields(list_id)

    for field in fields.get("fields", []):
        if field["name"].lower() == field_name.lower():
            return True, field

    return False, None

# Uso
exists, field = field_exists(client, "901234567", "Budget")
if exists:
    print(f"Campo encontrado: {field['id']}")
else:
    print("Campo não encontrado")
```

### Tentar Atualizar com Fallback

```python
def set_custom_field_with_retry(client, task_id, field_id, value, max_retries=3):
    """Tenta atualizar custom field com retry"""
    import time

    for attempt in range(max_retries):
        result = client.set_custom_field(task_id, field_id, value)

        if result:
            return result

        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # Backoff exponencial
            print(f"Tentativa {attempt + 1} falhou. Aguardando {wait_time}s...")
            time.sleep(wait_time)

    print(f"Erro: Não foi possível atualizar após {max_retries} tentativas")
    return None
```

---

## 🔧 Troubleshooting

### Problema: "Field not found"

```python
# ❌ ERRADO: Usar nome do campo
client.set_custom_field(task_id, "Budget", 5000)

# ✅ CORRETO: Usar UUID do campo
client.set_custom_field(task_id, "b955c4dc-a6a7-4c05-9051-8d5f7e4f2c55", 5000)
```

### Problema: "Invalid value format"

```python
# ❌ ERRADO: Dropdown com nome da opção
client.set_custom_field(task_id, field_id, "High")

# ✅ CORRETO: Dropdown com UUID da opção
client.set_custom_field(task_id, field_id, "option-uuid-123")
```

### Problema: Data não aparece corretamente

```python
# ❌ ERRADO: Timestamp em segundos
client.set_custom_field(task_id, field_id, 1701388800)

# ✅ CORRETO: Timestamp em MILISSEGUNDOS
client.set_custom_field(task_id, field_id, 1701388800000)

# ✅ OU: Usar helper
from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix
timestamp = fuzzy_time_to_unix("2024-12-01")
client.set_custom_field(task_id, field_id, timestamp)
```

### Problema: Labels não atualizam

```python
# ❌ ERRADO: Enviar array direto
client.set_custom_field(task_id, field_id, ["label1", "label2"])

# ✅ CORRETO: Usar formato add/remove
client.set_custom_field(
    task_id,
    field_id,
    {"add": ["label1", "label2"], "remove": []}
)
```

---

**Autor:** Sistema Kaloi
**Data:** 2025-10-31
**Versão:** 1.0
