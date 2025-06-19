import pandas as pd
import os
import glob

# Rutas a las carpetas
ruta_productos = r'D:\Archivos\Proyecto_PreciosClaros\datos\Productos'
ruta_catalogo = r'D:\Archivos\Proyecto_PreciosClaros\datos\CatálogoComercial'

# Función para unir archivos CSV y reportar duplicados
def unir_csv_y_reportar(ruta_carpeta, nombre_salida, columnas_duplicadas):
    archivos = glob.glob(os.path.join(ruta_carpeta, '*.csv'))
    print(f"📁 Procesando carpeta: {ruta_carpeta}")
    print(f"🔎 Archivos encontrados: {len(archivos)}")
    
    dataframes = []
    for archivo in archivos:
        df = pd.read_csv(archivo, low_memory=False)
        dataframes.append(df)
    
    df_unido = pd.concat(dataframes, ignore_index=True)
    total_filas = len(df_unido)

    df_sin_duplicados = df_unido.drop_duplicates(subset=columnas_duplicadas, keep='first')
    total_final = len(df_sin_duplicados)
    duplicados_eliminados = total_filas - total_final

    print(f"🧮 Total de filas unificadas: {total_filas}")
    print(f"❌ Duplicados eliminados: {duplicados_eliminados}")
    print(f"✅ Filas finales limpias: {total_final}\n")

    df_sin_duplicados.to_csv(f'{nombre_salida}_Unificado.csv', index=False)

    return {
        'archivos': len(archivos),
        'filas_originales': total_filas,
        'duplicados': duplicados_eliminados,
        'filas_finales': total_final
    }

# Procesar Productos
reporte_productos = unir_csv_y_reportar(
    ruta_productos,
    'Productos',
    ['id_producto']
)

# Procesar CatálogoComercial
reporte_catalogo = unir_csv_y_reportar(
    ruta_catalogo,
    'CatalogoComercial',
    ['id_comercio', 'id_sucursal', 'id_producto']
)

# Mostrar resumen final
print("📋 Resumen de procesamiento:")
print(f"📦 Productos - Archivos: {reporte_productos['archivos']}, Filas: {reporte_productos['filas_originales']}, Duplicados: {reporte_productos['duplicados']}, Final: {reporte_productos['filas_finales']}")
print(f"🏪 CatálogoComercial - Archivos: {reporte_catalogo['archivos']}, Filas: {reporte_catalogo['filas_originales']}, Duplicados: {reporte_catalogo['duplicados']}, Final: {reporte_catalogo['filas_finales']}")

