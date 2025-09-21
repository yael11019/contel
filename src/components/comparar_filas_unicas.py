import pandas as pd

# Archivos a comparar
a1 = 'votaciones2024_con_municipio.csv'
a2 = 'votaciones2024_con_municipio_limpio.csv'

# Columnas clave para identificar casilla única (sin municipio)
claves = [
    'CLAVE_CASILLA','CLAVE_ACTA','ID_ESTADO','NOMBRE_ESTADO','ID_DISTRITO','NOMBRE_DISTRITO','SECCION','ID_CASILLA','TIPO_CASILLA','CASILLA',
    'TIPO_ACTA'
]

# Cargar archivos
df1 = pd.read_csv(a1, delimiter='|', encoding='latin1')
df2 = pd.read_csv(a2, delimiter='|', encoding='latin1')

# Filas en original que no están en limpio (por claves)
df1_unicos = df1.merge(df2, on=claves, how='left', indicator=True)
df1_solo = df1_unicos[df1_unicos['_merge'] == 'left_only']
df1_solo.to_csv('solo_en_original.csv', sep='|', index=False, encoding='latin1')

# Filas en limpio que no están en original (por claves)
df2_unicos = df2.merge(df1, on=claves, how='left', indicator=True)
df2_solo = df2_unicos[df2_unicos['_merge'] == 'left_only']
df2_solo.to_csv('solo_en_limpio.csv', sep='|', index=False, encoding='latin1')

print(f"Filas solo en original: {len(df1_solo)} | solo en limpio: {len(df2_solo)}")

# Buscar claves repetidas con diferente municipio
df1_keys = df1[claves + ['MUNICIPIO']].drop_duplicates()
df2_keys = df2[claves + ['MUNICIPIO']].drop_duplicates()

# Unir por claves y ver si el municipio es diferente
df_merge = df1_keys.merge(df2_keys, on=claves, suffixes=('_orig','_limpio'))
dif_muni = df_merge[df_merge['MUNICIPIO_orig'] != df_merge['MUNICIPIO_limpio']]
dif_muni.to_csv('diferente_municipio.csv', sep='|', index=False, encoding='latin1')
print(f"Filas con misma clave pero diferente municipio: {len(dif_muni)}")
