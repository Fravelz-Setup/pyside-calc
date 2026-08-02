---
description: Commit cambios actuales con Conventional Commits, sin trailer Co-authored-by de Cursor
---

# Autocommit — pyside-calc

Usar cuando el usuario pida **hacer commit** del trabajo actual. Mensajes **Conventional Commits**, coherentes con
`git log`. **No** hacer `git push` salvo petición explícita.

## Prohibido (Cursor / co-autor)

- **Nunca** dejar `Co-authored-by: Cursor` (ni variantes) en el mensaje.
- **Nunca** push si `git log -1 --format=%B` muestra trailer de agente/IDE.
- Usar **`git commit -F`** con archivo de mensaje limpio; verificar con `git log -1 --format=%B`.

Cumplir [`.cursor/rules/git-commits.mdc`](../rules/git-commits.mdc).

## Cuándo ejecutar

- Invocación de **`/auto-commit`** o petición explícita de commit.
- **No** commitear si el usuario no lo pidió.

## Antes de commitear

1. `git status` — staged y unstaged.
2. `git diff` — qué entra en el commit.
3. `git log -15 --oneline` — tono reciente.
4. **Respetar borrados:** si el diff elimina líneas o archivos, **no restaurarlos** ni "arreglar" el contenido antes del commit salvo petición explícita del usuario.
5. Rama: **`main`**.

**No** incluir: `.venv/`, `__pycache__/`, logs, credenciales.

## Scopes habituales

`calc`, `ui`, `engine`, `theme`, `scripts`, `cursor`, `docs`, `deps`.

Rutas: `src/pyside_calc/`, `scripts/`, `.cursor/`, `README.md`.

## Ejemplos

```text
feat(calc): add floating PySide calculator for Super+=
fix(engine): treat caret as power operator
docs: document Sway binding and install
```

## Commit (obligatorio con `-F`)

```bash
cat > /tmp/commit-msg.txt <<'EOF'
feat(calc): add floating PySide calculator for Super+=
EOF
git commit -F /tmp/commit-msg.txt
git log -1 --format=%B
```

## Reglas

- Mensaje en **inglés**; respuesta al chat en **español**.
- Hook rechazado → corregir y **nuevo** commit; sin `--no-verify` salvo petición explícita.
