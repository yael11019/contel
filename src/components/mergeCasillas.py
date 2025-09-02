import pandas as pd
import os

# Archivos de entrada
votos_files = {
    "2018": "votaciones2018.csv",
    "2021": "votaciones2021.csv",
    "2024": "votaciones2024.csv"
}
casillas_file = "casillasLimpio.csv"

# Verificar que el archivo de casillas existe
if not os.path.exists(casillas_file):
    print(f"❌ Error: No se encuentra el archivo {casillas_file}")
    exit()

# Cargar tabla de casillas
print(f"📂 Cargando {casillas_file}...")
try:
    casillas = pd.read_csv(casillas_file)
    print(f"✅ Casillas cargadas: {len(casillas)} registros")
    print(f"📝 Columnas en casillas: {list(casillas.columns)}")
    
    # Normalizar nombres de columnas en casillas
    casillas.columns = casillas.columns.str.upper().str.strip()
    
    # Verificar que tenga las columnas necesarias
    if 'SECCION' not in casillas.columns:
        print("❌ Error: No se encuentra la columna SECCION en casillas")
        print(f"Columnas disponibles: {list(casillas.columns)}")
        exit()
    
    if 'MUNICIPIO' not in casillas.columns:
        print("❌ Error: No se encuentra la columna MUNICIPIO en casillas")
        print(f"Columnas disponibles: {list(casillas.columns)}")
        exit()
        
except Exception as e:
    print(f"❌ Error cargando casillas: {e}")
    exit()

# Iterar sobre los CSV de votaciones
for anio, file in votos_files.items():
    print(f"\n🔄 Procesando {file} ({anio})...")
    
    # Verificar que el archivo existe
    if not os.path.exists(file):
        print(f"⚠️  Archivo {file} no encontrado, saltando...")
        continue
    
    try:
        # Cargar archivo de votaciones
        if file.endswith('.csv'):
            # Probar diferentes separadores y encodings
            try:
                df = pd.read_csv(file, sep="|", encoding="latin-1")
            except:
                try:
                    df = pd.read_csv(file, sep=",", encoding="utf-8")
                except:
                    df = pd.read_csv(file, sep=",", encoding="latin-1")
        
        print(f"✅ Votaciones cargadas: {len(df)} registros")
        print(f"📝 Columnas en votaciones: {list(df.columns)[:10]}...")  # Solo primeras 10
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.replace('"', '').str.upper().str.strip()
        
        # Buscar columna de sección (puede tener diferentes nombres)
        seccion_col = None
        for col in df.columns:
            if 'SECCION' in col.upper():
                seccion_col = col
                break
        
        if seccion_col is None:
            print(f"❌ Error: No se encuentra columna de SECCION en {file}")
            print(f"Columnas disponibles: {list(df.columns)}")
            continue
        
        # Renombrar a SECCION estándar
        if seccion_col != 'SECCION':
            df.rename(columns={seccion_col: 'SECCION'}, inplace=True)
        
        # Convertir SECCION a int para hacer match
        df['SECCION'] = pd.to_numeric(df['SECCION'], errors='coerce')
        casillas['SECCION'] = pd.to_numeric(casillas['SECCION'], errors='coerce')
        
        # Mostrar estadísticas antes del merge
        print(f"📊 Secciones únicas en votaciones: {df['SECCION'].nunique()}")
        print(f"📊 Secciones únicas en casillas: {casillas['SECCION'].nunique()}")
        
        # Hacer el merge
        df_original_len = len(df)
        df = df.merge(casillas[["SECCION", "MUNICIPIO"]], on="SECCION", how="left")
        
        # Verificar resultados del merge
        municipios_agregados = df['MUNICIPIO'].notna().sum()
        print(f"✅ Merge completado: {municipios_agregados}/{df_original_len} registros con municipio")
        
        if municipios_agregados == 0:
            print("⚠️  Advertencia: No se agregaron municipios. Verificar compatibilidad de secciones.")
            # Mostrar algunas secciones de ejemplo
            print(f"Ejemplos de secciones en votaciones: {sorted(df['SECCION'].dropna().unique())[:10]}")
            print(f"Ejemplos de secciones en casillas: {sorted(casillas['SECCION'].dropna().unique())[:10]}")
        
        # Guardar nuevo archivo
        output_file = f"votaciones{anio}_con_municipio.csv"
        df.to_csv(output_file, index=False, sep="|", encoding="latin-1")
        print(f"✅ Archivo generado: {output_file}")
        print(f"📁 Tamaño: {len(df)} registros, {len(df.columns)} columnas")
        
    except Exception as e:
        print(f"❌ Error procesando {file}: {e}")
        continue

print("\n🎉 Proceso completado!")