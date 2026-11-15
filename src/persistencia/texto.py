# src/persistencia/texto.py
from pathlib import Path
from src.excepciones import ArchivoInvalidoError

# Anclamos las rutas a la raíz del proyecto
RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_TXT = DATA / "canciones.txt"
RUTA_VERSIONES = DATA / "versiones.txt"
RUTA_BIN = DATA / "canciones.bin"

ENCABEZADOS_CANCIONES = ["id", "titulo", "artista", "album", "genero", "anio", "duracion_seg"]


def cargar_texto(ruta):
    """
    Lee un .txt secuencial y devuelve una lista de dicts, uno por registro.
    Lanza ArchivoInvalidoError si el archivo no existe o tiene líneas mal formadas.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        primera_linea = archivo.readline().strip()
        if not primera_linea:
            raise ArchivoInvalidoError("El archivo está vacío o no tiene encabezado.")
        
        encabezado = [col.strip() for col in primera_linea.split(",")]
        
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue  # Ignoramos líneas vacías al final
            
            valores = [val.strip() for val in linea.split(",")]
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos (se esperaban {len(encabezado)}): {linea}"
                )
            
            fila = dict(zip(encabezado, valores))
            filas.append(fila)
            
    return filas


def guardar_texto(ruta, filas, encabezados=ENCABEZADOS_CANCIONES):
    """
    Escribe el catálogo completo en .txt: encabezado + un registro por línea.
    """
    ruta = Path(ruta)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]) for clave in encabezados]
            archivo.write(",".join(campos) + "\n")