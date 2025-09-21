import pandas as pd

def comparar_archivos(nombre):
    original = f'votaciones{nombre}_con_municipio.csv'
    limpio = f'votaciones{nombre}_con_municipio_limpio.csv'
    salida = f'faltantes_en_limpio_{nombre}.csv'

    df_original = pd.read_csv(original, delimiter='|', encoding='latin1')
    df_limpio = pd.read_csv(limpio, delimiter='|', encoding='latin1')

    clave_cols = [
        'CLAVE_CASILLA','CLAVE_ACTA','ID_ESTADO','NOMBRE_ESTADO','ID_DISTRITO','NOMBRE_DISTRITO','SECCION','ID_CASILLA','TIPO_CASILLA','CASILLA',
        'TIPO_ACTA','PAN','PRI','PRD','PVEM','PT','MC','MORENA','CANDIDATO_A_INDEPENDIENTE','PAN_PRI_PRD','PAN_PRI','PAN_PRD','PRI_PRD','PVEM_PT_MORENA','PVEM_PT','PVEM_MORENA','PT_MORENA','CANDIDATO/A NO REGISTRADO/A','VOTOS NULOS','TOTAL_VOTOS_CALCULADOS','LISTA_NOMINAL'
    ]
    def columnas_comunes(df1, df2, cols):
        return [col for col in cols if col in df1.columns and col in df2.columns]
    cols_comparar = columnas_comunes(df_original, df_limpio, clave_cols)
    df_merge = df_original.merge(df_limpio, on=cols_comparar, how='left', indicator=True)
    df_faltantes = df_merge[df_merge['_merge'] == 'left_only']
    df_faltantes[['CLAVE_CASILLA','MUNICIPIO_x'] + [c for c in cols_comparar if c not in ['CLAVE_CASILLA','MUNICIPIO']]].to_csv(salida, sep='|', index=False, encoding='latin1')
    print(f"{original}: Filas en original que faltan en limpio: {len(df_faltantes)}. Guardadas en {salida}")

for año in ['2024','2021','2018']:
    try:
        comparar_archivos(año)
    except Exception as e:
        print(f"Error procesando {año}: {e}")
