# ============================================================================
# ETAPA 1: CONFIGURACION E IMPORTES
# ============================================================================
# Importa modulos necesarios, establece constantes y rutas de archivos.

import csv
import os

# Ruta de la carpeta donde se encuentra el programa.
CARPETA_DEL_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Ruta completa del archivo CSV con los datos de paises.
ARCHIVO_DE_PAISES = os.path.join(CARPETA_DEL_PROGRAMA, "paises.csv")

# Columnas esperadas en el archivo CSV.
COLUMNAS_CSV = ["nombre", "poblacion", "superficie", "continente"]


# ============================================================================
# ETAPA 2: FUNCIONES DE VALIDACION DE ENTRADA
# ============================================================================
# Validan y procesan los datos ingresados por el usuario desde la consola.

def normalizar_texto(texto):
    """Convierte texto a minusculas y quita espacios al inicio/final."""
    return texto.strip().lower()


def pedir_texto_no_vacio(mensaje):
    """Pide un texto al usuario y no permite que quede vacío."""
    while True:
        texto_ingresado = input(mensaje).strip()
        if texto_ingresado != "":
            return texto_ingresado
        print("El campo no puede quedar vacio.")


def pedir_entero_positivo(mensaje):
    """Pide un numero entero positivo y repite hasta que sea valido."""
    while True:
        dato_ingresado = input(mensaje).strip()
        try:
            numero = int(dato_ingresado)
            if numero > 0:
                return numero
            print("El numero debe ser mayor que cero.")
        except ValueError:
            print("Debe ingresar un numero entero valido.")


def pedir_rango(nombre_dato):
    """Pide valores minimo y maximo para un rango de filtrado."""
    print(f"Ingrese el rango de {nombre_dato}.")
    minimo = pedir_entero_positivo("Valor minimo: ")
    maximo = pedir_entero_positivo("Valor maximo: ")

    while minimo > maximo:
        print("El minimo no puede ser mayor que el maximo.")
        minimo = pedir_entero_positivo("Valor minimo: ")
        maximo = pedir_entero_positivo("Valor maximo: ")

    return minimo, maximo


# ============================================================================
# ETAPA 3: FUNCIONES DE I/O (CARGA Y GUARDADO DE DATOS)
# ============================================================================
# Manejan la lectura y escritura del archivo CSV.

def cargar_paises(nombre_archivo):
    """Lee el archivo CSV y devuelve una lista de diccionarios con los paises."""
    lista_paises = []

    try:
        with open(nombre_archivo, "r", encoding="utf-8", newline="") as archivo:
            lector_csv = csv.DictReader(archivo)

            # Verifica que el archivo tenga las columnas esperadas.
            if lector_csv.fieldnames != COLUMNAS_CSV:
                print("Error: el archivo CSV no tiene las columnas esperadas.")
                print("Formato esperado: nombre,poblacion,superficie,continente")
                return lista_paises

            # Procesa cada fila del CSV.
            for numero_fila, fila_csv in enumerate(lector_csv, start=2):
                try:
                    nombre = fila_csv["nombre"].strip()
                    continente = fila_csv["continente"].strip()
                    poblacion = int(fila_csv["poblacion"])
                    superficie = int(fila_csv["superficie"])

                    # Valida que los textos obligatorios no esten vacios.
                    if nombre == "" or continente == "":
                        raise ValueError

                    # Valida que poblacion y superficie sean numeros positivos.
                    if poblacion <= 0 or superficie <= 0:
                        raise ValueError

                    # Crea el diccionario del pais y lo agrega a la lista.
                    pais = {
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente,
                    }
                    lista_paises.append(pais)
                except ValueError:
                    print(f"Fila {numero_fila} omitida: datos invalidos.")

    except FileNotFoundError:
        print("No se encontro el archivo paises.csv.")
        print("El archivo debe estar en la misma carpeta que main.py.")
    except OSError:
        print("No se pudo leer el archivo paises.csv.")

    return lista_paises


def guardar_paises(nombre_archivo, lista_paises):
    """Guarda la lista de paises actualizada en el archivo CSV."""
    try:
        with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
            escritor_csv = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_paises)
        print("Datos guardados correctamente.")
    except OSError:
        print("Error: no se pudieron guardar los datos.")


# ============================================================================
# ETAPA 4: FUNCIONES DE BUSQUEDA, FILTRADO Y ORDENAMIENTO
# ============================================================================
# Procesan y transforman el dataset segun criterios del usuario.

def buscar_paises_por_nombre(lista_paises, nombre_buscado, busqueda_exacta=False):
    """Busca paises por nombre (parcial o exacta)."""
    paises_encontrados = []
    nombre_buscado = normalizar_texto(nombre_buscado)

    for pais in lista_paises:
        nombre_del_pais = normalizar_texto(pais["nombre"])

        if busqueda_exacta and nombre_del_pais == nombre_buscado:
            paises_encontrados.append(pais)
        elif not busqueda_exacta and nombre_buscado in nombre_del_pais:
            paises_encontrados.append(pais)

    return paises_encontrados


