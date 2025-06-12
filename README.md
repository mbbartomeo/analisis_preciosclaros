# analisis_preciosclaros

## OBJETIVO
Proyecto personal exploratorio

## FASE 1: RECOLECCIÓN DE DATOS
### Origen
Precios Claros - Base SEPA
SEPA (Sistema Electrónico de Publicidad de Precios Argentinos) reúne los precios de comercios minoristas (grandes establecimientos) de más de 70 mil productos en todo el país, lo que de forma agregada genera una base diaria de aproximadamente 12 millones de registros. 
Temas: Ecomomía y Finanzas
Licencia: Creative Commons Attribution 4.0
Página de referencia: https://datos.produccion.gob.ar/dataset/sepa-precios
Fuente primaria: SEPA

## FASE 2: MANIPULACIÓN DE DATOS
### Estructura Original
Los archivos descargados se organizan de la siguiente manera:
• Una carpeta por cada día de la semana (Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo).
• Dentro de c/u, se encuentra otra carpeta con la última fecha registrada.
• Dentro hay entre 85 y 87 archivos .csv donde se encuentran por separado comercios, sucursales y productos. Presentando un total de 547 archivos.
• Cada archivo comercio.csv se corresponde a un único comercio, al igual que los sucursales.csv y los productos.csv, responden a un mismo comercio.

### PREPARACIÓN DE DATOS EN PYTHON
Se requiere unificación de los datos antes de pasar a la etapa de limpieza.
• Los archivos no pueden coexistir en una misma carpeta por su formato original ya que tienen el mismo nombre.

Se define una función utilizando Python para automatizar la copia de los archivos en otra carpeta reemplazando cada nombre y así facilitar su próxima unificación por carpeta en Power BI.

import os
import shutil

origen_base = 'D:/Archivos/1. datasets/Precios Claros - Base SEPA'
destino_base = 'D:/Archivos/1. datasets/Precios Claros - Base SEPA/00_ArchivosRenombradosUnificados'

os.makedirs(destino_base, exist_ok=True)

def copiar_y_renombrar(origen, destino):
    for carpeta_dia in os.listdir(origen):
        ruta_dia = os.path.join(origen, carpeta_dia)
        if os.path.isdir(ruta_dia):
            for carpeta_negocio in os.listdir(ruta_dia):
                ruta_negocio = os.path.join(ruta_dia, carpeta_negocio)
                if os.path.isdir(ruta_negocio):
                    for archivo in os.listdir(ruta_negocio):
                        if archivo.endswith('.csv'):
                            ruta_original = os.path.join(ruta_negocio, archivo)
                            nuevo_nombre = f"{carpeta_dia}_{carpeta_negocio}_{archivo}"
                            ruta_destino = os.path.join(destino, nuevo_nombre)
                            shutil.copy2(ruta_original, ruta_destino)
                            print(f"Copiado: {ruta_original} → {ruta_destino}")

copiar_y_renombrar(origen_base, destino_base)

### TRANSFORACIÓN DE DATOS EN POWER BI
Se inicia con una tabla de 9 columas y 658 filas.

• Se quitan filas con valores "null" y null, 
• Se eliminan columnas Source.Name, comercio_ultima_actualizacion, comercio_version_sepa,
• Se normalizan los valores de las columnas comercio_razon_social, comercio_bandera_nombre, comercio_bandera_url

Se finaliza con una tabla de 6 columnas y 44 filas.
