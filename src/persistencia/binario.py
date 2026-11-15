# src/persistencia/binario.py
import struct
from pathlib import Path
from src.excepciones import ArchivoInvalidoError
from src.dominio.cancion import Cancion

# Formato Música según guía §4.2:
# id (4B), titulo (30B), artista (25B), album (30B), genero (12B), anio (2B), duracion_seg (2B) = 105 bytes
FORMATO = struct.Struct("<I 30s 25s 30s 12s 2H")
HEADER = struct.Struct("<4s 1s I")  # 9 bytes: magia (AYED), tema (M), cantidad
TEMA = b"M"


def _a_bytes(texto, ancho):
    """Convierte texto a bytes UTF-8 de ancho exacto: recorta o rellena con \\x00."""
    return str(texto).encode("utf-8")[:ancho].ljust(ancho, b"\x00")


def _a_texto(datos):
    """Convierte bytes a texto limpio quitando los \\x00 del final."""
    return datos.rstrip(b"\x00").decode("utf-8", errors="ignore")


def _item_a_tupla(c):
    """Convierte un objeto Cancion en tupla lista para FORMATO.pack."""
    return (
        int(c.id),
        _a_bytes(c.titulo, 30),
        _a_bytes(c.artista, 25),
        _a_bytes(c.album, 30),
        _a_bytes(c.genero, 12),
        int(c.anio),
        int(c.duracion_seg),
    )


def _tupla_a_item(t):
    """Convierte una tupla desempaquetada en un objeto Cancion."""
    return Cancion(
        id=t[0],
        titulo=_a_texto(t[1]),
        artista=_a_texto(t[2]),
        album=_a_texto(t[3]),
        genero=_a_texto(t[4]),
        anio=t[5],
        duracion_seg=t[6],
    )


def guardar_binario(ruta, canciones):
    """Escribe el archivo completo: header (magia + tema + cantidad) + registros."""
    ruta = Path(ruta)
    lista = list(canciones)
    with ruta.open("wb") as archivo:
        archivo.write(HEADER.pack(b"AYED", TEMA, len(lista)))
        for item in lista:
            archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def cargar_binario(ruta):
    """Lee el binario con validaciones y devuelve una lista de objetos Cancion."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")

    with ruta.open("rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: ni siquiera tiene header completo.")

        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != b"AYED":
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no pertenece a este TP.")
        if tema != TEMA:
            raise ArchivoInvalidoError(f"El tema del archivo ({tema!r}) no corresponde a Música ({TEMA!r}).")

        canciones = []
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError("Binario truncado: el header indica más registros de los que hay.")
            canciones.append(_tupla_a_item(FORMATO.unpack(datos)))

    return canciones


def actualizar_registro(ruta, posicion, item):
    """Acceso directo O(1): pisa SOLO el registro en 'posicion' (0-based) sin reescribir el archivo."""
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))


def alta_binario(ruta, item):
    """Agrega un registro AL FINAL y actualiza la cantidad en el header."""
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)
        archivo.seek(0, 2)  # Final del archivo
        archivo.write(FORMATO.pack(*_item_a_tupla(item)))
        archivo.seek(0)  # Principio del archivo
        archivo.write(HEADER.pack(magia, tema, cantidad + 1))


def baja_binario(ruta, posicion):
    """Quita el registro 'posicion' y reescribe los restantes."""
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        magia, tema, cantidad = HEADER.unpack(cabecera)
        registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
        del registros[posicion]
        archivo.seek(0)
        archivo.truncate()
        archivo.write(HEADER.pack(magia, tema, len(registros)))
        for datos in registros:
            archivo.write(datos)