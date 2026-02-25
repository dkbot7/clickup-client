---
id: TAG-03
titulo: Tag "bloqueado" → Task de Desbloqueio
departamento: Geral
space: Projetos
ferramenta: ClickUp Nativo
prioridade: MÉDIA
tempo_setup: 3 min
economia_mensal: 1h
status: pendente
---

# TAG-03 — Tag "bloqueado" → Task de Desbloqueio

## O que faz
Quando a tag **`bloqueado`** é adicionada a uma task, cria automaticamente uma task de desbloqueio e notifica o responsável.

## Por que é importante
Garante que impedimentos sejam tratados formalmente com um item de ação — nenhum bloqueio fica sem responsável.

## Como criar no ClickUp

1. Abrir o Space **Projetos**
2. Ir em **Automations**
3. Clicar em **+ Add Automation**
4. Configurar:

```
TRIGGER:
  Tipo: Tag added
  Condição: Tag "bloqueado" is added

ACTIONS:
  1. Post comment → "🔒 TASK BLOQUEADA! Uma task de desbloqueio foi criada automaticamente."
  2. Create task →
      Name: "🔓 DESBLOQUEAR: [task name]"
      List: [mesma list da task original]
      Priority: High
      Tags: desbloqueio, impedimento
      Description: "Esta task foi criada automaticamente porque [task original] está bloqueada.\n\nAções:\n1. Identificar a causa do bloqueio\n2. Definir responsável pela resolução\n3. Estimar prazo de resolução\n4. Remover tag 'bloqueado' quando resolvido"
```

5. Nomear: `[TAG-03] Tag bloqueado → Task desbloqueio`
6. Ativar e testar

## Resultado esperado
- Task de desbloqueio criada imediatamente
- Comentário visível na task bloqueada
- Impedimento rastreável e com responsável

## Observações
- Ao resolver o bloqueio, remover manualmente a tag `bloqueado`
- Considerar criar automação reversa: tag removida → fechar task de desbloqueio
