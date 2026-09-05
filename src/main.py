from src.config import TEMA
from src.dominio.cancion import listar_catalogo

def mostrar_menu():
    print(f"\n=== Biblioteca Musical ({TEMA.upper()}) — AyED C2 2026 ===")
    print("1. Listar catálogo de canciones")
    print("0. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            listar_catalogo()
        elif opcion == "0":
            print("\n¡Gracias por usar la Biblioteca Musical! Hasta luego.")
            break
        else:
            print("\n❌ Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()