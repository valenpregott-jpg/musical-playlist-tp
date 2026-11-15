from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion

from src.config import TEMA
from src.dominio.biblioteca import Biblioteca
from src.dominio.cancion import Cancion
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import (
    ColeccionLlenaError,
    PilaVaciaError,
    ColaVaciaError,
    ArchivoInvalidoError,
)
from src.persistencia.texto import (
    RUTA_TXT,
    RUTA_VERSIONES,
    RUTA_BIN,
    ENCABEZADOS_CANCIONES,
    cargar_texto,
    guardar_texto,
)
from src.persistencia.binario import (
    guardar_binario,
    cargar_binario,
    actualizar_registro,
    alta_binario,
    baja_binario,
)

biblioteca = Biblioteca()
try:
    filas_c = cargar_texto(RUTA_TXT)
    filas_v = cargar_texto(RUTA_VERSIONES) if RUTA_VERSIONES.exists() else None
    biblioteca.cargar_desde_filas(filas_c, filas_v)
except ArchivoInvalidoError:
    biblioteca.cargar_datos_iniciales()

# --- INSTANCIAS E3 ---
playlist = Playlist(tope=6)
historial = Pila()
cola_reproduccion = Cola()


def guardar_todo():
    """Mantiene sincronizados los archivos .txt y .bin con la memoria."""
    guardar_texto(RUTA_TXT, biblioteca.a_filas_dict(), ENCABEZADOS_CANCIONES)
    guardar_binario(RUTA_BIN, biblioteca.listar())


def mostrar_menu():
    print(f"\n=== Biblioteca Musical ({TEMA.upper()}) — AyED C2 2026 ===")
    print("1. Listar catálogo de canciones")
    print("2. Ver detalle de una canción")
    print("3. Buscar canción (Lineal / Binaria)")
    print("4. Ordenar catálogo (Selección / Inserción)")
    print("5. Ver versiones derivadas de una canción (remix/cover)")
    print("6. ABM Catálogo (Alta / Baja / Modificación persistente)")
    print("7. Gestionar Playlist (Colección con tope)")
    print("8. Encolar y Reproducir siguiente (Cola FIFO)")
    print("9. Archivos (.txt / .bin) y Deshacer (Pila LIFO)")
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
    for cancion in biblioteca:
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
        if version:
            print(f"  {version.linea_corta()}  [{tipo}]")


