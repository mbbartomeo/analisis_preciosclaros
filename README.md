# 🛰️ Proyecto: Análisis de Precios Claros

## 📌 Objetivo
Análisis exploratorio autodidacta del dataset *Precios Claros - Base SEPA*, con el fin de practicar recolección, limpieza, transformación y visualización de datos a gran escala, utilizando las siguientes herramientas:
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

![renombrar](https://github.com/user-attachments/assets/e313df96-91bd-4ea8-985e-37a60d93a224)

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

  ![limpiar_horarios](https://github.com/user-attachments/assets/a1b27cb5-6f54-4c24-906a-c259d14aa667)
  
  - Los horarios limpios se categorizan según la cantidad de horas trabajadas:
    - Jornada Normal: ≤ 8 hs 
    - Jornada Doble: > 8 hs y ≤ 11 hs
    - Jornada Extendida: > 11 hs

![calcular_categorizar_jornadas](https://github.com/user-attachments/assets/6b163e23-614d-411e-a2c7-669ee58ce246)

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

![unificar](https://github.com/user-attachments/assets/3ca91ebc-70b5-4861-96bc-85e16f5a8ebe)

![image](https://github.com/user-attachments/assets/3a9e0fa5-0ae6-48ad-8c51-ce74f24777ee)

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
- Eliminación de duplicados y reporte de estado final de las tablas.

![limpieza_y_segmentacion](https://github.com/user-attachments/assets/c183c8a4-a238-452a-9efb-f224c1c2d35b)

![eliminar_duplicados](https://github.com/user-attachments/assets/dd6dc25a-00ac-4f0f-965d-1f541ba1a43f)

![image](https://github.com/user-attachments/assets/b8dfe7da-b9b5-487e-9676-8b0000421a10)

#### ✅ Resultado final: 
- **Tabla:** Productos
- **Filas:** 71.781
- **Columnas:** 5
- **Tabla:** CatalálogoComercial
- **Filas:** 13.829.327
- **Columnas:** 12

---

## 🛠️ Fase 3: Visualización en Power BI