def existe_pais(lista_paises, nombre):
    """Verifica si ya existe un pais con el mismo nombre."""
    return len(buscar_paises_por_nombre(lista_paises, nombre, True)) > 0


def filtrar_por_continente(lista_paises):
    """Filtra paises por continente."""
    continente_buscado = pedir_texto_no_vacio("Continente: ")
    paises_filtrados = []

    for pais in lista_paises:
        if normalizar_texto(pais["continente"]) == normalizar_texto(continente_buscado):
            paises_filtrados.append(pais)

    return paises_filtrados


def filtrar_por_rango(lista_paises, dato_a_filtrar, nombre_dato):
    """Filtra paises segun un rango de poblacion o superficie."""
    minimo, maximo = pedir_rango(nombre_dato)
    paises_filtrados = []

    for pais in lista_paises:
        if minimo <= pais[dato_a_filtrar] <= maximo:
            paises_filtrados.append(pais)

    return paises_filtrados


def ordenar_paises(lista_paises):
    """Ordena paises por nombre, poblacion o superficie (ascendente/descendente)."""
    print("\nOrdenar paises")
    print("1. Por nombre")
    print("2. Por poblacion")
    print("3. Por superficie")

    opcion = input("Seleccione criterio: ").strip()

    # Define el criterio de ordenamiento.
    if opcion == "1":
        dato_para_ordenar = "nombre"
    elif opcion == "2":
        dato_para_ordenar = "poblacion"
    elif opcion == "3":
        dato_para_ordenar = "superficie"
    else:
        print("Opcion invalida.")
        return None

    # Pregunta si el orden debe ser descendente.
    respuesta = input("Orden descendente? (s/n): ").strip().lower()
    orden_descendente = respuesta == "s"

    # Ordena la lista sin modificar la original.
    paises_ordenados = sorted(
        lista_paises,
        key=lambda pais: pais[dato_para_ordenar],
        reverse=orden_descendente,
    )

    return paises_ordenados


# ============================================================================
# ETAPA 5: FUNCIONES DE ANÁLISIS
# ============================================================================
# Calculan indicadores y estadísticas a partir del dataset.

def contar_por_continente(lista_paises):
    """Cuenta cuantos paises hay en cada continente."""
    cantidades_por_continente = {}

    for pais in lista_paises:
        continente = pais["continente"]
        if continente in cantidades_por_continente:
            cantidades_por_continente[continente] += 1
        else:
            cantidades_por_continente[continente] = 1

    return cantidades_por_continente


def calcular_estadisticas(lista_paises):
    """Calcula estadisticas generales del dataset."""
    if len(lista_paises) == 0:
        return None

    # Encontrar paises con mayor y menor poblacion.
    pais_mayor_poblacion = lista_paises[0]
    pais_menor_poblacion = lista_paises[0]
    suma_poblacion = 0
    suma_superficie = 0

    for pais in lista_paises:
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        if pais["poblacion"] > pais_mayor_poblacion["poblacion"]:
            pais_mayor_poblacion = pais

        if pais["poblacion"] < pais_menor_poblacion["poblacion"]:
            pais_menor_poblacion = pais

    # Calcular promedios.
    promedio_poblacion = suma_poblacion / len(lista_paises)
    promedio_superficie = suma_superficie / len(lista_paises)

    # Agrupar en un diccionario de resultados.
    estadisticas = {
        "pais_mayor_poblacion": pais_mayor_poblacion,
        "pais_menor_poblacion": pais_menor_poblacion,
        "promedio_poblacion": promedio_poblacion,
        "promedio_superficie": promedio_superficie,
        "cantidades_por_continente": contar_por_continente(lista_paises),
    }

    return estadisticas


# ============================================================================
# ETAPA 6: FUNCIONES DE PRESENTACIÓN
# ============================================================================
# Muestran datos en la consola con formato legible.

def mostrar_paises(lista_paises):
    """Muestra una lista de paises en formato de tabla."""
    if len(lista_paises) == 0:
        print("No hay paises para mostrar.")
        return

    # Imprime el encabezado de la tabla.
    print("-" * 78)
    print(f"{'Nombre':<22} {'Poblacion':>15} {'Superficie km2':>18} {'Continente':<15}")
    print("-" * 78)

    # Imprime cada pais.
    for pais in lista_paises:
        print(
            f"{pais['nombre']:<22} "
            f"{pais['poblacion']:>15} "
            f"{pais['superficie']:>18} "
            f"{pais['continente']:<15}"
        )

    print("-" * 78)


def mostrar_estadisticas(lista_paises):
    """Calcula y muestra estadisticas generales del dataset."""
    if len(lista_paises) == 0:
        print("No hay datos para calcular estadisticas.")
        return

    estadisticas = calcular_estadisticas(lista_paises)

    # Muestra los resultados.
    print("\nEstadisticas")
    print(
        f"Pais con mayor poblacion: "
        f"{estadisticas['pais_mayor_poblacion']['nombre']} "
        f"({estadisticas['pais_mayor_poblacion']['poblacion']})"
    )
    print(
        f"Pais con menor poblacion: "
        f"{estadisticas['pais_menor_poblacion']['nombre']} "
        f"({estadisticas['pais_menor_poblacion']['poblacion']})"
    )
    print(f"Promedio de poblacion: {estadisticas['promedio_poblacion']:.2f}")
    print(f"Promedio de superficie: {estadisticas['promedio_superficie']:.2f} km2")
    print("Cantidad de paises por continente:")

    for continente, cantidad in estadisticas['cantidades_por_continente'].items():
        print(f"- {continente}: {cantidad}")


