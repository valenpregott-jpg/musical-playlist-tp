# Protocolo de pruebas

Pruebas **manuales**. Cada fila es un caso. Ejecutar sobre el tag que se entrega.

Leyenda de resultado: `pasa` / `no pasa` / `no corrido`.

Mínimos: 8 casos escritos en E2; ejecutados en E3; 15 de regresión en E6.

Cómo arrancar el programa: desde la raíz del repo, `python -m src.main`.

## Protocolo de regresión final (P01–P15, numeración de cátedra)

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | E1 | Arrancar (`python -m src.main`) y elegir la opción `1` | catálogo cargado desde `data/canciones.txt` | imprime las canciones con id, título y detalle, sin traceback | pasa | |
| P02 | E1 | Opción `2` (ver detalle) con un id que no existe | id = `99` | "No existe una canción con id 99.", el menú vuelve a aparecer | pasa | |
| P03 | E2 | Opción `5` (versiones derivadas) sobre un ítem con cadena de versiones | id = `6` (Hola) | imprime "Hola Remix" con el tipo `remix` | pasa | Caso recursivo |
| P04 | E2 | Opción `5` sobre un ítem sin derivados | id = `1` (Hola Remix) | "(ninguna: esta canción no tiene versiones)", sin error | pasa | Caso base |
| P05 | E3 | Opción `7` → `a`, agregar a la Playlist hasta superar el tope de 6 | 7 canciones | Al intentar la 7ma, muestra el error de `ColeccionLlenaError` | pasa | Colección con tope |
| P06 | E3 | Opción `9` → `f` (deshacer) con el historial recién arrancado (vacío) | pila vacía | Lanza y captura `PilaVaciaError`, mensaje claro, sin traceback | pasa | Pila LIFO |
| P07 | E3 | Opción `8` → `b` (reproducir siguiente) sin haber encolado nada antes | cola vacía | Lanza y captura `ColaVaciaError`, mensaje claro, sin traceback | pasa | Cola FIFO — opción 8 separada en `a`/`b` para poder probar este caso |
| P08 | E3 | Opción `7` → `a` (agregar) y después `7` → `b` (listar) | playlist con canciones agregadas en orden | Recorre y muestra los temas en el mismo orden de inserción, usando el iterador propio de `ListaEnlazada` | pasa | Iterador |
| P09 | E4 | Opción `3` → `1` (búsqueda lineal) de un título que existe | título = `Hola` | Lo encuentra y lo muestra correctamente | pasa | Búsqueda lineal propia |
| P10 | E4 | Opción `3` → `1` (búsqueda lineal) de un título que no existe | título inexistente | Muestra "No se encontró...", sin traceback | pasa | |
| P11 | E4 | Opción `3` → `2` (búsqueda binaria) con el catálogo todavía sin ordenar | título existente | Avisa que no está ordenado, reordena por título (inserción) y encuentra | pasa | Cumple la regla dura del ítem |
| P12 | E4 | Opción `4`: ordenar por un criterio y algoritmo, y después por otro criterio/algoritmo | catálogo cargado | El orden de la colección cambia correctamente cada vez | pasa | Sin `sorted`/`list.sort` |
| P13 | E5 | Opción `9` → `b` (guardar `.txt`), salir del programa (`0`), volver a entrar y listar (`1`) | catálogo con alta/modificación reciente | Los datos persisten tras reiniciar el programa | pasa | Persistencia texto simple |
| P14 | E5 | Opción `9` → `c` (guardar `.bin`), modificar canción por id (`6` → `b`, usa `seek`), recargar `.bin` (`9` → `d`) y listar (`1`) | id existente | El registro se actualiza por posición (acceso directo) y refleja el nuevo valor al recargar | pasa | `actualizar_registro` |
| P15 | E5 | Opción `9` → `e`, cargar un archivo basura (sin la magia `AYED`) | archivo corrupto | Lanza `ArchivoInvalidoError` con mensaje claro, el menú continúa sin traceback | pasa | Sin traceback |

## Casos adicionales de entregas anteriores (no reemplazan a los de arriba)

| ID | Entrega | Acción (pasos en el CLI) | Datos | Resultado esperado | Resultado | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| P16 | E1 | Elegir una opción de menú que no existe | texto = `0z` | "Opción no válida." y vuelve a mostrar el menú | pasa | |
| P17 | E1 | Apretar Enter sin escribir nada en el menú | entrada vacía | no explota; "Opción no válida." y vuelve a preguntar | pasa | |
| P18 | E2 | Opción `2` y escribir letras en vez de un número | texto = `hola` | "Tenés que escribir un número." y vuelve al menú, sin traceback | pasa | |
| P19 | E2 | Opción `2` sobre una canción que ES una versión | id = `5` (911 Remix) | Además del detalle, avisa "(es una versión remix de otra canción)" | pasa | |
| P20 | E2 | Opción `5` sobre la canción "911" | id = `7` | imprime "911 Remix" con el tipo `remix` | pasa | |
