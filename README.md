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

