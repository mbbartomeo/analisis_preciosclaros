import pandas as pd
import os

# Ruta al archivo CSV a procesar
archivo = r'D:\Archivos\Proyecto_PreciosClaros\datos\Productos\lunes_lote02.csv' 

# Leer archivo
df = pd.read_csv(archivo, sep=',', encoding='utf-8', low_memory=False)

# Eliminar filas con metadata (donde id_producto no sea numérico)
df = df[pd.to_numeric(df['id_producto'], errors='coerce').notnull()]

# Convertir a numérico para aplicar la lógica de precios de referencia
df['productos_precio_referencia'] = pd.to_numeric(df['productos_precio_referencia'], errors='coerce')

# Reemplazo por NaN si productos_precio_referencia está vacío o es 0
cond = (df['productos_precio_referencia'].isna()) | (df['productos_precio_referencia'] == 0)
df.loc[cond, ['productos_precio_referencia',
              'productos_cantidad_referencia',
              'productos_unidad_medida_referencia']] = pd.NA

# Normalizar a mayúsculas ignorando valores NaN 

df['productos_descripcion'] = df['productos_descripcion'].astype(str).str.upper()

df['productos_unidad_medida_referencia'] = df['productos_unidad_medida_referencia'].astype(str).str.upper()

df['productos_unidad_medida_presentacion'] = df['productos_unidad_medida_presentacion'].where(
    df['productos_unidad_medida_presentacion'].notna(),
    pd.NA
).astype(str).str.upper()

df['productos_marca'] = df['productos_marca'].astype(str).str.upper()

# Reemplazar "UNIDAD" por "UN" para estandarizar nomenclatura
df['productos_unidad_medida_referencia'] = df['productos_unidad_medida_referencia'].replace('UNIDAD', 'UN')
df['productos_unidad_medida_presentacion'] = df['productos_unidad_medida_presentacion'].replace('UNIDAD', 'UN')

# Crear CatálogoComercial
cols_catálogo = [
    'id_comercio', 'id_bandera', 'id_sucursal', 'id_producto',
    'productos_precio_lista', 'productos_precio_referencia',
    'productos_cantidad_referencia', 'productos_unidad_medida_referencia',
    'productos_precio_unitario_promo1', 'productos_leyenda_promo1',
    'productos_precio_unitario_promo2', 'productos_leyenda_promo2'
]
df_catalogo = df[cols_catálogo]

# Crear Productos
cols_productos = [
    'id_producto', 'productos_descripcion',
    'productos_cantidad_presentacion', 'productos_unidad_medida_presentacion',
    'productos_marca'
]
df_productos = df[cols_productos]

# Exportar a archivos nuevos
lote_2 = os.path.splitext(archivo)[0] 

df_catalogo.to_csv(f"{lote_2}_CatalogoComercial.csv", index=False)
df_productos.to_csv(f"{lote_2}_Productos.csv", index=False)

print("✅ Archivos exportados correctamente.")
