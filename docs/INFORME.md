# Informe del Proyecto — Biblioteca Musical

## 1. Elección del Tema
Elegimos el tema Biblioteca Musical porque nos permite estructurar adecuadamente colecciones de canciones, listas de reproducción e historiales de reproducción.  Las entidades principales tienen atributos claros como título, artista, álbum y duración.

## 2. Justificación de Tipos Utilizados (Mutabilidad e Inmutabilidad)
- **Catálogo (`list`):** Es una estructura mutable. La utilizamos para almacenar el catálogo general porque en entregas posteriores realizaremos modificaciones.
- **Atributos de las canciones (`str`, `int`):** Los usamos para los datos individuales de cada canción (título, artista, álbum y duración). Son inmutables, lo que evita que la información de una canción se modifique por error..
- **Registros individuales (`dict`):** Cada canción es un diccionario. Lo usamos porque nos permite guardar los datos organizados por nombre, como "titulo" o "artista".

*Actualización E2: en esta entrega pasamos cada canción de diccionario a un objeto de la clase `Cancion` (en `src/dominio/cancion.py`), porque la rúbrica de E2 pide clases del dominio, no diccionarios sueltos. El id de cada canción quedó como atributo de solo lectura (`@property` sin setter) porque es la identidad del registro y no debe cambiar; el resto de los atributos siguen siendo mutables.*

## 3. Recursión (E2)

- **Función:** `Biblioteca.versiones_de(id_cancion)`, en `src/dominio/biblioteca.py`
- **Qué hace:** dada una canción, devuelve los ids de todas las canciones que son versión derivada de ella (remixes o covers), incluyendo las versiones de esas versiones.
- **Caso base:** si la canción no tiene versiones directas (`versiones_directas` devuelve una lista vacía), la función devuelve `[]` y no sigue.
- **Caso recursivo:** por cada versión directa encontrada, se agrega su id al resultado y se le suma lo que devuelva `versiones_de` llamada sobre esa versión.

### Traza de un ejemplo real del dataset

Datos usados (relación de versiones armada a mano hasta que se lea `data/versiones.txt` en E5):

```text
1, 6, remix     -> la canción 1 (Hola Remix) es un remix de la canción 6 (Hola)
```

**Traza de `versiones_de(6)`** (id de "Hola", la canción original):

```text
Llamada 1: versiones_de(6)
  versiones_directas(6) -> [1]        (no está vacía, NO es caso base)
  resultado = []
  entra al for con id_version = 1
  resultado.append(1)  -> resultado = [1]
  necesita el valor de versiones_de(1), se apila la llamada 2

  Llamada 2: versiones_de(1)
    versiones_directas(1) -> []       (vacía -> CASO BASE)
    devuelve []                        <- se desapila

  vuelve a la llamada 1: resultado += [] -> resultado sigue [1]
  devuelve [1]

Resultado final: [1]
```

Salida por pantalla (opción 5 del menú, id 6):

```text
Versiones derivadas de «Hola»:
  [ 1] Hola Remix - Dalex, Rauw Alejandro, Lenny Tavarez, Chencho Corleone  [remix]
```

**Traza del caso base puro, `versiones_de(1)`** (la canción "Hola Remix", que no tiene versiones propias):

```text
Llamada 1: versiones_de(1)
  versiones_directas(1) -> []         (CASO BASE, no se apila nada más)
  devuelve []

Resultado final: []
```

Salida por pantalla (opción 5 del menú, id 1):

```text
Versiones derivadas de «Hola Remix»:
  (ninguna: esta canción no tiene versiones)
```


## 4.  Estructuras de Datos Propias y Manejo de Excepciones (E3)

### 1. Estructura de Datos Elegida
Para el manejo del catálogo y la playlist se implementó una **`ListaEnlazada`** propia basada en nodos (`Nodo`), evitando el uso de las listas nativas de Python (`list`). 

* **Iterador:** La clase `ListaEnlazada` implementa los métodos mágicos `__iter__` y `__next__`, lo que permite recorrer la playlist e imprimir las canciones de forma limpia utilizando bucles `for`.
* **Pila (LIFO):** La clase `Pila` utiliza internamente `ListaEnlazada` para gestionar el historial de acciones y permitir la funcionalidad de deshacer (`Deshacer última acción`).
* **Cola (FIFO):** La clase `Cola` utiliza internamente `ListaEnlazada` para encolar canciones y reproducirlas en orden de llegada.

### 2. Colección con Tope y Excepciones
La `Playlist` posee un límite/tope máximo de elementos. Cuando se intenta superar dicho límite o se opera sobre estructuras vacías, el sistema lanza excepciones personalizadas heredadas de `Exception` (definidas en `src/excepciones.py`):
* `ColeccionLlenaError`: Se dispara al intentar agregar una canción cuando la playlist alcanzó su capacidad máxima.
* `PilaVaciaError` y `ColaVaciaError`: Se disparan al intentar desapilar o desencolar cuando no hay elementos disponibles.

Todas estas excepciones son capturadas en `main.py` mediante bloques `try / except` para informar adecuadamente al usuario por consola sin interrumpir la ejecución del programa.