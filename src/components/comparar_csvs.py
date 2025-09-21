import pandas as pd

# Cargar ambos archivos (usando encoding robusto y delimitador correcto)
df_original = pd.read_csv('votaciones2024_con_municipio.csv', delimiter='|', encoding='latin1')
df_limpio = pd.read_csv('votaciones2024_con_municipio_limpio.csv', delimiter='|', encoding='latin1')

# Columnas clave para identificar filas únicas (sin municipio, para comparar solo por casilla y votos)
clave_cols = [
    'CLAVE_CASILLA','CLAVE_ACTA','ID_ESTADO','NOMBRE_ESTADO','ID_DISTRITO','NOMBRE_DISTRITO','SECCION','ID_CASILLA','TIPO_CASILLA','CASILLA',
    'TIPO_ACTA','PAN','PRI','PRD','PVEM','PT','MC','MORENA','CANDIDATO_A_INDEPENDIENTE','PAN_PRI_PRD','PAN_PRI','PAN_PRD','PRI_PRD','PVEM_PT_MORENA','PVEM_PT','PVEM_MORENA','PT_MORENA','CANDIDATO/A NO REGISTRADO/A','VOTOS NULOS','TOTAL_VOTOS_CALCULADOS','LISTA_NOMINAL'
]

# Solo usar columnas que existan en ambos
def columnas_comunes(df1, df2, cols):
    return [col for col in cols if col in df1.columns and col in df2.columns]

cols_comparar = columnas_comunes(df_original, df_limpio, clave_cols)

# Buscar filas del original que NO están en el limpio (por claves de conteo, sin municipio)
df_merge = df_original.merge(df_limpio, on=cols_comparar, how='left', indicator=True)
df_faltantes = df_merge[df_merge['_merge'] == 'left_only']

# Mostrar cuántas filas faltan y guardar resultado para revisión
df_faltantes[['CLAVE_CASILLA','MUNICIPIO_x'] + [c for c in cols_comparar if c not in ['CLAVE_CASILLA','MUNICIPIO']]].to_csv('faltantes_en_limpio.csv', sep='|', index=False, encoding='latin1')
print(f"Filas en original que faltan en limpio: {len(df_faltantes)}. Guardadas en faltantes_en_limpio.csv")
