from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError

class Playlist:
    def __init__(self, tope=6):
        self._canciones = ListaEnlazada()
        self._tope = tope

    def agregar(self, cancion):
        if self._canciones.tamanio() >= self._tope:
            raise ColeccionLlenaError(f"La playlist está llena (máximo {self._tope} canciones).")
        self._canciones.insertar_al_final(cancion)

    def esta_vacia(self):
        return self._canciones.esta_vacia()

    def __iter__(self):
        for cancion in self._canciones:
            yield cancion