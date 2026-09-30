from src.config import TEMA
from src.dominio.biblioteca import Biblioteca

# --- NUEVOS IMPORTS E3 ---
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import ColeccionLlenaError, PilaVaciaError, ColaVaciaError

biblioteca = Biblioteca()
biblioteca.cargar_datos_iniciales()

# --- INSTANCIAS E3 ---
playlist = Playlist(tope=6)
historial = Pila()
cola_reproduccion = Cola()


def mostrar_menu():
    print(f"\n=== Biblioteca Musical ({TEMA.upper()}) — AyED C2 2026 ===")
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("5. Ver versiones derivadas de una canción (remix/cover)")
    # --- NUEVAS OPCIONES E3 ---
    print("6. Agregar a la Playlist (Colección con tope)")
    print("7. Listar Playlist")
    print("8. Encolar y Reproducir siguiente (Cola FIFO)")
    print("9. Deshacer última acción (Pila LIFO)")
    print("0. Salir")


def pedir_id(mensaje):
    """Pide un id por teclado. Devuelve None si no se escribió un número."""
    texto = input(mensaje).strip()
    if not texto.lstrip("-").isdigit():
        print("\n❌ Tenés que escribir un número.")
        return None
    return int(texto)


def listar_catalogo():
    print("\n" + "=" * 60)
    print("         🎵 BIBLIOTECA MUSICAL - CATÁLOGO 🎵")
    print("=" * 60)
    for cancion in biblioteca.listar():
        print(cancion.linea_corta())
        print(cancion.detalle())
        print("-" * 60)


def ver_detalle():
    id_cancion = pedir_id("\nId de la canción: ")
    if id_cancion is None:
        return
    cancion = biblioteca.buscar_por_id(id_cancion)
    if cancion is None:
        print(f"\n❌ No existe una canción con id {id_cancion}.")
        return
    print()
    print(cancion.linea_corta())
    print(cancion.detalle())
    tipo = biblioteca.tipo_de_version(cancion.id)
    if tipo is not None:
        print(f"     (es una versión {tipo} de otra canción)")


def ver_versiones_derivadas():
    id_cancion = pedir_id("\nId de la canción base: ")
    if id_cancion is None:
        return
    cancion = biblioteca.buscar_por_id(id_cancion)
    if cancion is None:
        print(f"\n❌ No existe una canción con id {id_cancion}.")
        return

    ids_derivados = biblioteca.versiones_de(cancion.id)
    print(f"\nVersiones derivadas de «{cancion.titulo}»:")
    if not ids_derivados:
        print("  (ninguna: esta canción no tiene versiones)")
        return
    for id_version in ids_derivados:
        version = biblioteca.buscar_por_id(id_version)
        tipo = biblioteca.tipo_de_version(id_version)
        print(f"  {version.linea_corta()}  [{tipo}]")


def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_catalogo()
        elif opcion == "2":
            ver_detalle()
        elif opcion == "5":
            ver_versiones_derivadas()
            
        # --- LÓGICA E3 ---
        elif opcion == "6":
            id_cancion = pedir_id("\nId de la canción a agregar: ")
            if id_cancion is not None:
                cancion = biblioteca.buscar_por_id(id_cancion)
                if cancion:
                    try:
                        playlist.agregar(cancion.titulo)
                        historial.apilar(f"Se agregó '{cancion.titulo}' a la playlist")
                        print(f"✅ Agregada a la Playlist: {cancion.titulo}")
                    except ColeccionLlenaError as e:
                        print(f"❌ Error: {e}")
                else:
                    print(f"❌ No existe una canción con id {id_cancion}.")
                    
        elif opcion == "7":
            print("\n--- Mi Playlist ---")
            if playlist.esta_vacia():
                print("La playlist está vacía.")
            else:
                for tema in playlist:
                    print(f" 🎵 {tema}")
                    
        elif opcion == "8":
            id_cancion = pedir_id("\nId de la canción para encolar: ")
            if id_cancion is not None:
                cancion = biblioteca.buscar_por_id(id_cancion)
                if cancion:
                    cola_reproduccion.encolar(cancion.titulo)
                    print(f"✅ Encolada en la fila: {cancion.titulo}")
                    try:
                        tema = cola_reproduccion.desencolar()
                        historial.apilar(f"Se reprodujo '{tema}' desde la cola")
                        print(f"▶️ Reproduciendo turno de cola: {tema}")
                    except ColaVaciaError as e:
                        print(f"❌ Error: {e}")
                else:
                    print(f"❌ No existe una canción con id {id_cancion}.")
                    
        elif opcion == "9":
            try:
                accion = historial.desapilar()
                print(f"↩️ Deshacer: {accion}")
            except PilaVaciaError as e:
                print(f"❌ Error: {e}")
                
        elif opcion == "0":
            print("\n¡Gracias por usar la Biblioteca Musical! Hasta luego.")
            break
        else:
            print("\n❌ Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()