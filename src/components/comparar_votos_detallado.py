import pandas as pd

def comparar_votos_detallado(nombre):
    original = f'votaciones{nombre}.csv'
    limpio = f'votaciones{nombre}_con_municipio_limpio.csv'
    salida = f'diferencias_votos_{nombre}.csv'

    df1 = pd.read_csv(original, delimiter='|', encoding='latin1')
    df2 = pd.read_csv(limpio, delimiter='|', encoding='latin1')

    # Columnas clave para identificar la casilla única
    claves = [
        'CLAVE_CASILLA','CLAVE_ACTA','ID_ESTADO','NOMBRE_ESTADO','ID_DISTRITO','NOMBRE_DISTRITO','SECCION','ID_CASILLA','TIPO_CASILLA','CASILLA'
    ]
    # Columnas de votos a comparar
    votos = [
        'PAN','PRI','PRD','PVEM','PT','MC','MORENA','CANDIDATO_A_INDEPENDIENTE',
        'PAN_PRI_PRD','PAN_PRI','PAN_PRD','PRI_PRD','PVEM_PT_MORENA','PVEM_PT','PVEM_MORENA','PT_MORENA',
        'CANDIDATO/A NO REGISTRADO/A','VOTOS NULOS','TOTAL_VOTOS_CALCULADOS'
    ]
    claves_exist = [c for c in claves if c in df1.columns and c in df2.columns]
    votos_exist = [v for v in votos if v in df1.columns and v in df2.columns]

    # Unir por claves
    merged = df1.merge(df2, on=claves_exist, suffixes=('_orig','_limpio'))
    diferencias = []
    for v in votos_exist:
        dif = merged[merged[f'{v}_orig'] != merged[f'{v}_limpio']]
        if not dif.empty:
            difs = dif[claves_exist + [f'{v}_orig', f'{v}_limpio']]
            difs['COLUMNA'] = v
            diferencias.append(difs)
    if diferencias:
        df_dif = pd.concat(diferencias)
        df_dif.to_csv(salida, sep='|', index=False, encoding='latin1')
        print(f"Diferencias encontradas en {nombre}: {len(df_dif)} filas. Guardadas en {salida}")
    else:
        print(f"No se encontraron diferencias de votos en {nombre}.")

for año in ['2024','2021','2018']:
    try:
        comparar_votos_detallado(año)
    except Exception as e:
        print(f"Error procesando {año}: {e}")
