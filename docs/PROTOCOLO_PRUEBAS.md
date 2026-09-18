# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que se entrega.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6.

Cómo arrancar el programa: desde la raíz del repo, `python -m src.main`.

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y elegir la opción `1` | catálogo cargado en código | imprime las 7 canciones con id, título y detalle, sin traceback | no corrido |  |
| P02 | E1 | Opción `2` (ver detalle) y escribir un id que no existe | id = `99` | mensaje "No existe una canción con id 99.", el menú vuelve a aparecer | no corrido |  |
| P03 | E2 | Opción `5` (versiones derivadas) sobre una canción que tiene versiones | id = `6` (Hola) | imprime "Hola Remix" con el tipo `remix` | no corrido | caso de la traza del informe |
| P04 | E2 | Opción `5` sobre una canción sin versiones propias | id = `1` (Hola Remix) | imprime "(ninguna: esta canción no tiene versiones)", sin error — caso base | no corrido |  |
| P05 | E1 | Opción `2` con un id que sí existe | id = `4` (512) | muestra título, artista, álbum, género, año y duración | no corrido |  |
| P06 | E2 | Opción `2` sobre una canción que ES una versión | id = `5` (911 Remix) | además del detalle, avisa "(es una versión remix de otra canción)" | no corrido |  |
| P07 | E1 | Elegir una opción de menú que no existe | texto = `0z` | imprime "Opción no válida." y vuelve a mostrar el menú | no corrido |  |
| P08 | E1 | Apretar Enter sin escribir nada en el menú | entrada vacía | no explota; imprime "Opción no válida." y vuelve a preguntar | no corrido |  |
| P09 | E2 | Opción `2` y escribir letras en vez de un número | texto = `hola` | imprime "Tenés que escribir un número." y vuelve al menú, sin traceback | no corrido |  |
| P10 | E2 | Opción `5` sobre la canción "911" | id = `7` | imprime "911 Remix" con el tipo `remix` | no corrido |  |
