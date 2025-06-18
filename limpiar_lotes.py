# Dar acceso a Drive en Google Colab
# from google.colab import drive
# drive.mount('/content/drive')

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

# Exportamos el DataFrame con los datos correctos
df_unificado.to_csv('/content/drive/MyDrive/Productos/Limpios/lunes_lote01.csv', index=False, encoding='utf-8')

# Exportamos el DataFrame con los errores de estructura
df_errores.to_csv('/content/drive/MyDrive/Productos/Errores/lunes_lote01.csv', index=False, encoding='utf-8')

# Mensaje final de confirmación
print("✅ Archivos guardados: limpio y errores.")