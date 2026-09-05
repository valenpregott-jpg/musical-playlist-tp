CATALOGO = [
    {
        "id": 1,
        "titulo": "Hola Remix",
        "artista": "Dalex, Rauw Alejandro, Lenny Tavarez, Chencho Corleone",
        "album": "Climaxxx",
        "duracion_seg": 288
    },
    {
        "id": 2,
        "titulo": "China",
        "artista": "Anuel AA, Daddy Yankee, Karol G, Ozuna, J Balvin",
        "album": "Emmanuel",
        "duracion_seg": 301
    },
    {
        "id": 3,
        "titulo": "La Canción",
        "artista": "J Balvin, Bad Bunny",
        "album": "OASIS",
        "duracion_seg": 242
    },
    {
        "id": 4,
        "titulo": "512",
        "artista": "Mora, Jhay Cortez",
        "album": "MicroDosis",
        "duracion_seg": 193
    },
    {
        "id": 5,
        "titulo": "911 Remix",
        "artista": "Sech, Jhay Cortez",
        "album": "42",
        "duracion_seg": 215
    }
]

def obtener_catalogo():
    return CATALOGO

def formatear_duracion(segundos):
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos}m {seg:02d}s"

def listar_catalogo():
    print("\n" + "=" * 60)
    print("         🎵 BIBLIOTECA MUSICAL - CATÁLOGO 🎵")
    print("=" * 60)
    for cancion in CATALOGO:
        duracion = formatear_duracion(cancion['duracion_seg'])
        print(f"[{cancion['id']:>2}] {cancion['titulo']} - {cancion['artista']}")
        print(f"     Álbum: {cancion['album']} | Duración: {duracion}")
        print("-" * 60)