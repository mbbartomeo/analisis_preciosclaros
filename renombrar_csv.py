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
