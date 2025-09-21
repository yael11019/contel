import pandas as pd

# Archivos a limpiar (entrada y salida)
archivos = [
    ("votaciones2024_con_municipio.csv", "votaciones2024_con_municipio_limpio.csv"),
    ("votaciones2021_con_municipio.csv", "votaciones2021_con_municipio_limpio.csv"),
    ("votaciones2018_con_municipio.csv", "votaciones2018_con_municipio_limpio.csv")
]

# Columnas de conteo de votos (todas las columnas numéricas de votos)
voto_cols = [
    'PAN','PRI','PRD','PVEM','PT','MC','MORENA','CANDIDATO_A_INDEPENDIENTE',
    'PAN_PRI_PRD','PAN_PRI','PAN_PRD','PRI_PRD','PVEM_PT_MORENA','PVEM_PT','PVEM_MORENA','PT_MORENA',
    'CANDIDATO/A NO REGISTRADO/A','VOTOS NULOS','TOTAL_VOTOS_CALCULADOS'
]

# Columnas clave para identificar duplicados (estado, distrito, municipio, sección, casilla, etc.)
clave_cols = [
    'ID_ESTADO','NOMBRE_ESTADO','ID_DISTRITO','NOMBRE_DISTRITO','SECCION','ID_CASILLA','TIPO_CASILLA','CASILLA','MUNICIPIO'
]

for archivo_entrada, archivo_salida in archivos:
    try:
        df = pd.read_csv(archivo_entrada, delimiter='|', encoding='latin1')
        voto_cols_exist = [col for col in voto_cols if col in df.columns]
        clave_cols_exist = [col for col in clave_cols if col in df.columns]
        df_clean = df.drop_duplicates(subset=clave_cols_exist + voto_cols_exist, keep='first')
        df_clean.to_csv(archivo_salida, sep='|', index=False, encoding='latin1')
        print(f"{archivo_entrada}: Filas originales: {len(df)} | Filas limpias: {len(df_clean)} -> Guardado en {archivo_salida}")
    except Exception as e:
        print(f"No se pudo procesar {archivo_entrada}: {e}")
