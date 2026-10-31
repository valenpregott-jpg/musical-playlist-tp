# src/algoritmos/busqueda.py

def busqueda_lineal(coleccion, clave, obtener_clave=None):
    
    for elemento in coleccion:
        if obtener_clave is None:
            if elemento == clave:
                return elemento
        else:
            if obtener_clave(elemento) == clave:
                return elemento
    return None  # Si no lo encuentra, devuelve None


def busqueda_binaria(coleccion, clave, obtener_clave):
  
    izq = 0
    der = len(coleccion) - 1

    while izq <= der:
        medio = (izq + der) // 2
        valor = obtener_clave(coleccion[medio])

        if valor == clave:
            return coleccion[medio]  # ¡Encontrado!
        elif valor < clave:
            izq = medio + 1  # Buscamos en la mitad derecha
        else:
            der = medio - 1  # Buscamos en la mitad izquierda

    return None  # No encontrado