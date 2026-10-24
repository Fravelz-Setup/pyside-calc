<h1 align="center">pyside-calc</h1>

<p align="center">
  <img src="assets/readme-hero.jpg" alt="Banner carbón y papel de la calculadora flotante" width="100%">
</p>

<p align="center">Calculadora flotante para Sway. Cerrada en ese tamaño.</p>

Se abre con Super+=. Escribe la expresión, Enter copia el número con `wl-copy`. El panel de notas guarda en `~/.local/share/pyside-calc/notes.txt`.

<p align="center">
  <a href="https://skillicons.dev">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=py,linux&theme=dark&perline=6">
      <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=py,linux&theme=light&perline=6">
      <img alt="Python, Linux" src="https://skillicons.dev/icons?i=py,linux&perline=6">
    </picture>
  </a>
</p>

## Características

- Ventana flotante para una expresión.
- Copia el resultado al portapapeles de Wayland.
- Cerrada: no va a crecer más allá de la calculadora.

> [!NOTE]
> El atajo de Sway es `bindsym $mod+equal exec ~/.local/bin/pyside-calc`.

## Tecnologías

- **Python y PySide6** — la ventana.
- **wl-copy** — copiar el resultado en Sway.

## Inicio rápido

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
ln -sfn "$(pwd)/scripts/pyside-calc" ~/.local/bin/pyside-calc
```

> [!IMPORTANT]
> Hace falta el venv y el enlace en `~/.local/bin`. Sin eso, Super+= no encuentra el comando.

## Uso

Escribe `10+10` o `(3+1)*2`. Enter copia el número y cierra la cuenta. Escape cierra la ventana.

> [!TIP]
> Para probar sin el atajo: `.venv/bin/python -m pyside_calc`.

## Contribuir

> [!CAUTION]
> Está cerrada en este tamaño. No la conviertas en otra calculadora.

Repositorio de [FraVelz](https://github.com/FraVelz).

## Licencia

Este repositorio no incluye un archivo de licencia. El uso previsto es personal.
