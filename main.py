# Importa el modulo csv para poder leer y escribir archivos con formato CSV.
import csv

# Importa el modulo os para trabajar con rutas de archivos y carpetas.
import os


# Guarda la ruta de la carpeta donde se encuentra este archivo main.py.
CARPETA_DEL_PROGRAMA = os.path.dirname(os.path.abspath(__file__))

# Arma la ruta completa del archivo paises.csv para poder encontrarlo siempre.
ARCHIVO_DE_PAISES = os.path.join(CARPETA_DEL_PROGRAMA, "paises.csv")

# Define las columnas que debe tener el archivo CSV.
COLUMNAS_CSV = ["nombre", "poblacion", "superficie", "continente"]


# Convierte un texto a minusculas y le quita espacios al principio y al final.
def normalizar_texto(texto):
    return texto.strip().lower()


# Lee el archivo CSV y devuelve una lista de diccionarios con los paises cargados.
def cargar_paises(nombre_archivo):
    # Crea la lista donde se van a guardar todos los paises.
    lista_paises = []

    try:
        # Abre el archivo CSV en modo lectura.
        with open(nombre_archivo, "r", encoding="utf-8", newline="") as archivo:
            # Lee el CSV usando los encabezados como claves del diccionario.
            lector_csv = csv.DictReader(archivo)

            # Controla que el archivo tenga las columnas esperadas.
            if lector_csv.fieldnames != COLUMNAS_CSV:
                print("Error: el archivo CSV no tiene las columnas esperadas.")
                print("Formato esperado: nombre,poblacion,superficie,continente")
                return lista_paises

            # Recorre cada fila del CSV, empezando a contar desde la fila 2.
            for numero_fila, fila_csv in enumerate(lector_csv, start=2):
                try:
                    # Toma el nombre del pais y le quita espacios sobrantes.
                    nombre = fila_csv["nombre"].strip()

                    # Toma el continente y le quita espacios sobrantes.
                    continente = fila_csv["continente"].strip()

                    # Convierte la poblacion a numero entero.
                    poblacion = int(fila_csv["poblacion"])

                    # Convierte la superficie a numero entero.
                    superficie = int(fila_csv["superficie"])

                    # Valida que los textos obligatorios no esten vacios.
                    if nombre == "" or continente == "":
                        raise ValueError

                    # Valida que poblacion y superficie sean numeros positivos.
                    if poblacion <= 0 or superficie <= 0:
                        raise ValueError

                    # Crea un diccionario con los datos de un pais.
                    pais = {
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente,
                    }

                    # Agrega el pais validado a la lista principal.
                    lista_paises.append(pais)
                except ValueError:
                    # Informa si una fila tiene datos incorrectos.
                    print(f"Fila {numero_fila} omitida: datos invalidos.")

    except FileNotFoundError:
        # Informa si no se encuentra el archivo CSV.
        print("No se encontro el archivo paises.csv.")
        print("El archivo debe estar en la misma carpeta que main.py.")
    except OSError:
        # Informa si ocurre otro error al intentar leer el archivo.
        print("No se pudo leer el archivo paises.csv.")

    # Devuelve la lista cargada, aunque este vacia si hubo algun error.
    return lista_paises


# Guarda la lista de paises actualizada dentro del archivo CSV.
def guardar_paises(nombre_archivo, lista_paises):
    try:
        # Abre el archivo CSV en modo escritura.
        with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
            # Crea el escritor CSV usando las columnas definidas.
            escritor_csv = csv.DictWriter(archivo, fieldnames=COLUMNAS_CSV)

            # Escribe la primera fila con los nombres de las columnas.
            escritor_csv.writeheader()

            # Escribe todos los paises de la lista en el archivo.
            escritor_csv.writerows(lista_paises)

        print("Datos guardados correctamente.")
    except OSError:
        # Informa si no se pudo guardar el archivo.
        print("Error: no se pudieron guardar los datos.")


# Pide un texto al usuario y no permite que quede vacio.
def pedir_texto_no_vacio(mensaje):
    while True:
        # Pide el dato y elimina espacios al principio y al final.
        texto_ingresado = input(mensaje).strip()

        # Si el texto no esta vacio, lo devuelve.
        if texto_ingresado != "":
            return texto_ingresado

        print("El campo no puede quedar vacio.")


# Pide un numero entero positivo y repite hasta que sea valido.
def pedir_entero_positivo(mensaje):
    while True:
        # Pide el dato como texto para poder validarlo.
        dato_ingresado = input(mensaje).strip()

        try:
            # Intenta convertir el dato ingresado a entero.
            numero = int(dato_ingresado)

            # Si el numero es positivo, lo devuelve.
            if numero > 0:
                return numero

            print("El numero debe ser mayor que cero.")
        except ValueError:
            # Informa si el dato no puede convertirse a entero.
            print("Debe ingresar un numero entero valido.")