def mostrar_menu():
    """Muestra el menu principal del programa."""
    print("\nSistema de Gestion de Datos de Paises")
    print("1. Mostrar todos los paises")
    print("2. Agregar un pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. Salir")


# ============================================================================
# ETAPA 7: FUNCIONES DEL MENU (LOGICA DE FLUJO)
# ============================================================================
# Coordinan las operaciones de alto nivel solicitadas por el usuario.

def seleccionar_pais(lista_paises):
    """Busca un pais para actualizarlo, manejando coincidencias."""
    nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ")
    coincidencias = buscar_paises_por_nombre(lista_paises, nombre)

    if len(coincidencias) == 0:
        print("No se encontraron paises con ese nombre.")
        return None

    if len(coincidencias) == 1:
        return coincidencias[0]

    # Si hay multiples coincidencias, muestra opciones.
    print("Se encontraron varias coincidencias:")
    for numero, pais in enumerate(coincidencias, start=1):
        print(f"{numero}. {pais['nombre']}")

    while True:
        opcion = input("Seleccione un numero o 0 para cancelar: ").strip()
        try:
            opcion = int(opcion)
            if opcion == 0:
                return None
            if 1 <= opcion <= len(coincidencias):
                return coincidencias[opcion - 1]
            print("Opcion fuera de rango.")
        except ValueError:
            print("Debe ingresar un numero valido.")


def agregar_pais(lista_paises):
    """Permite agregar un nuevo pais a la lista y al archivo CSV."""
    print("\nAgregar pais")

    nombre = pedir_texto_no_vacio("Nombre: ")

    # Evita cargar dos paises con el mismo nombre.
    if existe_pais(lista_paises, nombre):
        print("Ya existe un pais con ese nombre.")
        return

    poblacion = pedir_entero_positivo("Poblacion: ")
    superficie = pedir_entero_positivo("Superficie en km2: ")
    continente = pedir_texto_no_vacio("Continente: ")

    # Crea el diccionario del pais.
    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }

    lista_paises.append(pais)
    guardar_paises(ARCHIVO_DE_PAISES, lista_paises)
    print("Pais agregado correctamente.")


def actualizar_pais(lista_paises):
    """Actualiza la poblacion y superficie de un pais existente."""
    print("\nActualizar pais")

    pais = seleccionar_pais(lista_paises)

    if pais is None:
        return

    print(f"Pais seleccionado: {pais['nombre']}")

    pais["poblacion"] = pedir_entero_positivo("Nueva poblacion: ")
    pais["superficie"] = pedir_entero_positivo("Nueva superficie en km2: ")

    guardar_paises(ARCHIVO_DE_PAISES, lista_paises)
    print("Pais actualizado correctamente.")


def buscar_pais(lista_paises):
    """Busca y muestra paises por nombre."""
    print("\nBuscar pais")

    nombre = pedir_texto_no_vacio("Ingrese nombre o parte del nombre: ")
    paises_encontrados = buscar_paises_por_nombre(lista_paises, nombre)

    mostrar_paises(paises_encontrados)


def filtrar_paises(lista_paises):
    """Muestra un submenu de filtros y ejecuta el elegido."""
    print("\nFiltrar paises")
    print("1. Por continente")
    print("2. Por rango de poblacion")
    print("3. Por rango de superficie")

    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        paises_filtrados = filtrar_por_continente(lista_paises)
    elif opcion == "2":
        paises_filtrados = filtrar_por_rango(lista_paises, "poblacion", "poblacion")
    elif opcion == "3":
        paises_filtrados = filtrar_por_rango(lista_paises, "superficie", "superficie")
    else:
        print("Opcion invalida.")
        return

    mostrar_paises(paises_filtrados)


# ============================================================================
# ETAPA 8: FUNCION PRINCIPAL Y EJECUCION
# ============================================================================
# Punto de entrada del programa; controla el bucle principal.

def ejecutar_programa():
    """Funcion principal que controla todo el programa."""
    lista_paises = cargar_paises(ARCHIVO_DE_PAISES)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            mostrar_paises(lista_paises)
        elif opcion == "2":
            agregar_pais(lista_paises)
        elif opcion == "3":
            actualizar_pais(lista_paises)
        elif opcion == "4":
            buscar_pais(lista_paises)
        elif opcion == "5":
            filtrar_paises(lista_paises)
        elif opcion == "6":
            paises_ordenados = ordenar_paises(lista_paises)
            if paises_ordenados is not None:
                mostrar_paises(paises_ordenados)
        elif opcion == "7":
            mostrar_estadisticas(lista_paises)
        elif opcion == "8":
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida. Intente nuevamente.")


# Verifica que el archivo se este ejecutando directamente.
if __name__ == "__main__":
    ejecutar_programa()
