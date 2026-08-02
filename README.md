# pyside-calc

Calculadora flotante en PySide6 para Sway. Sustituye la antigua calculadora Rofi en **`Super+=`**.

## Uso

- `Super+=` abre la ventana (binding de Sway → `~/.local/bin/pyside-calc`)
- Izquierda: escribe una expresión (`10+10`, `2^8`, `(3+1)*2`)
- Aparece `expr = resultado`; **Enter** o clic copia el número (`wl-copy`) y notifica
- Derecha: panel **Notas** (se guarda en `~/.local/share/pyside-calc/notes.txt`)
- **Escape** cierra

## Instalación local

```bash
cd ~/Documentos/personal/pyside-calc
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
chmod +x scripts/pyside-calc
ln -sfn "$(pwd)/scripts/pyside-calc" ~/.local/bin/pyside-calc
```

Binding en Sway:

```
bindsym $mod+equal exec ~/.local/bin/pyside-calc
```

## Desarrollo

```bash
.venv/bin/python -m pyside_calc
```

## Licencia

Uso personal.