# Pide un rango minimo y maximo para filtrar datos numericos.
def pedir_rango(nombre_dato):
    print(f"Ingrese el rango de {nombre_dato}.")

    # Solicita el valor minimo del rango.
    minimo = pedir_entero_positivo("Valor minimo: ")

    # Solicita el valor maximo del rango.
    maximo = pedir_entero_positivo("Valor maximo: ")

    # Controla que el minimo no sea mayor que el maximo.
    while minimo > maximo:
        print("El minimo no puede ser mayor que el maximo.")
        minimo = pedir_entero_positivo("Valor minimo: ")
        maximo = pedir_entero_positivo("Valor maximo: ")

    # Devuelve ambos valores para usarlos en el filtro.
    return minimo, maximo


# Muestra en pantalla una lista de paises con formato de tabla.
def mostrar_paises(lista_paises):
    # Si la lista esta vacia, informa que no hay resultados.
    if len(lista_paises) == 0:
        print("No hay paises para mostrar.")
        return

    # Imprime el encabezado de la tabla.
    print("-" * 78)
    print(f"{'Nombre':<22} {'Poblacion':>15} {'Superficie km2':>18} {'Continente':<15}")
    print("-" * 78)

    # Recorre la lista e imprime los datos de cada pais.
    for pais in lista_paises:
        print(
            f"{pais['nombre']:<22} "
            f"{pais['poblacion']:>15} "
            f"{pais['superficie']:>18} "
            f"{pais['continente']:<15}"
        )

    print("-" * 78)


# Busca paises por nombre, permitiendo coincidencia parcial o exacta.
def buscar_paises_por_nombre(lista_paises, nombre_buscado, busqueda_exacta=False):
    # Crea una lista para guardar los paises encontrados.
    paises_encontrados = []

    # Normaliza el texto buscado para comparar sin importar mayusculas.
    nombre_buscado = normalizar_texto(nombre_buscado)

    # Recorre todos los paises de la lista.
    for pais in lista_paises:
        # Normaliza el nombre del pais actual.
        nombre_del_pais = normalizar_texto(pais["nombre"])

        # Agrega el pais si coincide exactamente.
        if busqueda_exacta and nombre_del_pais == nombre_buscado:
            paises_encontrados.append(pais)

        # Agrega el pais si el texto buscado esta dentro del nombre.
        elif not busqueda_exacta and nombre_buscado in nombre_del_pais:
            paises_encontrados.append(pais)

    # Devuelve la lista de coincidencias.
    return paises_encontrados


# Verifica si ya existe un pais con el mismo nombre.
def existe_pais(lista_paises, nombre):
    return len(buscar_paises_por_nombre(lista_paises, nombre, True)) > 0


# Permite agregar un nuevo pais a la lista y al archivo CSV.
def agregar_pais(lista_paises):
    print("\nAgregar pais")

    # Pide el nombre del pais.
    nombre = pedir_texto_no_vacio("Nombre: ")

    # Evita cargar dos paises con el mismo nombre.
    if existe_pais(lista_paises, nombre):
        print("Ya existe un pais con ese nombre.")
        return

    # Pide los datos numericos y el continente.
    poblacion = pedir_entero_positivo("Poblacion: ")
    superficie = pedir_entero_positivo("Superficie en km2: ")
    continente = pedir_texto_no_vacio("Continente: ")

    # Arma el diccionario del nuevo pais.
    pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    }

    # Agrega el nuevo pais a la lista.
    lista_paises.append(pais)

    # Guarda la lista actualizada en el CSV.
    guardar_paises(ARCHIVO_DE_PAISES, lista_paises)

    print("Pais agregado correctamente.")