def gestionar_abm():
    print("\n--- ABM PERSISTENTE DEL CATÁLOGO ---")
    print("a) Alta de nueva canción")
    print("b) Modificar canción existente (acceso directo seek en .bin)")
    print("c) Baja de canción")
    sub = input("Seleccione opción (a/b/c): ").strip().lower()

    if not RUTA_BIN.exists():
        guardar_binario(RUTA_BIN, biblioteca.listar())

    if sub == "a":
        nuevo_id = pedir_id("Nuevo ID: ")
        if nuevo_id is None:
            return
        if biblioteca.buscar_por_id(nuevo_id) is not None:
            print("❌ Ya existe una canción con ese ID.")
            return
        titulo = input("Título: ").strip()
        artista = input("Artista: ").strip()
        album = input("Álbum: ").strip()
        genero = input("Género: ").strip()
        anio = pedir_id("Año: ")
        duracion = pedir_id("Duración (segundos): ")
        if anio is None or duracion is None:
            return

        nueva = Cancion(nuevo_id, titulo, artista, album, genero, anio, duracion)
        biblioteca.agregar_cancion(nueva)
        alta_binario(RUTA_BIN, nueva)
        guardar_texto(RUTA_TXT, biblioteca.a_filas_dict(), ENCABEZADOS_CANCIONES)
        historial.apilar(f"Alta de '{titulo}' (id {nuevo_id})")
        print(f"✅ Canción '{titulo}' dada de alta y guardada en disco.")

    elif sub == "b":
        id_mod = pedir_id("ID de la canción a modificar: ")
        if id_mod is None:
            return
        pos = biblioteca.posicion_de(id_mod)
        if pos is None:
            print(f"❌ No existe canción con id {id_mod}.")
            return
        actual = biblioteca.buscar_por_id(id_mod)
        print(f"Modificando: {actual.linea_corta()} (Enter para dejar igual)")
        titulo = input(f"Nuevo título [{actual.titulo}]: ").strip() or actual.titulo
        artista = input(f"Nuevo artista [{actual.artista}]: ").strip() or actual.artista
        album = input(f"Nuevo álbum [{actual.album}]: ").strip() or actual.album
        genero = input(f"Nuevo género [{actual.genero}]: ").strip() or actual.genero
        anio_txt = input(f"Nuevo año [{actual.anio}]: ").strip()
        anio = int(anio_txt) if anio_txt.isdigit() else actual.anio
        dur_txt = input(f"Nueva duración [{actual.duracion_seg}]: ").strip()
        duracion = int(dur_txt) if dur_txt.isdigit() else actual.duracion_seg

        actual.titulo = titulo
        actual.artista = artista
        actual.album = album
        actual.genero = genero
        actual.anio = anio
        actual.duracion_seg = duracion

        actualizar_registro(RUTA_BIN, pos, actual)
        guardar_texto(RUTA_TXT, biblioteca.a_filas_dict(), ENCABEZADOS_CANCIONES)
        historial.apilar(f"Modificación de id {id_mod}")
        print(f"✅ Registro en posición {pos} actualizado con acceso directo (seek) y guardado en .txt.")

    elif sub == "c":
        id_baja = pedir_id("ID de la canción a eliminar: ")
        if id_baja is None:
            return
        pos = biblioteca.posicion_de(id_baja)
        if pos is None:
            print(f"❌ No existe canción con id {id_baja}.")
            return
        if biblioteca.cantidad() <= 1:
            print("❌ No se puede dejar el catálogo vacío.")
            return
        eliminada = biblioteca.buscar_por_id(id_baja)
        biblioteca.eliminar_en_posicion(pos)
        baja_binario(RUTA_BIN, pos)
        guardar_texto(RUTA_TXT, biblioteca.a_filas_dict(), ENCABEZADOS_CANCIONES)
        historial.apilar(f"Baja de '{eliminada.titulo}' (id {id_baja})")
        print(f"✅ Canción '{eliminada.titulo}' eliminada de memoria, .bin y .txt.")
    else:
        print("❌ Subopción inválida.")


