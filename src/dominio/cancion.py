"""Entidad del catálogo: una canción de la biblioteca musical."""


class Cancion:
    """Una canción del catálogo.

    El id es la identidad del registro y no cambia (inmutable por criterio
    del grupo). El resto de los atributos son mutables: se pueden corregir
    si algún dato vino mal cargado.
    """

    def __init__(self, id, titulo, artista, album, genero, anio, duracion_seg):
        self._id = id
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.genero = genero
        self.anio = anio
        self.duracion_seg = duracion_seg

    @property
    def id(self):
        return self._id

    def duracion_formateada(self):
        minutos = self.duracion_seg // 60
        segundos = self.duracion_seg % 60
        return f"{minutos}m {segundos:02d}s"

    def linea_corta(self):
        return f"[{self.id:>2}] {self.titulo} - {self.artista}"

    def detalle(self):
        return (
            f"     Álbum: {self.album} | Género: {self.genero} | "
            f"Año: {self.anio} | Duración: {self.duracion_formateada()}"
        )

    def __str__(self):
        return self.linea_corta()