# Busca un pais para actualizarlo, manejando una o varias coincidencias.
def seleccionar_pais(lista_paises):
    # Pide el nombre o parte del nombre del pais.
    nombre = pedir_texto_no_vacio("Ingrese el nombre del pais: ")

    # Busca coincidencias dentro de la lista.
    coincidencias = buscar_paises_por_nombre(lista_paises, nombre)

    # Si no hay coincidencias, corta la funcion.
    if len(coincidencias) == 0:
        print("No se encontraron paises con ese nombre.")
        return None

    # Si hay una sola coincidencia, la devuelve directamente.
    if len(coincidencias) == 1:
        return coincidencias[0]

    # Si hay varias coincidencias, las muestra numeradas.
    print("Se encontraron varias coincidencias:")
    for numero, pais in enumerate(coincidencias, start=1):
        print(f"{numero}. {pais['nombre']}")

    # Pide al usuario que elija una de las coincidencias.
    while True:
        opcion = input("Seleccione un numero o 0 para cancelar: ").strip()

        try:
            # Convierte la opcion ingresada a entero.
            opcion = int(opcion)

            # Permite cancelar la seleccion.
            if opcion == 0:
                return None

            # Devuelve el pais elegido si la opcion esta dentro del rango.
            if 1 <= opcion <= len(coincidencias):
                return coincidencias[opcion - 1]

            print("Opcion fuera de rango.")
        except ValueError:
            print("Debe ingresar un numero valido.")


# Actualiza la poblacion y la superficie de un pais existente.
def actualizar_pais(lista_paises):
    print("\nActualizar pais")

    # Selecciona el pais que se quiere modificar.
    pais = seleccionar_pais(lista_paises)

    # Si no se selecciona ningun pais, vuelve al menu.
    if pais is None:
        return

    print(f"Pais seleccionado: {pais['nombre']}")

    # Reemplaza la poblacion por un nuevo valor.
    pais["poblacion"] = pedir_entero_positivo("Nueva poblacion: ")

    # Reemplaza la superficie por un nuevo valor.
    pais["superficie"] = pedir_entero_positivo("Nueva superficie en km2: ")

    # Guarda los cambios en el archivo CSV.
    guardar_paises(ARCHIVO_DE_PAISES, lista_paises)

    print("Pais actualizado correctamente.")


# Pide un nombre y muestra los paises encontrados.
def buscar_pais(lista_paises):
    print("\nBuscar pais")

    # Pide el nombre completo o parcial.
    nombre = pedir_texto_no_vacio("Ingrese nombre o parte del nombre: ")

    # Busca los paises que coinciden con el texto ingresado.
    paises_encontrados = buscar_paises_por_nombre(lista_paises, nombre)

    # Muestra los resultados.
    mostrar_paises(paises_encontrados)


# Filtra paises por continente.
def filtrar_por_continente(lista_paises):
    # Pide el continente a buscar.
    continente_buscado = pedir_texto_no_vacio("Continente: ")

    # Crea una lista para guardar los paises que coinciden.
    paises_filtrados = []

    # Recorre todos los paises y compara el continente.
    for pais in lista_paises:
        if normalizar_texto(pais["continente"]) == normalizar_texto(continente_buscado):
            paises_filtrados.append(pais)

    # Muestra los paises filtrados.
    mostrar_paises(paises_filtrados)


# Filtra paises segun un rango de poblacion o superficie.
def filtrar_por_rango(lista_paises, dato_a_filtrar, nombre_dato):
    # Pide el minimo y maximo del rango.
    minimo, maximo = pedir_rango(nombre_dato)

    # Crea una lista para guardar los paises que cumplen el rango.
    paises_filtrados = []

    # Recorre los paises y compara el dato elegido.
    for pais in lista_paises:
        if minimo <= pais[dato_a_filtrar] <= maximo:
            paises_filtrados.append(pais)

    # Muestra los resultados del filtro.
    mostrar_paises(paises_filtrados)


# Muestra el submenu de filtros y ejecuta el filtro elegido.
def filtrar_paises(lista_paises):
    print("\nFiltrar paises")
    print("1. Por continente")
    print("2. Por rango de poblacion")
    print("3. Por rango de superficie")

    # Pide la opcion de filtro.
    opcion = input("Seleccione una opcion: ").strip()

    # Ejecuta el filtro por continente.
    if opcion == "1":
        filtrar_por_continente(lista_paises)

    # Ejecuta el filtro por rango de poblacion.
    elif opcion == "2":
        filtrar_por_rango(lista_paises, "poblacion", "poblacion")

    # Ejecuta el filtro por rango de superficie.
    elif opcion == "3":
        filtrar_por_rango(lista_paises, "superficie", "superficie")

    else:
        print("Opcion invalida.")


