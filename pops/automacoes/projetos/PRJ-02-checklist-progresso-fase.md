---
id: PRJ-02
titulo: Checklist Progresso → Atualizar Campo Fase
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 5 min
economia_mensal: 1h/semana
status: pendente
---

# PRJ-02 — Checklist Progresso → Atualizar Campo "Fase"

## O que faz
Conforme o progresso geral dos checklists de uma task avança (25%, 50%, 75%, 100%), atualiza automaticamente o custom field **"Fase"**.

## Por que é importante
Mantém o campo Fase sempre sincronizado com o progresso real da task sem esforço manual.

## Mapeamento de Fases

| Progresso | Fase |
|-----------|------|
| 25% | Iniciação |
| 50% | Execução |
| 75% | Revisão |
| 100% | Entrega |

## Como criar no ClickUp

Criar **4 automações separadas** (uma para cada marco):

### Automação 1 - 25%
```
TRIGGER: Checklist progress reaches 25%
ACTION: Set custom field "Fase" = "Iniciação"
```

### Automação 2 - 50%
```
TRIGGER: Checklist progress reaches 50%
ACTION: Set custom field "Fase" = "Execução"
```

### Automação 3 - 75%
```
TRIGGER: Checklist progress reaches 75%
ACTION: Set custom field "Fase" = "Revisão"
```

### Automação 4 - 100%
```
TRIGGER: Checklist progress reaches 100%
ACTION: Set custom field "Fase" = "Entrega"
ACTION: Add tag → "entregue"
```

Nomear cada uma: `[PRJ-02] Checklist [X%] → Fase [nome]`

## Resultado esperado
- Campo Fase sempre atualizado automaticamente
- Visibilidade clara da fase atual de cada projeto

## Observações
- O custom field "Fase" deve existir no Space Projetos
- Se não existir, criar antes de configurar as automações
