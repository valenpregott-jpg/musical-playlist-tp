# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que se entrega.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6.

Cómo arrancar el programa: desde la raíz del repo, `python -m src.main`.

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar el programa y elegir la opción `1` | catálogo cargado en código | imprime las canciones con id, título y detalle, sin traceback | pasa | Verificado en E3 |
| P02 | E1 | Opción `2` (ver detalle) y escribir un id que no existe | id = `99` | mensaje "No existe una canción con id 99.", el menú vuelve a aparecer | pasa | Verificado en E3 |
| P03 | E2 | Opción `5` (versiones derivadas) sobre una canción que tiene versiones | id = `6` (Hola) | imprime "Hola Remix" con el tipo `remix` | pasa | caso de la traza del informe |
| P04 | E2 | Opción `5` sobre una canción sin versiones propias | id = `1` (Hola Remix) | imprime "(ninguna: esta canción no tiene versiones)", sin error — caso base | pasa | Verificado en E3 |
| P05 | E1 | Opción `2` con un id que sí existe | id = `4` (512) | muestra título, artista, álbum, género, año y duración | pasa | Verificado en E3 |
| P06 | E2 | Opción `2` sobre una canción que ES una versión | id = `5` (911 Remix) | además del detalle, avisa "(es una versión remix de otra canción)" | pasa | Verificado en E3 |
| P07 | E1 | Elegir una opción de menú que no existe | texto = `0z` | imprime "Opción no válida." y vuelve a mostrar el menú | pasa | Verificado en E3 |
| P08 | E1 | Apretar Enter sin escribir nada en el menú | entrada vacía | no explota; imprime "Opción no válida." y vuelve a preguntar | pasa | Verificado en E3 |
| P09 | E2 | Opción `2` y escribir letras en vez de un número | texto = `hola` | imprime "Tenés que escribir un número." y vuelve al menú, sin traceback | pasa | Verificado en E3 |
| P10 | E2 | Opción `5` sobre la canción "911" | id = `7` | imprime "911 Remix" con el tipo `remix` | pasa | Verificado en E3 |
| P11 | E3 | Opción `6` (agregar a playlist) hasta superar el tope de 6 | 7 canciones cargadas | Muestra cartel de error "ColeccionLlenaError" al querer meter la 7ma canción | pasa | Colección con tope |
| P12 | E3 | Opción `7` (listar playlist) | playlist con canciones | Recorre y muestra los temas usando el iterador propio de ListaEnlazada | pasa | Iterador |
| P13 | E3 | Opción `8` (encolar/desencolar) con la cola vacía | cola sin temas | Lanza y captura ColaVaciaError sin romper la app | pasa | Cola FIFO |
| P14 | E3 | Opción `9` (deshacer) con el historial vacío | pila vacía | Lanza y captura PilaVaciaError indicando que no hay acciones para deshacer. | pasa | Pila LIFO |
