# 🛰️ Proyecto: Análisis de Precios Claros

## 📌 Objetivo
Análisis exploratorio autodidacta del dataset **Precios Claros - Base SEPA (Agosto 2024 - Junio 2025)**, con el fin de practicar *recolección, limpieza, transformación y visualización de datos a gran escala*, utilizando las siguientes herramientas:
- ChatGPT, código Python para transformaciones robustas.
- Python, proceso ETL.
- Google Sheets, transformaciones menores de tablas.
- Power BI, transformaciones finales y visualización de datos.
    
---

## 📦 Fase 1: Recolección de Datos

### 🔍 Fuente
- **Nombre:** Precios Claros - Base SEPA  
- **Institución:** Secretaría de Comercio Interior (Argentina)  
- **Descripción:** Sistema Electrónico de Publicidad de Precios Argentinos. Reúne información diaria de más de 70.000 productos en grandes comercios del país.  
- **Frecuencia:** Diaria  
- **Volumen estimado:** ~80 millones de registros totales
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

### 🐍 Renombrado y Unificación

Para facilitar el posterior análisis, se desarrolló un script en Python que copia y renombra todos los archivos agregando prefijos con el día y la fecha, evitando colisiones por nombres duplicados:

<img width="1954" height="1204" alt="renombrar" src="https://github.com/user-attachments/assets/e5cb5505-601f-4765-955f-3522786f40c0" />

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
- **Filas:** 20.619  
- **Columnas:** 22

#### 🔧 Transformaciones aplicadas:
- Eliminación de filas con valores `null` o el string `"null"`.
- Eliminación de columnas innecesarias para el análisis:
  - `sucursales_nombre`
  - `sucursales_calle`
  - `sucursales_numero`
  - `sucursales_observaciones`
  - `sucursales_barrio`
  - `sucursales_codigo_postal`
- Normalización de texto:
  - Corrección de formato de valores en `sucursales_tipo`, `sucursales_localidad`.
- Reemplazo de valores: 
  - `sucursales_provincia`
  
### 🐍 Corrección y normalización de horarios
  - Las celdas con horarios tienen diferentes formatos y rangos que no permiten su correcta segmentación.

<img width="2036" height="4054" alt="limpiar_horarios" src="https://github.com/user-attachments/assets/5756e184-5476-4b0c-b555-23fd668884f9" />
  
  - Los horarios limpios se categorizan según la cantidad de horas trabajadas:
    - Jornada Normal: ≤ 8 hs 
    - Jornada Doble: > 8 hs y ≤ 11 hs
    - Jornada Extendida: > 11 hs

<img width="2692" height="2496" alt="calcular_categorizar_jornadas" src="https://github.com/user-attachments/assets/b5383762-2d8f-4bf5-9cdc-f639c52b2714" />

- Eliminación de duplicados.

### 🔄 Transformación en Power BI
- Aplicación de función unpivot en columnas de día de semana con jornadas, se crean columnas: `sucursal_dia_atencion`, `sucursal_jornada`.
- Eliminación de columnas: `sucursal_lat`, `sucursal_long` por ingreso erróneo de valores.
- Creación de Tablas de Entorno:
  - **Provincias**: Presenta latitud y longitud de cada provincia para la correcta ubicación en gráficos.
  - **Medidas**: Presenta medidas relevantes para próximo análisis.
 
#### ✅ Resultado final: 
- **Filas:** 21.826
- **Columnas:** 7

### 🗒️ TABLA PRODUCTOS
#### 🧹 Datos iniciales: 
- **Filas:** +80 millones 
- **Columnas:** 17

Los archivos csv presentan un peso aproximado de 8GB, no son fácilmente tratables, presentan errores en la carga y precisan un tratamiento robusto para obtener buenos resultados.

#### 🔧 Tratamiento inicial:
- Separación manual de archivos por lotes para tratamiento idividual

### 🐍 Filtrado y Unificación
- Se utiliza Google Colab + Python + Google Drive para identificar y unificar archivos csv con la cantidad de columnas correctas.

<img width="2134" height="2382" alt="unificar" src="https://github.com/user-attachments/assets/989dc03f-5984-4dd9-a72a-e4c172901839" />

⚠️ La estructura de la tabla **Productos** funciona como catálogo de los comercios/sucursales. Necesita atomización de datos para facilitar su mantenimiento, escalado y consumo de memoria.

- Se determina la tabla actual como **CatálogoComercial** manteniendo las columnas:
  - `id_comercio`
  - `id_bandera`
  - `id_sucursal`
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
  - Los valores de las columnas `productos_precio_referencia`,	`productos_cantidad_referencia`,	`productos_unidad_medida_referencia` serán tratados como N/A siempre que no exista un precio de referencia de producto.
- Eliminación de filas con metadata.
 
⚠️ Las columnas: `id_producto`,`productos_descripcion`,`productos_cantidad_presentacion`,	`productos_unidad_medida_presentacion`y `productos_marca` serán parte de la estructura de una nueva **Tabla Productos**.

### 🐍 Python: Limpieza y Segmentación
- Unificación de archivos csv en carpeta Productos y carpeta CatálogoComercial después de la primer etapa de limpieza.

<img width="2134" height="2648" alt="limpieza_y_segmentacion" src="https://github.com/user-attachments/assets/c82d90ef-a528-4c67-9224-571890aeb431" />

- Eliminación de duplicados y reporte de estado final de las tablas.

<img width="1788" height="2268" alt="eliminar_duplicados" src="https://github.com/user-attachments/assets/c0a0125e-8845-4e99-bc43-adebc88fd219" />

#### ✅ Resultado final: 
- **Tabla:** Productos
- **Filas:** 71.781
- **Columnas:** 5
- **Tabla:** CatalálogoComercial
- **Filas:** 13.829.327
- **Columnas:** 12

---

## 🛠️ Fase 3: Visualización en Power BI
