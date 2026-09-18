"""Catálogo de canciones y relación recursiva de versiones (covers/remixes).

En E1 y E2 el catálogo se arma a mano en el código. Los .txt de data/ se
empiezan a leer recién en E5 (no se tocan hasta esa entrega).
"""

from src.dominio.cancion import Cancion

# (id, titulo, artista, album, genero, anio, duracion_seg)
_DATOS_CANCIONES = [
    (1, "Hola Remix", "Dalex, Rauw Alejandro, Lenny Tavarez, Chencho Corleone",
     "Climaxxx", "Urbano", 2019, 288),
    (2, "China", "Anuel AA, Daddy Yankee, Karol G, Ozuna, J Balvin",
     "Emmanuel", "Urbano", 2019, 301),
    (3, "La Canción", "J Balvin, Bad Bunny", "Oasis", "Urbano", 2019, 242),
    (4, "512", "Mora, Jhay Cortez", "MicroDosis", "Urbano", 2020, 193),
    (5, "911 Remix", "Sech, Jhay Cortez", "42", "Urbano", 2021, 215),
    # Originales agregadas para que los remixes de arriba tengan de qué
    # canción derivan (necesario para la recursión del ítem 2 de E2).
    (6, "Hola", "Dalex", "Climaxxx", "Urbano", 2019, 210),
    (7, "911", "Sech", "42", "Urbano", 2021, 198),
]

# (cancion_id, version_de_id, tipo): la canción de la izquierda es una
# versión derivada de la de la derecha.
_DATOS_VERSIONES = [
    (1, 6, "remix"),   # Hola Remix   es remix de Hola
    (5, 7, "remix"),   # 911 Remix    es remix de 911
]


class Biblioteca:
    """El catálogo completo de canciones más la relación de versiones."""

    def __init__(self):
        self._canciones = []
        self._versiones = []

    def cargar_datos_iniciales(self):
        """Arma el catálogo en memoria a partir de los datos del módulo."""
        for fila in _DATOS_CANCIONES:
            self._canciones.append(Cancion(*fila))
        for fila in _DATOS_VERSIONES:
            self._versiones.append(fila)

    def cantidad(self):
        return len(self._canciones)

    def listar(self):
        """Devuelve las canciones del catálogo."""
        return list(self._canciones)

    def buscar_por_id(self, id_cancion):
        """Devuelve la canción con ese id o None si no está."""
        for cancion in self._canciones:
            if cancion.id == id_cancion:
                return cancion
        return None

    def versiones_directas(self, id_cancion):
        """Ids de las canciones que son versión directa de id_cancion."""
        derivadas = []
        for cancion_id, version_de_id, _tipo in self._versiones:
            if version_de_id == id_cancion:
                derivadas.append(cancion_id)
        return derivadas

    def tipo_de_version(self, id_cancion):
        """Devuelve 'remix'/'cover'/'live', o None si es una canción original."""
        for cancion_id, _version_de_id, tipo in self._versiones:
            if cancion_id == id_cancion:
                return tipo
        return None

    def versiones_de(self, id_cancion):
        """RECURSIVA: todas las versiones derivadas de una canción.

        Incluye también las versiones de las versiones (por eso hace falta
        recursión y no alcanza con un for simple).

        Caso base: la canción no tiene versiones directas -> devuelve [].
        Caso recursivo: por cada versión directa, se agrega esa versión al
        resultado y se suma lo que devuelva versiones_de llamada sobre ella.
        """
        directas = self.versiones_directas(id_cancion)
        if not directas:                       # CASO BASE
            return []
        resultado = []
        for id_version in directas:            # CASO RECURSIVO
            resultado.append(id_version)
            resultado += self.versiones_de(id_version)
        return resultado