# Ordena los paises segun el criterio elegido por el usuario.
def ordenar_paises(lista_paises):
    print("\nOrdenar paises")
    print("1. Por nombre")
    print("2. Por poblacion")
    print("3. Por superficie")

    # Pide el criterio de ordenamiento.
    opcion = input("Seleccione criterio: ").strip()

    # Define que dato se va a usar para ordenar.
    if opcion == "1":
        dato_para_ordenar = "nombre"
    elif opcion == "2":
        dato_para_ordenar = "poblacion"
    elif opcion == "3":
        dato_para_ordenar = "superficie"
    else:
        print("Opcion invalida.")
        return

    # Pregunta si el orden debe ser descendente.
    respuesta = input("Orden descendente? (s/n): ").strip().lower()

    # Convierte la respuesta en un valor booleano.
    orden_descendente = respuesta == "s"

    # Ordena la lista sin modificar el orden original.
    paises_ordenados = sorted(
        lista_paises,
        key=lambda pais: pais[dato_para_ordenar],
        reverse=orden_descendente,
    )

    # Muestra la lista ordenada.
    mostrar_paises(paises_ordenados)


# Cuenta cuantos paises hay por cada continente.
def contar_por_continente(lista_paises):
    # Crea un diccionario para acumular cantidades.
    cantidades_por_continente = {}

    # Recorre la lista de paises.
    for pais in lista_paises:
        continente = pais["continente"]

        # Si el continente ya existe, suma uno.
        if continente in cantidades_por_continente:
            cantidades_por_continente[continente] += 1

        # Si el continente no existe, lo inicia en uno.
        else:
            cantidades_por_continente[continente] = 1

    # Devuelve el diccionario con los totales.
    return cantidades_por_continente


# Calcula y muestra estadisticas generales del dataset.
def mostrar_estadisticas(lista_paises):
    # No calcula estadisticas si no hay datos cargados.
    if len(lista_paises) == 0:
        print("No hay datos para calcular estadisticas.")
        return

    # Toma el primer pais como referencia inicial.
    pais_mayor_poblacion = lista_paises[0]
    pais_menor_poblacion = lista_paises[0]

    # Inicia los acumuladores para calcular promedios.
    suma_poblacion = 0
    suma_superficie = 0

    # Recorre todos los paises para calcular indicadores.
    for pais in lista_paises:
        # Acumula poblacion y superficie.
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        # Actualiza el pais con mayor poblacion.
        if pais["poblacion"] > pais_mayor_poblacion["poblacion"]:
            pais_mayor_poblacion = pais

        # Actualiza el pais con menor poblacion.
        if pais["poblacion"] < pais_menor_poblacion["poblacion"]:
            pais_menor_poblacion = pais

    # Calcula los promedios.
    promedio_poblacion = suma_poblacion / len(lista_paises)
    promedio_superficie = suma_superficie / len(lista_paises)

    # Cuenta cuantos paises hay por continente.
    cantidades_por_continente = contar_por_continente(lista_paises)

    # Muestra los resultados.
    print("\nEstadisticas")
    print(
        f"Pais con mayor poblacion: "
        f"{pais_mayor_poblacion['nombre']} ({pais_mayor_poblacion['poblacion']})"
    )
    print(
        f"Pais con menor poblacion: "
        f"{pais_menor_poblacion['nombre']} ({pais_menor_poblacion['poblacion']})"
    )
    print(f"Promedio de poblacion: {promedio_poblacion:.2f}")
    print(f"Promedio de superficie: {promedio_superficie:.2f} km2")
    print("Cantidad de paises por continente:")

    # Muestra la cantidad de paises por cada continente.
    for continente, cantidad in cantidades_por_continente.items():
        print(f"- {continente}: {cantidad}")


# Muestra el menu principal del programa.
def mostrar_menu():
    print("\nSistema de Gestion de Datos de Paises")
    print("1. Mostrar todos los paises")
    print("2. Agregar un pais")
    print("3. Actualizar poblacion y superficie")
    print("4. Buscar pais por nombre")
    print("5. Filtrar paises")
    print("6. Ordenar paises")
    print("7. Mostrar estadisticas")
    print("8. Salir")


# Funcion principal que controla todo el programa.
def ejecutar_programa():
    # Carga los paises desde el archivo CSV al iniciar.
    lista_paises = cargar_paises(ARCHIVO_DE_PAISES)

    # Mantiene el programa funcionando hasta que el usuario elija salir.
    while True:
        # Muestra el menu en cada vuelta.
        mostrar_menu()

        # Pide la opcion elegida por el usuario.
        opcion = input("Seleccione una opcion: ").strip()

        # Ejecuta la opcion seleccionada.
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
            ordenar_paises(lista_paises)
        elif opcion == "7":
            mostrar_estadisticas(lista_paises)
        elif opcion == "8":
            print("Programa finalizado.")
            break
        else:
            print("Opcion invalida. Intente nuevamente.")


# Verifica que el archivo se este ejecutando directamente.
if __name__ == "__main__":
    # Inicia el programa.
    ejecutar_programa()