def main():
    catalogo_ordenado = False
    criterio_orden_actual = None

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_catalogo()

        elif opcion == "2":
            ver_detalle()

        elif opcion == "3":
            print("\n--- BÚSQUEDA EN EL CATÁLOGO ---")
            print("1. Búsqueda Lineal (por Título)")
            print("2. Búsqueda Binaria (por Título)")
            sub_opcion = input("Seleccione tipo de búsqueda (1/2): ").strip()
            lista_actual = biblioteca.listar()

            if sub_opcion == "1":
                titulo_buscar = input("Ingrese el título de la canción a buscar: ").strip()
                resultado = busqueda_lineal(lista_actual, titulo_buscar, obtener_clave=lambda c: c.titulo)
                if resultado:
                    print(f"\n✅ ¡Canción encontrada!: {resultado.linea_corta()}")
                else:
                    print(f"\nNo se encontró ninguna canción con el título '{titulo_buscar}'.")

            elif sub_opcion == "2":
                if not catalogo_ordenado or criterio_orden_actual != "titulo":
                    print("\n[AVISO] El catálogo no está ordenado por Título.")
                    print("Ordenando automáticamente por Título (Inserción) para ejecutar búsqueda binaria...")
                    lista_actual = ordenar_insercion(lista_actual, obtener_clave=lambda c: c.titulo)
                    biblioteca.reemplazar_canciones(lista_actual)
                    catalogo_ordenado = True
                    criterio_orden_actual = "titulo"
                    guardar_todo()

                titulo_buscar = input("Ingrese el título de la canción a buscar: ").strip()
                resultado = busqueda_binaria(lista_actual, titulo_buscar, obtener_clave=lambda c: c.titulo)
                if resultado:
                    print(f"\n✅ ¡Canción encontrada (Búsqueda Binaria)!: {resultado.linea_corta()}")
                else:
                    print(f"\nNo se encontró ninguna canción con el título '{titulo_buscar}'.")
            else:
                print("❌ Opción no válida.")

        elif opcion == "4":
            print("\n--- ORDENAR CATÁLOGO ---")
            print("1. Por Título  |  2. Por Artista")
            criterio_sel = input("Seleccione el criterio (1/2): ").strip()
            if criterio_sel == "1":
                obtener_clave = lambda c: c.titulo
                criterio_nombre = "titulo"
            elif criterio_sel == "2":
                obtener_clave = lambda c: c.artista
                criterio_nombre = "artista"
            else:
                print("❌ Criterio inválido.")
                continue

            print("1. Selección  |  2. Inserción")
            algo_sel = input("Seleccione algoritmo (1/2): ").strip()
            lista_actual = biblioteca.listar()

            if algo_sel == "1":
                lista_actual = ordenar_seleccion(lista_actual, obtener_clave)
            elif algo_sel == "2":
                lista_actual = ordenar_insercion(lista_actual, obtener_clave)
            else:
                print("❌ Algoritmo inválido.")
                continue

            biblioteca.reemplazar_canciones(lista_actual)
            catalogo_ordenado = True
            criterio_orden_actual = criterio_nombre
            guardar_todo()
            print(f"✅ Catálogo ordenado por {criterio_nombre} y guardado en archivos.")

        elif opcion == "5":
            ver_versiones_derivadas()

        elif opcion == "6":
            gestionar_abm()

        elif opcion == "7":
            print("\n--- PLAYLIST (Tope 6) ---")
            print("a) Agregar canción a Playlist  |  b) Ver Playlist")
            sub = input("Subopción (a/b): ").strip().lower()
            if sub == "a":
                id_cancion = pedir_id("Id de la canción a agregar: ")
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
            elif sub == "b":
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
            print("\n--- PERSISTENCIA Y DESHACER ---")
            print("a) Cargar catálogo desde .txt")
            print("b) Guardar catálogo en .txt")
            print("c) Guardar catálogo en binario (.bin)")
            print("d) Cargar catálogo desde binario (.bin)")
            print("e) Probar carga de archivo inválido (prueba ArchivoInvalidoError)")
            print("f) Deshacer última acción (Pila LIFO)")
            sub = input("Subopción > ").strip().lower()
            try:
                if sub == "a":
                    filas_c = cargar_texto(RUTA_TXT)
                    filas_v = cargar_texto(RUTA_VERSIONES) if RUTA_VERSIONES.exists() else None
                    biblioteca.cargar_desde_filas(filas_c, filas_v)
                    catalogo_ordenado = False
                    print(f"✅ Catálogo cargado desde .txt: {biblioteca.cantidad()} canciones.")
                elif sub == "b":
                    guardar_texto(RUTA_TXT, biblioteca.a_filas_dict(), ENCABEZADOS_CANCIONES)
                    print("✅ Catálogo guardado en data/canciones.txt.")
                elif sub == "c":
                    guardar_binario(RUTA_BIN, biblioteca.listar())
                    print("✅ Catálogo guardado en data/canciones.bin.")
                elif sub == "d":
                    canciones_bin = cargar_binario(RUTA_BIN)
                    biblioteca.reemplazar_canciones(canciones_bin)
                    catalogo_ordenado = False
                    print(f"✅ Catálogo cargado desde .bin: {biblioteca.cantidad()} canciones.")
                elif sub == "e":
                    ruta_test = input("Nombre de archivo en data/ a probar (ej: basura.bin): ").strip()
                    cargar_binario(RUTA_BIN.parent / ruta_test)
                elif sub == "f":
                    try:
                        accion = historial.desapilar()
                        print(f"↩️ Deshacer: {accion}")
                    except PilaVaciaError as e:
                        print(f"❌ Error: {e}")
                else:
                    print("❌ Subopción inválida.")
            except ArchivoInvalidoError as error:
                print(f"❌ Archivo inválido: {error}")

        elif opcion == "0":
            print("\n¡Gracias por usar la Biblioteca Musical! Hasta luego.")
            break
        else:
            print("\n❌ Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    main()



