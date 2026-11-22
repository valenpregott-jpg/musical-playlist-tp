# TP Integrador — AyED C2 2026 — Biblioteca Musical (`MUSICA`) — Grupo 32

## Integrantes

| Nombre | Mail | GitHub |
| --- | --- | --- |
| Joaquín Luisetto | luisettojoaquin86@gmail.com | [@joaquinluisetto13-ux](https://github.com/joaquinluisetto13-ux) |
| Valentín Pregot Villalba | valenpregot@gmail.com | [@valenpregott-jpg](https://github.com/valenpregott-jpg) |
| Alex Cazas | alexcazas37@gmail.com | [@Alexcazas37](https://github.com/Alexcazas37) |

## Tema
**Biblioteca musical**: gestor de catálogo musical por consola que permite administrar canciones, playlists con tope, cola de reproducción, búsquedas, ordenamientos, relaciones recursivas de versiones (covers/remixes) y persistencia en archivos de texto y binarios.

## Cómo ejecutarlo
Requiere Python 3.10 o superior (utiliza únicamente la biblioteca estándar; no hay `requirements.txt` a propósito). Desde la raíz del repositorio:

```bash
python -m src.main
```

En Windows, si `python` no anda: `py -3 -m src.main`.

## Qué hace

Gestor de catálogo musical por consola con las 10 operaciones del menú: listar, ver detalle, buscar (lineal y binaria), ordenar (selección e inserción), ver versiones derivadas (recursión), ABM persistente del catálogo (alta/baja/modificación con acceso directo por `seek` en el binario), gestión de una playlist con tope, cola de reproducción FIFO, y guardado/carga del catálogo en texto simple (`.txt`) y binario de longitud fija (`.bin`).

## Limitaciones conocidas

- No hay interfaz gráfica ni web: todo es por consola.
- El catálogo es el elegido por el grupo (no se admite cargar un dataset de otro tema sin adaptar `src/config.py`).
- No se valida que los campos de texto (título, artista, etc.) respeten el ancho fijo del registro binario antes de truncarlos — un valor muy largo se recorta silenciosamente al guardar en `.bin`.