from src.config import TEMA
from src.dominio.biblioteca import Biblioteca

biblioteca = Biblioteca()
biblioteca.cargar_datos_iniciales()


def mostrar_menu():
    print(f"\n=== Biblioteca Musical ({TEMA.upper()}) — AyED C2 2026 ===")
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("5. Ver versiones derivadas de una canción (remix/cover)")
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
        elif opcion == "0":
            print("\n¡Gracias por usar la Biblioteca Musical! Hasta luego.")
            break
        else:
            print("\n❌ Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main()
