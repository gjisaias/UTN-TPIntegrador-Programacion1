# Trabajo Practico Integrador - Programacion 1

## Gestion de datos de paises

Este trabajo es una aplicacion de consola hecha en Python. Sirve para trabajar con informacion de paises, usando un archivo CSV como base de datos.

El programa carga los paises automaticamente cuando inicia. No hace falta cargarlos a mano antes de buscar, filtrar, ordenar o ver estadisticas.

La informacion de cada pais incluye:

- Nombre
- Poblacion
- Superficie
- Continente

## Datos del trabajo

- Institucion: UTN
- Carrera: Tecnicatura Universitaria en Programacion a Distancia
- Materia: Programacion 1
- Comision: 11 - Regional Venado Tuerto
- Fecha de entrega: 17/06/2026

## Integrantes

- Franco Kaddour
- Gonzalo Isaias

## Archivos del proyecto

- main.py: codigo fuente principal del programa.
- paises.csv: dataset base con los paises.
- README.md: descripcion del proyecto, instrucciones de uso y participacion.
- Informe_tecnico.pdf: documentacion academica y tecnica en PDF.

## Como funciona

Al iniciar, el programa lee el archivo paises.csv y guarda los datos en una lista de diccionarios.

Cada diccionario representa un pais. Por ejemplo, un pais tiene nombre, poblacion, superficie y continente.

Despues el usuario puede elegir opciones desde un menu en consola.

## Como ejecutar el programa

Se puede ejecutar desde la carpeta del proyecto con este comando:

python main.py

Tambien se puede abrir desde el editor o IDE que se use para la materia.

Importante: el archivo paises.csv tiene que estar en la misma carpeta que main.py para que el programa pueda leer los datos.

## Opciones del menu

1. Mostrar todos los paises.
2. Agregar un pais.
3. Actualizar poblacion y superficie.
4. Buscar pais por nombre.
5. Filtrar paises.
6. Ordenar paises.
7. Mostrar estadisticas.
8. Salir.

## Funcionalidades principales

El programa permite:

- Cargar datos desde un archivo CSV.
- Agregar un pais nuevo.
- Actualizar la poblacion y la superficie de un pais.
- Buscar paises por nombre o por una parte del nombre.
- Filtrar por continente.
- Filtrar por rango de poblacion.
- Filtrar por rango de superficie.
- Ordenar por nombre, poblacion o superficie.
- Calcular estadisticas basicas.

## Ejemplos de uso

Ejemplo de busqueda:

```
Seleccione una opcion: 4
Ingrese nombre o parte del nombre: arg
Argentina                45376763            2780400 America
```

Ejemplo de filtro por continente:

```
Seleccione una opcion: 5
Seleccione una opcion: 1
Continente: Europa
Espana                   47450795             505990 Europa
Alemania                 83149300             357022 Europa
Francia                  67750000             643801 Europa
Italia                   59030133             301340 Europa
```

Ejemplo de estadisticas:

```
Seleccione una opcion: 7
Pais con mayor poblacion: China (1411750000)
Pais con menor poblacion: Uruguay (3426260)
Promedio de poblacion: 220633557.30
Promedio de superficie: 3021381.95 km2
Cantidad de paises por continente:
- America: 8
- Europa: 4
- Asia: 4
- Africa: 3
- Oceania: 1
```

## Enlaces de entrega

- Repositorio GitHub: https://github.com/gjisaias/UTN-TPI-Programacion1
- Video demostrativo: https://youtu.be/EfYUKP-7b7A
- Documentacion PDF: Informe_tecnico.pdf (incluido en la raiz del repositorio)

## Participacion

- Gonzalo Isaias: desarrollo del programa en Python (carga del CSV, menu, busqueda, filtros, ordenamientos y estadisticas), pruebas de funcionamiento, correccion de errores y apoyo en la documentacion.
- Franco Kaddour: armado del dataset de paises, redaccion del README y del informe tecnico, generacion de las capturas y el diagrama de flujo, revision final y coordinacion de la entrega.
