# 🛰️ Proyecto: Análisis de Precios Claros

## 📌 Objetivo
Análisis exploratorio autodidacta del dataset *Precios Claros - Base SEPA*, con el fin de practicar recolección, limpieza, transformación y visualización de datos a gran escala, utilizando herramientas como Python y Power BI.

---

## 📦 Fase 1: Recolección de Datos

### 🔍 Fuente
- **Nombre:** Precios Claros - Base SEPA  
- **Institución:** Secretaría de Comercio Interior (Argentina)  
- **Descripción:** Sistema Electrónico de Publicidad de Precios Argentinos. Reúne información diaria de más de 70.000 productos en grandes comercios del país.  
- **Frecuencia:** Diaria  
- **Volumen estimado:** ~12 millones de registros por día  
- **Licencia:** [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)  
- **Acceso al dataset:** [Portal de Datos Abiertos](https://datos.produccion.gob.ar/dataset/sepa-precios)

---

## 🛠️ Fase 2: Manipulación y Preparación de Datos

### 📂 Estructura de Archivos Originales
- Los archivos están organizados por día de la semana.
- Dentro de cada día, hay una carpeta con la fecha específica.
- Cada carpeta contiene entre 85 y 87 archivos `.csv`, organizados por tipo de entidad:
  - `comercios.csv`
  - `sucursales.csv`
  - `productos.csv`
- Cada conjunto pertenece a un comercio distinto, pero repiten nombre, lo cual impide su manipulación directa en conjunto.

---

### 🧮 Automatización con Python: Renombrado y Unificación

Para facilitar el posterior análisis, se desarrolló un script en Python que copia y renombra todos los archivos agregando prefijos con el día y la fecha, evitando colisiones por nombres duplicados:

```python
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
```
### 🔄 Transformación en Power BI

Una vez unificados los archivos `.csv` renombrados, se cargan en Power BI para iniciar el proceso de limpieza y transformación.

### 🗒️ TABLA COMERCIOS
#### 🧹 Tabla consolidada inicial: 
- **Filas:** 658  
- **Columnas:** 9

#### 🔧 Transformaciones aplicadas:
- Eliminación de filas con valores `null` o el string `"null"`.
- Eliminación de columnas innecesarias para el análisis:
  - `Source.Name`
  - `comercio_ultima_actualizacion`
  - `comercio_version_sepa`
  - `comercio_bandera_url`
  - `comercio_cuit`
- Normalización de texto:
  - Corrección de formato de valores en `comercio_razon_social`, `comercio_bandera_nombre`.

#### ✅ Resultado final: 
- **Filas:** 44  
- **Columnas:** 4

### 🗒️ TABLA SUCURSALES
#### 🧹 Tabla consolidada inicial: 
- **Filas:** 20619  
- **Columnas:** 22

#### 🔧 Transformaciones aplicadas:
- Eliminación de filas con valores `null` o el string `"null"`.
- Eliminación de columnas innecesarias para el análisis:
  - `Source.Name`
  - `sucursales_domingo_horario_atencion`
  - `sucursales_lunes_horario_atencion`
  - `sucursales_martes_horario_atencion`
  - `sucursales_miercoles_horario_atencion` 
  - `sucursales_jueves_horario_atencion`
  - `sucursales_viernes_horario_atencion` 
  - `sucursales_sabado_horario_atencion`
  - `sucursales_nombre`
- Normalización de valores con notación científica:
  - `sucursal_lat`
  - `sucursal_long`
- Normalización de texto:
  - Corrección de formato de valores en `sucursales_tipo`, `sucursales_localidad`
- Reemplazo de valores: 
  - `sucursales_provincia`

#### ✅ Resultado final: 
- **Filas:** 20259  
- **Columnas:** 8

### 🗒️ TABLA PRODUCTOS
#### 🧹 Datos iniciales: 
- **Filas:** +80 millones 
- **Columnas:** 17

Los archivos csv presentan un peso aproximado de 8GB, no son fácilmente tratables, presentan errores en la carga y precisan un tratamiento robusto para obtener buenos resultados.

#### 🔧 Tratamiento inicial:
- Separación manual de archivos por lotes para tratamiento idividual
- Se utiliza Google Colab + Python + Google Drive para identificar y unificar archivos csv con la cantidad de columnas correctas.
```python
# Dar acceso a Drive
from google.colab import drive
drive.mount('/content/drive')

# Importar las bibliotecas necesarias
import pandas as pd
import os

# Definir la ruta de la carpeta en Google Drive que contiene los CSV del lote
ruta_lote = '/content/drive/MyDrive/Productos/1.lote_lunes_01/'
archivos = os.listdir(ruta_lote) # Listar los archivos en la carpeta

# Definir cuántas columnas debe tener un archivo CSV válido
columnas_esperadas = 17

# Crear dos DataFrame vacíos
df_unificado = pd.DataFrame() # df para archivos correctos
df_errores = pd.DataFrame() # df para archivos con errores

# Iterar sobre cada archivo .csv en la carpeta
for archivo in archivos:
  if archivo.endswith('.csv'):
    ruta_completa = os.path.join(ruta_lote,archivo) # Obtiene ruta completa al archivo
    try:
      # Se lee el csv forzando que todas las columnas sean tratadas como texto
      df = pd.read_csv(
          ruta_completa,
          encoding='utf-8',
          sep='|',
          low_memory=False,
          dtype=str
          )
      # Se verifica si el archivo tiene la cantidad correcta de columnas
      if df.shape[1] == columnas_esperadas:
        # Si el archivo es correcto se agrega al DataFrame unificado
        df_unificado = pd.concat([df_unificado,df], ignore_index = True)
        print(f'✅ OK: {archivo} ({df.shape[0]} filas)')
      else:
        # Si el archivo tiene errores se agrega al DataFrame de errores
        df['archivo_origen'] = archivo # Se agrega columna para saber de dónde provino
        df_errores = pd.concat([df_errores,df], ignore_index = True)
        print(f'⚠️ ERROR: {archivo} con {df.shape[1]} columnas')

    except Exception as e:
      # Si ocurre un error al leer el archivo, se informa mediante excepción
            print(f'❌ Fallo en archivo {archivo}: {e}')
```
![image](https://github.com/user-attachments/assets/3a9e0fa5-0ae6-48ad-8c51-ce74f24777ee)

```python
# Exportamos el DataFrame con los datos correctos
df_unificado.to_csv('/content/drive/MyDrive/Productos/Limpios/lunes_lote01.csv', index=False, encoding='utf-8')

# Exportamos el DataFrame con los errores de estructura
df_errores.to_csv('/content/drive/MyDrive/Productos/Errores/lunes_lote01.csv', index=False, encoding='utf-8')

# Mensaje final de confirmación
print("✅ Archivos guardados: limpio y errores.")
```
⚠️ La estructura de la tabla **Productos** funciona como catálogo de los comercios/sucursales. Necesita atomización de datos para facilitar su mantenimiento, escalado y consumo de memoria.

- Se determina la tabla actual como **CatálogoComercial** manteniendo las columnas:
  - `id_comercio`
  - `id_bandera	id_sucursal`
  - `id_producto`
  - `productos_precio_lista`
  - `productos_precio_referencia`
  - `productos_cantidad_referencia`
  - `productos_unidad_medida_referencia`
  - `productos_precio_unitario_promo1`
  - `productos_leyenda_promo1`
  - `productos_precio_unitario_promo2`
  - `productos_leyenda_promo2`
- Normalización de texto:
  - Corrección de formato de valores en `productos_unidad_medida_referencia`.
- Reemplazo de valores: 
  - Los valores de las columnas `productos_precio_referencia`,	`productos_cantidad_referencia`,	`productos_unidad_medida_referencia` serán tratados como *N/A* siempre que no exista un precio de referencia de producto.
 
⚠️ Las columnas: `id_producto`,`productos_descripcion`,`productos_cantidad_presentacion`,	`productos_unidad_medida_presentacion`y `productos_marca` serán parte de la estructura de una nueva **Tabla Productos** utilizando Google Sheets.
