---
id: PRJ-01
titulo: Checklist "Testes e Validação" 100% → Status Monitoramento
departamento: Projetos
space: Projetos
list: Projetos Internos
list_id: "901307128249"
ferramenta: ClickUp Nativo
prioridade: ALTA
tempo_setup: 3 min
economia_mensal: 1h/semana
status: pendente
---

# PRJ-01 — Checklist "Testes e Validação" 100% → Status Monitoramento

## O que faz
Quando o checklist **"Testes e Validação"** de uma task atinge **100%** (todos os itens marcados), muda automaticamente o status para `monitoramento` e adiciona a tag `testado`.

## Por que é importante
Elimina a necessidade de mudança manual de status — o workflow avança automaticamente quando a etapa de testes é concluída.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Checklist updated
  Condição: Checklist "Testes e Validação" is 100% complete

ACTIONS:
  1. Change status → monitoramento
  2. Add tag → "testado"
  3. Post a comment → "✅ Testes e validação concluídos! Status atualizado para Monitoramento."
```

5. Nomear: `[PRJ-01] Checklist Testes → Status Monitoramento`
6. Ativar e testar

## Resultado esperado
- Status muda para `monitoramento` automaticamente
- Tag `testado` adicionada
- Comentário registra a transição

## Observações
- O nome do checklist deve ser exatamente "Testes e Validação" (case-sensitive)
- Complementado por PRJ-02 que atualiza o campo Fase
