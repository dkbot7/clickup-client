# 📊 Resumo Executivo: Custom Fields

**TL;DR - O que você precisa saber sobre Custom Fields na API ClickUp**

---

## ⚡ Quick Facts

| Aspecto | Informação |
|---------|------------|
| **Endpoint principal** | `POST /task/{task_id}/field/{field_id}` |
| **Tipos suportados** | 16 tipos diferentes |
| **Atualização em lote** | ❌ NÃO SUPORTADO - requer 1 chamada por campo |
| **Identificação** | UUID obrigatório (não aceita nome) |
| **Limitação plano free** | 60 usos totais (não resetam) |
| **Complexidade** | 🟡 Média |

---

## ✅ O Que Funciona

```python
# ✅ Atualizar um campo por vez
client.set_custom_field(task_id, field_id, value)

# ✅ Criar task com múltiplos custom fields
client.create_task(
    list_id="123",
    name="Task",
    custom_fields=[
        {"id": "field1", "value": "valor1"},
        {"id": "field2", "value": 42}
    ]
)
```

---

## ❌ O Que NÃO Funciona

```python
# ❌ Update task não suporta custom fields
client.update_task(task_id, custom_fields=[...])  # ERRO!

# ❌ Não aceita nome do campo
client.set_custom_field(task_id, "Budget", 5000)  # ERRO!

# ❌ Não aceita nome da opção em dropdown
client.set_custom_field(task_id, field_id, "High")  # ERRO!
```

---

## 🎨 Tipos Mais Usados

### Top 5 Essenciais

1. **`short_text`** - Texto curto (1 linha)
   ```python
   client.set_custom_field(task_id, field_id, "Texto aqui")
   ```

2. **`number`** - Números
   ```python
   client.set_custom_field(task_id, field_id, 42.5)
   ```

3. **`checkbox`** - Verdadeiro/Falso
   ```python
   client.set_custom_field(task_id, field_id, True)
   ```

4. **`date`** - Datas
   ```python
   client.set_custom_field(task_id, field_id, 1701388800000)  # Unix ms
   ```

5. **`drop_down`** - Lista suspensa
   ```python
   client.set_custom_field(task_id, field_id, "option-uuid-123")
   ```

---

## 🔑 3 Passos Essenciais

### 1. Obter Field ID

```python
fields = client.get_custom_fields(list_id)
field_id = next(f["id"] for f in fields["fields"] if f["name"] == "Budget")
```

### 2. Formatar Valor Corretamente

```python
# Texto/Number/Checkbox - valor direto
value = "texto" | 42 | True

# Dropdown - UUID da opção
value = "option-uuid-from-type-config"

# Labels/Users/Tasks - formato add/remove
value = {"add": ["id1"], "remove": ["id2"]}

# Date - Unix timestamp em MILISSEGUNDOS
value = 1701388800000  # Não em segundos!
```

### 3. Enviar para API

```python
result = client.set_custom_field(task_id, field_id, value)
```

---

## ⚠️ Principais Armadilhas

### 1. Timestamp em segundos vs milissegundos
```python
# ❌ ERRADO
timestamp = 1701388800  # Segundos

# ✅ CORRETO
timestamp = 1701388800000  # Milissegundos (x1000)
```

### 2. Usar nome em vez de UUID
```python
# ❌ ERRADO
field_id = "Budget"

# ✅ CORRETO
field_id = "b955c4dc-a6a7-4c05-9051-8d5f7e4f2c55"
```

### 3. Formato de dropdown
```python
# ❌ ERRADO - nome da opção
value = "High"

# ✅ CORRETO - UUID da opção
value = "option-uuid-123"
```

### 4. Formato de labels/users
```python
# ❌ ERRADO - array direto
value = ["label1", "label2"]

# ✅ CORRETO - add/remove
value = {"add": ["label1", "label2"], "remove": []}
```

---

## 💰 Custo de Uso

### Plano Free Forever
- **Limite:** 60 usos TOTAIS no workspace
- **Cada chamada:** 1 uso
- **Reset:** NUNCA (limite permanente)

### Cálculo de Uso
```python
# Atualizar 5 custom fields em 1 task = 5 usos
for field_id, value in fields.items():
    client.set_custom_field(task_id, field_id, value)  # +1 uso cada

# Criar task com 5 custom fields = 0 usos extras
client.create_task(
    list_id="123",
    name="Task",
    custom_fields=[...]  # Não conta para limite
)
```

**💡 Dica:** Use `create_task()` com custom_fields sempre que possível!

---

## 📝 Receita Básica

```python
from src.clickup_api.client import KaloiClickUpClient
from src.clickup_api.helpers.date_utils import fuzzy_time_to_unix

# 1. Inicializar
client = KaloiClickUpClient()

# 2. Obter field IDs (fazer uma vez, cachear)
fields = client.get_custom_fields(list_id="901234567")
budget_field_id = next(f["id"] for f in fields["fields"] if f["name"] == "Budget")
date_field_id = next(f["id"] for f in fields["fields"] if f["name"] == "Due Date")

# 3. Atualizar campos
client.set_custom_field(task_id, budget_field_id, 15000.00)
client.set_custom_field(task_id, date_field_id, fuzzy_time_to_unix("próxima segunda"))

print("✓ Custom fields atualizados!")
```

---

## 🚀 Próximos Passos

1. **Ler:** [CUSTOM_FIELDS_RESEARCH.md](CUSTOM_FIELDS_RESEARCH.md) - Pesquisa completa
2. **Praticar:** [CUSTOM_FIELDS_EXAMPLES.md](CUSTOM_FIELDS_EXAMPLES.md) - 15+ exemplos
3. **Implementar:** Ver checklist em CUSTOM_FIELDS_RESEARCH.md

---

## 📚 Recursos

- **Documentação oficial:** https://developer.clickup.com/docs/customfields
- **Endpoint:** https://developer.clickup.com/reference/setcustomfieldvalue
- **Lib Python recomendada:** https://github.com/Stashchen/pyclickup

---

**Criado em:** 2025-10-31
**Autor:** Sistema Kaloi
**Tempo de leitura:** 3 minutos
