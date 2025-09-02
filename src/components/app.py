import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import os
import streamlit.components.v1
from io import BytesIO 
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet 
from reportlab.lib import colors 
from reportlab.lib.units import inch
import time

# --- Configuración --- 
st.set_page_config(page_title="Sistema de Análisis Electoral", layout="wide") 

st.markdown("""
<style>
    /* Estilos más agresivos para las tablas */
    .stDataFrame, 
    .stDataFrame table,
    .stDataFrame tbody,
    .stDataFrame thead,
    .element-container .stDataFrame,
    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] table,
    div[data-testid="stDataFrame"] tbody,
    div[data-testid="stDataFrame"] thead {
        font-size: 20px !important;
        font-family: 'Arial', sans-serif !important;
    }
    
    /* Headers de tablas */
    .stDataFrame th,
    .stDataFrame thead th,
    div[data-testid="stDataFrame"] th,
    div[data-testid="stDataFrame"] thead th {
        font-size: 22px !important;
        font-weight: bold !important;
        background-color: #f0f0f0 !important;
    }
    
    /* Celdas de tablas */
    .stDataFrame td,
    .stDataFrame tbody td,
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] tbody td {
        font-size: 20px !important;
        padding: 12px !important;
    }
    
    /* Forzar en todos los elementos de tabla */
    table, table th, table td {
        font-size: 20px !important;
    }
    
    /* Métricas más grandes */
    div[data-testid="metric-container"] {
        font-size: 24px !important;
    }
    
    div[data-testid="metric-container"] > div {
        font-size: 26px !important;
    }
    
    /* Reducir títulos */
    h1 { font-size: 2.2rem !important; }
    h2 { font-size: 1.8rem !important; }
    h3 { font-size: 1.4rem !important; }
    h4 { font-size: 1.2rem !important; }
    
    /* Tabs más grandes */
    .stTabs [data-baseweb="tab-list"] button div p {
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

# Configurar matplotlib para texto más grande en gráficos
plt.rcParams.update({
    "font.size": 18,           # Tamaño base más grande
    "axes.titlesize": 24,      # Título del gráfico
    "axes.labelsize": 20,      # Etiquetas de ejes
    "xtick.labelsize": 18,     # Números en eje X
    "ytick.labelsize": 18,     # Números en eje Y
    "legend.fontsize": 18,     # Leyenda
    "figure.titlesize": 26,    # Título de figura
    "axes.titleweight": "bold" # Títulos en negrita
})

st.markdown("# 🗳️ Sistema de Análisis Electoral") 
st.markdown("## Tipo de elección: Diputación Federal")

# --- Función para mostrar tablas grandes ---
def mostrar_tabla_grande(df, titulo_columnas):
    """Mostrar tabla con texto más grande usando HTML"""
    if len(df) == 0:
        return
    
    # Crear HTML personalizado
    html = f"""
    <style>
        .tabla-grande {{
            font-size: 20px !important;
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        .tabla-grande th {{
            font-size: 22px !important;
            font-weight: bold !important;
            background-color: #f0f0f0;
            padding: 15px;
            border: 1px solid #ddd;
            text-align: center;
        }}
        .tabla-grande td {{
            font-size: 20px !important;
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }}
        .tabla-grande tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
    <table class="tabla-grande">
        <thead>
            <tr>{"".join([f"<th>{col}</th>" for col in titulo_columnas])}</tr>
        </thead>
        <tbody>
            {"".join([f"<tr>{''.join([f'<td>{val}</td>' for val in row])}</tr>" for row in df.values])}
        </tbody>
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)

# --- Cargar CSV --- 
@st.cache_data 
def load_data(): 
    # Obtener la ruta del directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    archivos = [
        ("votaciones2018_con_municipio.csv", 2018),
        ("votaciones2021_con_municipio.csv", 2021),
        ("votaciones2024_con_municipio.csv", 2024)
    ]
    dfs = []
    archivos_cargados = []
    
    for archivo, año in archivos:
        # Buscar archivo en múltiples ubicaciones posibles
        rutas_posibles = [
            archivo,  # Ruta relativa directa
            os.path.join(current_dir, archivo),  # En el mismo directorio que el script
            os.path.join(current_dir, "..", archivo),  # Un nivel arriba
            os.path.join(current_dir, "..", "..", archivo),  # Dos niveles arriba
            os.path.join("data", archivo),  # En carpeta data
            os.path.join(current_dir, "data", archivo),  # En carpeta data relativa al script
        ]
        
        archivo_encontrado = None
        
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                archivo_encontrado = ruta
                break
        
        if archivo_encontrado:
            try:
                df = pd.read_csv(archivo_encontrado, sep="|", encoding="latin-1")
                
                # Limpiar nombres de columnas
                df.columns = df.columns.str.replace('"', '')
                df.columns = df.columns.str.replace('/', '_')
                df.columns = df.columns.str.strip()
                
                # Función para limpiar texto con caracteres especiales
                def limpiar_texto(texto):
                    if pd.isna(texto):
                        return texto
                    texto = str(texto)
                    
                    # Mapeo específico para caracteres problemáticos
                    replacements = {
                        'MICHOAC�N': 'MICHOACÁN',
                        'MICHOACï¿½N': 'MICHOACÁN',
                        'M�XICO': 'MÉXICO',
                        'MÉXICOï¿½': 'MÉXICO',
                        'QUER�TARO': 'QUERÉTARO',
                        'QUERÉTAROï¿½': 'QUERÉTARO',
                        'YUCAT�N': 'YUCATÁN',
                        'YUCATÁNï¿½': 'YUCATÁN',
                        'LE�N': 'LEÓN',
                        'LEÓNï¿½': 'LEÓN',
                        'NUEVO LE�N': 'NUEVO LEÓN',
                        'SAN LUIS POTOS�': 'SAN LUIS POTOSÍ',
                        'L�ZARO C�RDENAS': 'LÁZARO CÁRDENAS',
                        'LÁZAROï¿½CÁRDENASï¿½': 'LÁZARO CÁRDENAS',
                        'ï¿½': '',
                        '�': 'Á',
                    }
                    
                    for old, new in replacements.items():
                        texto = texto.replace(old, new)
                    
                    # Si no encuentra coincidencia exacta, buscar palabras clave
                    if 'MICHOAC' in texto.upper():
                        return 'MICHOACÁN'
                    elif 'MEXICO' in texto.upper() and 'NUEVO' not in texto.upper():
                        return 'MÉXICO'
                    elif 'QUERETARO' in texto.upper():
                        return 'QUERÉTARO'
                    elif 'YUCATAN' in texto.upper():
                        return 'YUCATÁN'
                    elif 'LEON' in texto.upper() and 'NUEVO' not in texto.upper():
                        return 'LEÓN'
                    
                    return texto
                
                # Limpiar columnas de texto importantes
                if 'NOMBRE_ESTADO' in df.columns:
                    df['NOMBRE_ESTADO'] = df['NOMBRE_ESTADO'].apply(limpiar_texto)
                
                if 'NOMBRE_DISTRITO' in df.columns:
                    df['NOMBRE_DISTRITO'] = df['NOMBRE_DISTRITO'].apply(limpiar_texto)
                
                df["Año"] = año
                dfs.append(df)
                archivos_cargados.append(f"✅ {archivo}: {len(df)} registros")
                    
            except Exception as e:
                archivos_cargados.append(f"❌ {archivo}: Error al leer - {str(e)}")
        else:
            archivos_cargados.append(f"❌ {archivo}: Archivo no encontrado en ninguna ubicación")
    
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        return combined_df
    else:
        st.error("❌ No se pudieron cargar los archivos de datos")
        
        try:
            files = os.listdir(os.getcwd())
            for file in sorted(files):
                st.write(f"  - {file}")
        except Exception as e:
            st.write(f"  Error listando archivos: {e}")
        
        # Opción para subir archivos manualmente
        st.write("---")
        st.write("### 📤 Opción alternativa: Subir archivos manualmente")
        
        uploaded_files = st.file_uploader(
            "Sube los archivos CSV de votaciones:",
            type=['csv'],
            accept_multiple_files=True,
            help="Sube los archivos votaciones2018.csv, votaciones2021.csv y votaciones2024.csv"
        )
        
        if uploaded_files:
            dfs_manual = []
            for uploaded_file in uploaded_files:
                try:
                    # Determinar el año basado en el nombre del archivo
                    if "2018" in uploaded_file.name:
                        año = 2018
                    elif "2021" in uploaded_file.name:
                        año = 2021
                    elif "2024" in uploaded_file.name:
                        año = 2024
                    else:
                        st.warning(f"No se pudo determinar el año para {uploaded_file.name}")
                        continue
                    
                    df = pd.read_csv(uploaded_file, sep="|", encoding="latin-1")
                    
                    # Limpiar nombres de columnas
                    df.columns = df.columns.str.replace('"', '')
                    df.columns = df.columns.str.replace('/', '_')
                    df.columns = df.columns.str.strip()
                    
                    df["Año"] = año
                    dfs_manual.append(df)
                    st.success(f"✅ {uploaded_file.name}: {len(df)} registros cargados")
                    
                except Exception as e:
                    st.error(f"❌ Error cargando {uploaded_file.name}: {str(e)}")
            
            if dfs_manual:
                combined_df = pd.concat(dfs_manual, ignore_index=True)
                st.success(f"✅ Archivos manuales cargados: {len(combined_df)} registros totales")
                return combined_df
        
        return pd.DataFrame()

# Cargar datos
df = load_data() 

if df.empty:
    st.stop()

# --- Función auxiliar para candidatos independientes ---
def calcular_candidatos_independientes(df_año):
    """
    Calcula votos de candidatos independientes
    """
    candidatos_independientes = [
        "CAND_IND_01", "CAND_IND_02", "CANDIDATO_A_INDEPENDIENTE"
    ]
    
    mapeo_independientes = {
        "CANDIDATO_A_INDEPENDIENTE": "Candidato Independiente",
        "CAND_IND_01": "Candidato Independiente 1",
        "CAND_IND_02": "Candidato Independiente 2"
    }
    
    independientes_resultado = []
    
    for independiente in candidatos_independientes:
        if independiente in df_año.columns:
            votos = pd.to_numeric(df_año[independiente], errors='coerce').fillna(0).sum()
            if votos > 0:
                nombre = mapeo_independientes.get(independiente, independiente)
                independientes_resultado.append({"Independiente": nombre, "Votos": votos})
    
    return independientes_resultado

# --- Configuración de coaliciones agrupadas (incluyendo independientes) ---
def calcular_coaliciones_agrupadas(df_año, año):
    """
    Calcula las coaliciones agrupando votos individuales y coaliciones formales + candidatos independientes
    """
    
    # Función auxiliar para obtener votos de una columna
    def obtener_votos(columna):
        return pd.to_numeric(df_año[columna], errors='coerce').fillna(0).sum() if columna in df_año.columns else 0
    
    coaliciones_resultado = []
    
    if año == 2024:
        # Coalición PAN-PRI-PRD (2024)
        votos_oposicion = (
            obtener_votos("PAN") + obtener_votos("PRI") + obtener_votos("PRD") +
            obtener_votos("PAN_PRI_PRD") + obtener_votos("PAN_PRI") + 
            obtener_votos("PAN_PRD") + obtener_votos("PRI_PRD")
        )
        if votos_oposicion > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición PAN-PRI-PRD", "Votos": votos_oposicion})
        
        # Coalición MORENA-PT-PVEM (2024)
        votos_morena_coalition = (
            obtener_votos("MORENA") + obtener_votos("PT") + obtener_votos("PVEM") +
            obtener_votos("PVEM_PT_MORENA") + obtener_votos("PVEM_PT") + 
            obtener_votos("PVEM_MORENA") + obtener_votos("PT_MORENA")
        )
        if votos_morena_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición MORENA-PT-PVEM", "Votos": votos_morena_coalition})
        
        # MC participó solo en 2024
        votos_mc = obtener_votos("MC") + obtener_votos("MOVIMIENTO CIUDADANO")
        if votos_mc > 0:
            coaliciones_resultado.append({"Coalicion": "Movimiento Ciudadano", "Votos": votos_mc})
    
    elif año == 2021:
        # Coalición PAN-PRD-MC (2021)
        votos_pan_coalition = (
            obtener_votos("PAN") + obtener_votos("PRD") + obtener_votos("MC") + obtener_votos("MOVIMIENTO CIUDADANO") +
            obtener_votos("PAN_PRD_MC") + obtener_votos("PAN_PRD") + 
            obtener_votos("PAN_MC") + obtener_votos("PRD_MC")
        )
        if votos_pan_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición PAN-PRD-MC", "Votos": votos_pan_coalition})
        
        # Coalición PRI-PVEM-NA (2021)
        votos_pri_coalition = (
            obtener_votos("PRI") + obtener_votos("PVEM") + obtener_votos("NUEVA ALIANZA") +
            obtener_votos("PRI_PVEM_NA") + obtener_votos("PRI_PVEM") + 
            obtener_votos("PRI_NA") + obtener_votos("PVEM_NA")
        )
        if votos_pri_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición PRI-PVEM-NA", "Votos": votos_pri_coalition})
        
        # Coalición MORENA-PT-PES (2021)
        votos_morena_coalition = (
            obtener_votos("MORENA") + obtener_votos("PT") + obtener_votos("ENCUENTRO SOCIAL") +
            obtener_votos("PT_MORENA_PES") + obtener_votos("PT_MORENA") + 
            obtener_votos("PT_PES") + obtener_votos("MORENA_PES")
        )
        if votos_morena_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición MORENA-PT-PES", "Votos": votos_morena_coalition})
    
    elif año == 2018:
        # Coalición PAN-PRD-MC (2018)
        votos_pan_coalition = (
            obtener_votos("PAN") + obtener_votos("PRD") + obtener_votos("MC") + obtener_votos("MOVIMIENTO CIUDADANO") +
            obtener_votos("PAN_PRD_MC") + obtener_votos("PAN_PRD") + 
            obtener_votos("PAN_MC") + obtener_votos("PRD_MC")
        )
        if votos_pan_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición PAN-PRD-MC", "Votos": votos_pan_coalition})
        
        # Coalición PRI-PVEM-NA (2018)
        votos_pri_coalition = (
            obtener_votos("PRI") + obtener_votos("PVEM") + obtener_votos("NUEVA ALIANZA") +
            obtener_votos("PRI_PVEM_NA") + obtener_votos("PRI_PVEM") + 
            obtener_votos("PRI_NA") + obtener_votos("PVEM_NA")
        )
        if votos_pri_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición PRI-PVEM-NA", "Votos": votos_pri_coalition})
        
        # Coalición MORENA-PT-PES (2018)
        votos_morena_coalition = (
            obtener_votos("MORENA") + obtener_votos("PT") + obtener_votos("ENCUENTRO SOCIAL") +
            obtener_votos("PT_MORENA_PES") + obtener_votos("PT_MORENA") + 
            obtener_votos("PT_PES") + obtener_votos("MORENA_PES")
        )
        if votos_morena_coalition > 0:
            coaliciones_resultado.append({"Coalicion": "Coalición MORENA-PT-PES", "Votos": votos_morena_coalition})
    
    # Agregar candidatos independientes a las coaliciones
    independientes = calcular_candidatos_independientes(df_año)
    for independiente in independientes:
        coaliciones_resultado.append({"Coalicion": independiente["Independiente"], "Votos": independiente["Votos"]})
    
    # Convertir a DataFrame
    if coaliciones_resultado:
        df_coaliciones = pd.DataFrame(coaliciones_resultado)
        df_coaliciones = df_coaliciones.sort_values("Votos", ascending=False)
        return df_coaliciones
    else:
        return pd.DataFrame()

def calcular_partidos_individuales(df_año):
    """
    Calcula votos de TODOS los partidos individuales + candidatos independientes
    """
    partidos_todos = [
        "PAN", "PRI", "PRD", "PVEM", "PT", "MC", "MOVIMIENTO CIUDADANO", 
        "NUEVA ALIANZA", "MORENA", "ENCUENTRO SOCIAL"
    ]
    
    partidos_individuales = []
    
    # Agregar partidos políticos
    for partido in partidos_todos:
        if partido in df_año.columns:
            votos = pd.to_numeric(df_año[partido], errors='coerce').fillna(0).sum()
            if votos > 0:
                # Mapear nombres más legibles
                nombre_partido = {
                    "MC": "Movimiento Ciudadano",
                    "MOVIMIENTO CIUDADANO": "Movimiento Ciudadano",
                    "NUEVA ALIANZA": "Nueva Alianza",
                    "ENCUENTRO SOCIAL": "Encuentro Social"
                }.get(partido, partido)
                
                partidos_individuales.append({"Partido": nombre_partido, "Votos": votos})
    
    # Agregar candidatos independientes
    independientes = calcular_candidatos_independientes(df_año)
    for independiente in independientes:
        partidos_individuales.append({"Partido": independiente["Independiente"], "Votos": independiente["Votos"]})
    
    if partidos_individuales:
        df_partidos = pd.DataFrame(partidos_individuales)
        df_partidos = df_partidos.sort_values("Votos", ascending=False)
        return df_partidos
    else:
        return pd.DataFrame()

def calcular_otros_votos(df_año):
    """
    Calcula votos nulos y no registrados (sin candidatos independientes)
    """
    otros_votos = [
        "CNR", "CANDIDATO_A_NO_REGISTRADO_A",
        "VN", "VOTOS NULOS"
    ]
    
    mapeo_otros = {
        "CNR": "No Registrados",
        "VN": "Votos Nulos",
        "CANDIDATO_A_NO_REGISTRADO_A": "No Registrados",
        "VOTOS NULOS": "Votos Nulos"
    }
    
    otros_resultado = []
    
    for otro in otros_votos:
        if otro in df_año.columns:
            votos = pd.to_numeric(df_año[otro], errors='coerce').fillna(0).sum()
            if votos > 0:
                nombre = mapeo_otros.get(otro, otro)
                otros_resultado.append({"Otros": nombre, "Votos": votos})
    
    if otros_resultado:
        df_otros = pd.DataFrame(otros_resultado)
        df_otros = df_otros.sort_values("Votos", ascending=False)
        return df_otros
    else:
        return pd.DataFrame()

# --- Filtros con jerarquía corregida --- 
st.sidebar.header("Filtros") 

# Usar NOMBRE_ESTADO como columna principal
estado_col = "NOMBRE_ESTADO"
estados_unicos = df[estado_col].dropna().astype(str).unique()

# Inicializar session state para los filtros
if 'estado_anterior' not in st.session_state:
    st.session_state.estado_anterior = None
if 'distrito_anterior' not in st.session_state:
    st.session_state.distrito_anterior = None
if 'municipio_anterior' not in st.session_state:
    st.session_state.municipio_anterior = None
if 'seccion_anterior' not in st.session_state:
    st.session_state.seccion_anterior = None

# 1. FILTRO DE ESTADO
estado_sel = st.sidebar.selectbox("Estado", sorted(estados_unicos)) 
df_estado = df[df[estado_col] == estado_sel] 

# Verificar si cambió el estado
if st.session_state.estado_anterior != estado_sel:
    if st.session_state.estado_anterior is not None:
        time.sleep(0.1)
    st.session_state.estado_anterior = estado_sel

# 2. FILTRO DE DISTRITO (basado en estado)
if len(df_estado) > 0:
    distritos_con_id = df_estado.apply(lambda row: f"{row['ID_DISTRITO']} - {row['NOMBRE_DISTRITO']}", axis=1).dropna().unique()
    distritos_opciones = ["Todos"] + sorted(distritos_con_id)
    distrito_sel = st.sidebar.selectbox("Distrito", distritos_opciones, index=0)
    
    # Verificar si cambió el distrito
    if st.session_state.distrito_anterior != distrito_sel:
        if st.session_state.distrito_anterior is not None:
            time.sleep(0.1)
        st.session_state.distrito_anterior = distrito_sel
    
    if distrito_sel == "Todos":
        df_distrito = df_estado
        distrito_display = "Todos los distritos"
    else:
        nombre_distrito = distrito_sel.split(" - ", 1)[1] if " - " in distrito_sel else distrito_sel
        df_distrito = df_estado[df_estado["NOMBRE_DISTRITO"] == nombre_distrito]
        distrito_display = distrito_sel
else:
    df_distrito = df_estado
    distrito_display = "No hay datos disponibles"
    distrito_sel = "Todos"

# 3. FILTRO DE MUNICIPIO (basado en distrito)
if len(df_distrito) > 0 and "MUNICIPIO" in df_distrito.columns:
    municipios_unicos = df_distrito["MUNICIPIO"].dropna().astype(str).unique()
    municipios_opciones = ["Todos"] + sorted(municipios_unicos)
    municipio_sel = st.sidebar.selectbox("Municipio", municipios_opciones, index=0)
    
    # Verificar si cambió el municipio
    if st.session_state.municipio_anterior != municipio_sel:
        if st.session_state.municipio_anterior is not None:
            time.sleep(0.1)
        st.session_state.municipio_anterior = municipio_sel
    
    if municipio_sel == "Todos":
        df_municipio = df_distrito
        municipio_display = "Todos los municipios"
    else:
        df_municipio = df_distrito[df_distrito["MUNICIPIO"] == municipio_sel]
        municipio_display = municipio_sel
else:
    df_municipio = df_distrito
    municipio_display = "No disponible"
    municipio_sel = "Todos"

# 4. FILTRO DE SECCIÓN (basado en municipio)
if len(df_municipio) > 0:
    secciones_unicas = df_municipio["SECCION"].dropna().astype(int).unique()
    secciones_ordenadas = sorted(secciones_unicas)
    secciones_opciones = ["Todas"] + [str(s) for s in secciones_ordenadas]
    
    seccion_sel = st.sidebar.selectbox("Sección", secciones_opciones, index=0)
    
    # Verificar si cambió la sección
    if st.session_state.seccion_anterior != seccion_sel:
        if st.session_state.seccion_anterior is not None:
            time.sleep(0.1)
        st.session_state.seccion_anterior = seccion_sel
    
    if seccion_sel == "Todas":
        df_seccion = df_municipio
        seccion_display = "Todas las secciones"
    else:
        df_seccion = df_municipio[df_municipio["SECCION"].astype(str) == seccion_sel]
        
        # Obtener tipos de casilla únicos para la sección seleccionada
        if len(df_seccion) > 0:
            # Buscar columna TIPO_CASILLA o CASILLA
            tipo_col = None
            if "TIPO_CASILLA" in df_seccion.columns:
                tipo_col = "TIPO_CASILLA"
            elif "CASILLA" in df_seccion.columns:
                tipo_col = "CASILLA"
            
            if tipo_col:
                tipos_casilla = df_seccion[tipo_col].dropna().unique()
                if len(tipos_casilla) > 0:
                    tipos_casilla_str = ", ".join(sorted(tipos_casilla))
                    seccion_display = f"Sección {seccion_sel} ({tipos_casilla_str})"
                else:
                    seccion_display = f"Sección {seccion_sel}"
            else:
                seccion_display = f"Sección {seccion_sel}"
        else:
            seccion_display = f"Sección {seccion_sel}"
else:
    df_seccion = pd.DataFrame()
    seccion_display = "No hay datos disponibles"

# Reemplazar desde la línea ~700 (después del título principal) hasta donde empiezan las métricas:

if len(df_seccion) > 0:
    # Título principal con jerarquía correcta: Estado - Distrito - Municipio - Sección
    if municipio_sel == "Todos":
        st.header(f"📊 Resultados para {estado_sel} - {distrito_display} - {municipio_display} - {seccion_display}")
    else:
        st.header(f"📊 Resultados para {estado_sel} - {distrito_display} - {municipio_sel} - {seccion_display}")
    
    # Obtener años disponibles en orden descendente: 2024, 2021, 2018
    años_disponibles = sorted(df_seccion["Año"].unique(), reverse=True)
    
    # Función para procesar resultados por año
    def procesar_año(df_año, año):
        # Contar número de casillas únicas
        num_casillas = len(df_año)
        
        # Calcular coaliciones agrupadas (incluye independientes)
        suma_coaliciones = calcular_coaliciones_agrupadas(df_año, año)
        
        # Calcular partidos individuales (incluye independientes)
        suma_partidos = calcular_partidos_individuales(df_año)
        
        # Calcular otros votos (solo nulos y no registrados)
        suma_otros = calcular_otros_votos(df_año)
        
        # Calcular totales por separado para cada análisis
        total_coaliciones = suma_coaliciones["Votos"].sum() if len(suma_coaliciones) > 0 else 0
        total_otros_coaliciones = suma_otros["Votos"].sum() if len(suma_otros) > 0 else 0
        total_votos_coaliciones = total_coaliciones + total_otros_coaliciones
        
        total_partidos = suma_partidos["Votos"].sum() if len(suma_partidos) > 0 else 0
        total_otros_partidos = suma_otros["Votos"].sum() if len(suma_otros) > 0 else 0
        total_votos_partidos = total_partidos + total_otros_partidos
        
        # Calcular porcentajes para coaliciones
        if len(suma_coaliciones) > 0 and total_votos_coaliciones > 0:
            suma_coaliciones["Porcentaje"] = round((suma_coaliciones["Votos"] / total_votos_coaliciones) * 100, 2)
            suma_coaliciones["Votos_Formatted"] = suma_coaliciones["Votos"].apply(lambda x: f"{int(x):,}")
            suma_coaliciones["Porcentaje_Formatted"] = suma_coaliciones["Porcentaje"].apply(lambda x: f"{x}%")
        
        # Calcular porcentajes para partidos individuales
        if len(suma_partidos) > 0 and total_votos_partidos > 0:
            suma_partidos["Porcentaje"] = round((suma_partidos["Votos"] / total_votos_partidos) * 100, 2)
            suma_partidos["Votos_Formatted"] = suma_partidos["Votos"].apply(lambda x: f"{int(x):,}")
            suma_partidos["Porcentaje_Formatted"] = suma_partidos["Porcentaje"].apply(lambda x: f"{x}%")
        
        # Calcular porcentajes para otros votos (usando total de coaliciones como base)
        if len(suma_otros) > 0 and total_votos_coaliciones > 0:
            suma_otros["Porcentaje"] = round((suma_otros["Votos"] / total_votos_coaliciones) * 100, 2)
            suma_otros["Votos_Formatted"] = suma_otros["Votos"].apply(lambda x: f"{int(x):,}")
            suma_otros["Porcentaje_Formatted"] = suma_otros["Porcentaje"].apply(lambda x: f"{x}%")
        
        # Calcular lista nominal y participación
        lista_nominal_cols = ["LISTA_NOMINAL", "LISTA_NOMINAL_CASILLA"]
        lista_nominal = 0
        
        for col in lista_nominal_cols:
            if col in df_año.columns:
                lista_nominal = pd.to_numeric(df_año[col], errors='coerce').fillna(0).sum()
                break
        
        lista_nominal = float(lista_nominal) if lista_nominal else 0
        porcentaje_participacion = round((total_votos_coaliciones / lista_nominal) * 100, 2) if lista_nominal > 0 else 0
        
        # Determinar ganadores
        ganador_coalicion = ""
        ganador_partido = ""
        
        if len(suma_coaliciones) > 0:
            ganador_coalicion = suma_coaliciones.iloc[0]["Coalicion"]
        
        if len(suma_partidos) > 0:
            ganador_partido = suma_partidos.iloc[0]["Partido"]
        
        return {
            'coaliciones': suma_coaliciones,
            'partidos': suma_partidos,
            'otros': suma_otros,
            'num_casillas': num_casillas,
            'total_votos': total_votos_coaliciones,
            'lista_nominal': lista_nominal,
            'porcentaje_participacion': porcentaje_participacion,
            'ganador_coalicion': ganador_coalicion,
            'ganador_partido': ganador_partido
        }

    # Procesar resultados para todos los años
    resultados_por_año = {}
    
    for año in años_disponibles:
        df_año = df_seccion[df_seccion["Año"] == año]
        if len(df_año) > 0:
            resultados = procesar_año(df_año, año)
            resultados_por_año[año] = resultados

    # ===== SECCIÓN DE RESUMEN GENERAL =====
    st.subheader("📈 Resumen General por Proceso Electoral")
    
    # Crear columnas para cada año disponible
    if len(años_disponibles) == 3:
        col1, col2, col3 = st.columns(3)
        columnas = [col1, col2, col3]
    elif len(años_disponibles) == 2:
        col1, col2 = st.columns(2)
        columnas = [col1, col2]
    else:
        col1 = st.columns(1)[0]
        columnas = [col1]
    
    for i, año in enumerate(años_disponibles):
        if año in resultados_por_año:
            resultados = resultados_por_año[año]
            
            with columnas[i]:
                st.markdown(f"### 🗳️ {año}")
                
                # Métricas principales
                st.metric("Total de Casillas", f"{resultados['num_casillas']:,}")
                st.metric("Lista Nominal", f"{int(resultados['lista_nominal']):,}")
                st.metric("Total de Votos", f"{int(resultados['total_votos']):,}")
                st.metric("Participación", f"{resultados['porcentaje_participacion']}%")
                
                # Ganadores
                st.markdown("**🏆 Ganadores:**")
                if resultados['ganador_coalicion']:
                    # Obtener porcentaje del ganador por coalición
                    if len(resultados['coaliciones']) > 0:
                        porcentaje_ganador_coal = resultados['coaliciones'].iloc[0]['Porcentaje']
                        st.markdown(f"**Coalición:** {resultados['ganador_coalicion']} ({porcentaje_ganador_coal}%)")
                    else:
                        st.markdown(f"**Coalición:** {resultados['ganador_coalicion']}")
                
                if resultados['ganador_partido']:
                    # Obtener porcentaje del ganador por partido
                    if len(resultados['partidos']) > 0:
                        porcentaje_ganador_part = resultados['partidos'].iloc[0]['Porcentaje']
                        st.markdown(f"**Partido:** {resultados['ganador_partido']} ({porcentaje_ganador_part}%)")
                    else:
                        st.markdown(f"**Partido:** {resultados['ganador_partido']}")

    # ===== SECCIÓN DE TABLAS DETALLADAS =====
    st.divider()
    st.subheader("📋 Resultados Detallados por Proceso Electoral")
    
    for año in años_disponibles:
        if año in resultados_por_año:
            resultados = resultados_por_año[año]
            
            st.write(f"### 🗳️ Proceso Electoral: {año}")
            
            # Crear tabs para las diferentes tablas
            tab1, tab2, tab3 = st.tabs(["🤝 Resultados por Coalición", "🏛️ Resultados por Partido", "📋 Otros Votos"])
            
            with tab1:
                if len(resultados['coaliciones']) > 0:
                    df_coaliciones_display = resultados['coaliciones'][["Coalicion", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_coaliciones_display.columns = ["Coalición", "Votos", "Porcentaje"]
                    mostrar_tabla_grande(df_coaliciones_display, ["Coalición", "Votos", "Porcentaje"])
                else:
                    st.info("No hay coaliciones registradas para este año")
            
            with tab2:
                if len(resultados['partidos']) > 0:
                    df_partidos_display = resultados['partidos'][["Partido", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_partidos_display.columns = ["Partido", "Votos", "Porcentaje"]
                    mostrar_tabla_grande(df_partidos_display, ["Partido", "Votos", "Porcentaje"])
                else:
                    st.info("No hay partidos registrados para este año")
            
            with tab3:
                st.write("**Votos Nulos y No Registrados:** Votos que no van a ningún candidato")
                if len(resultados['otros']) > 0:
                    df_otros_display = resultados['otros'][["Otros", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_otros_display.columns = ["Tipo", "Votos", "Porcentaje"]
                    mostrar_tabla_grande(df_otros_display, ["Tipo", "Votos", "Porcentaje"])
                else:
                    st.info("No hay otros tipos de votos registrados para este año")
            
            # Separador entre años
            if año != años_disponibles[-1]:
                st.divider()

    # ===== RESTO DEL CÓDIGO SIGUE IGUAL =====
    # (Botones de acción, gráficos, etc.)

    # --- Botones de acción --- 
    st.subheader("📄 Acciones")
    col1, col2, col3 = st.columns(3) 
    
    # --- Variables de estado para gráficos ---
    if "mostrar_graficos" not in st.session_state:
        st.session_state.mostrar_graficos = False

    partido_colors = {
        "PAN": "#005DA4",
        "PRI": "#006847",
        "PRD": "#FFD700",
        "MORENA": "#A01916",
        "PT": "#FF0000",
        "PVEM": "#006D3C",
        "MC": "#F58025",
        "Movimiento Ciudadano": "#F58025",
        "NUEVA ALIANZA": "#00C0F3",
        "Encuentro Social": "#8E44AD",
        "Candidato Independiente": "#7F8C8D",
        "Candidato Independiente 1": "#95A5A6",
        "Candidato Independiente 2": "#BDC3C7",
    }

    coalicion_colors = {
        "Coalición PAN-PRI-PRD": "PAN",
        "Coalición PAN-PRD-MC": "PAN",
        "Coalición PRI-PVEM-NA": "PRI",
        "Coalición MORENA-PT-PVEM": "MORENA",
        "Coalición MORENA-PT-PES": "MORENA",
        "Movimiento Ciudadano": "Movimiento Ciudadano",
        "Candidato Independiente": "Candidato Independiente",
        "Candidato Independiente 1": "Candidato Independiente 1",
        "Candidato Independiente 2": "Candidato Independiente 2",
    }
    
    with col1: 
        if st.session_state.mostrar_graficos:
            if st.button("📊  Ocultar Gráficos"):
                st.session_state.mostrar_graficos = False
                st.rerun()
        else:
            if st.button("📊 Ver Gráficos"):
                st.session_state.mostrar_graficos = True
                st.rerun()
    
    with col2: 
        if st.button("🖨️ Imprimir"): 
            st.info("Usa Ctrl+P o Cmd+P para imprimir esta vista en PDF o papel.") 
    
    with col3: 
        def create_pdf_multi_año(resultados_por_año): 
            buffer = BytesIO() 
            doc = SimpleDocTemplate(buffer, topMargin=0.5*inch, bottomMargin=0.5*inch) 
            styles = getSampleStyleSheet() 
            story = [] 
            
            # Título principal
            story.append(Paragraph("Resultados Electorales", styles["Title"])) 
            story.append(Spacer(1, 0.3*inch))
            
            # Información general
            story.append(Paragraph(f"<b>Estado:</b> {estado_sel}", styles["Normal"])) 
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Distrito:</b> {distrito_display}", styles["Normal"])) 
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Municipio:</b> {municipio_display}", styles["Normal"])) 
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph(f"<b>Sección:</b> {seccion_display}", styles["Normal"])) 
            story.append(Spacer(1, 0.3*inch))
            
            # Resultados por año en orden: 2024, 2021, 2018
            años_ordenados = sorted(resultados_por_año.keys(), reverse=True)
            
            for i, año in enumerate(años_ordenados):
                resultados = resultados_por_año[año]
                story.append(Paragraph(f"Proceso Electoral: {año}", styles["Heading1"]))
                story.append(Spacer(1, 0.2*inch))
                
                # Métricas del año
                story.append(Paragraph("Resumen", styles["Heading2"]))
                story.append(Spacer(1, 0.1*inch))
                story.append(Paragraph(f"• Total de Casillas: {resultados['num_casillas']:,}", styles["Normal"])) 
                story.append(Paragraph(f"• Lista Nominal: {int(resultados['lista_nominal']):,}", styles["Normal"])) 
                story.append(Paragraph(f"• Total de Votos: {int(resultados['total_votos']):,}", styles["Normal"])) 
                story.append(Paragraph(f"• Participación: {resultados['porcentaje_participacion']}%", styles["Normal"])) 
                story.append(Spacer(1, 0.2*inch))
                
                # Tabla de coaliciones
                if len(resultados['coaliciones']) > 0:
                    story.append(Paragraph("Resultados por Coalición", styles["Heading2"]))
                    story.append(Spacer(1, 0.1*inch))
                    
                    df_coaliciones_display = resultados['coaliciones'][["Coalicion", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_coaliciones_display.columns = ["Coalición", "Votos", "Porcentaje"]
                    
                    table_data = [list(df_coaliciones_display.columns)] + df_coaliciones_display.values.tolist() 
                    table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                    table.setStyle(TableStyle([ 
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke), 
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.beige, colors.white]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ])) 
                    story.append(table)
                    story.append(Spacer(1, 0.2*inch))
                
                # Tabla de partidos
                if len(resultados['partidos']) > 0:
                    story.append(Paragraph("Resultados por Partido Individual", styles["Heading2"]))
                    story.append(Spacer(1, 0.1*inch))
                    
                    df_partidos_display = resultados['partidos'][["Partido", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_partidos_display.columns = ["Partido", "Votos", "Porcentaje"]
                    
                    table_data = [list(df_partidos_display.columns)] + df_partidos_display.values.tolist() 
                    table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                    table.setStyle(TableStyle([ 
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke), 
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.beige, colors.white]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ])) 
                    story.append(table)
                    story.append(Spacer(1, 0.2*inch))
                
                # Tabla de otros votos
                if len(resultados['otros']) > 0:
                    story.append(Paragraph("Otros Votos", styles["Heading2"]))
                    story.append(Spacer(1, 0.1*inch))
                    
                    df_otros_display = resultados['otros'][["Otros", "Votos_Formatted", "Porcentaje_Formatted"]].copy()
                    df_otros_display.columns = ["Tipo", "Votos", "Porcentaje"]
                    
                    table_data = [list(df_otros_display.columns)] + df_otros_display.values.tolist() 
                    table = Table(table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
                    table.setStyle(TableStyle([ 
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke), 
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("FONTSIZE", (0, 1), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.beige, colors.white]),
                        ("LEFTPADDING", (0, 0), (-1, -1), 12),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ])) 
                    story.append(table)
                
                # Separador entre años (excepto el último)
                if i < len(años_ordenados) - 1:
                    story.append(Spacer(1, 0.5*inch))
                    story.append(Paragraph("-" * 80, styles["Normal"]))
                    story.append(Spacer(1, 0.5*inch))
            
            doc.build(story) 
            buffer.seek(0) 
            return buffer 
        
        # Generar nombre del archivo con jerarquía correcta
        estado_clean = estado_sel.replace('/', '_').replace(' ', '_')
        distrito_clean = distrito_sel.replace('/', '_').replace(' ', '_').replace('-', '_')
        municipio_clean = municipio_sel.replace('/', '_').replace(' ', '_') if municipio_sel != "Todos" else "Todos"
        archivo_nombre = f"resultados_electorales_{estado_clean}_{distrito_clean}_{municipio_clean}_{seccion_sel}.pdf"

        # Botón de descarga directo
        st.download_button(
            label="📥 Descargar PDF Completo",
            data=create_pdf_multi_año(resultados_por_año),
            file_name=archivo_nombre,
            mime="application/pdf",
            help="Descarga PDF con todos los años disponibles"
        )
    
    # Mostrar gráficos si están activados
    if st.session_state.mostrar_graficos:
        st.divider()
        st.subheader("📊 Visualizaciones Comparativas")
        
        # Gráficos por año en orden: 2024, 2021, 2018
        for año in años_disponibles:
            if año in resultados_por_año:
                st.write(f"### Gráficos - Proceso Electoral {año}")
                resultados = resultados_por_año[año]
                
                # Crear tabs para gráficos
                tab1, tab2, tab3 = st.tabs(["🤝 Coaliciones", "🏛️ Partidos", "📋 Otros"])
                
                with tab1:
                    if len(resultados['coaliciones']) > 0:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig, ax = plt.subplots(figsize=(16, 12))  # Más grande
                            colors_barras = [
                                partido_colors.get(coalicion_colors.get(c, ""), "gray")
                                for c in resultados['coaliciones']["Coalicion"]
                            ]
                            bars = ax.bar(resultados['coaliciones']["Coalicion"], resultados['coaliciones']["Votos"], color=colors_barras)
                            
                            # Configurar texto MÁS grande
                            ax.tick_params(axis='x', labelsize=20, rotation=45)
                            ax.tick_params(axis='y', labelsize=20)
                            ax.set_title(f"Resultados Electorales - {año}", fontsize=26, fontweight='bold', pad=25)
                            ax.set_xlabel("Coalición", fontsize=22, fontweight='bold')
                            ax.set_ylabel("Número de Votos", fontsize=22, fontweight='bold')
                            
                            # Agregar valores en las barras con texto más grande
                            for bar in bars:
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(height):,}',
                                       ha='center', va='bottom', fontsize=18, fontweight='bold')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        with col2:
                            fig2, ax2 = plt.subplots(figsize=(14, 14))  # Más grande
                            colors_pie = [
                                partido_colors.get(coalicion_colors.get(c, ""), "gray")
                                for c in resultados['coaliciones']["Coalicion"]
                            ]
                            
                            # Crear etiquetas más cortas para el pie
                            labels_cortas = [label.replace("Coalición ", "").replace("Movimiento Ciudadano", "MC") 
                                           for label in resultados['coaliciones']["Coalicion"]]
                            
                            wedges, texts, autotexts = ax2.pie(
                                resultados['coaliciones']["Votos"], 
                                labels=labels_cortas,
                                autopct='%1.1f%%', 
                                colors=colors_pie, 
                                startangle=90,
                                textprops={'fontsize': 20}  # Texto MÁS grande
                            )
                            
                            # Hacer texto de porcentajes más grande y visible
                            for autotext in autotexts:
                                autotext.set_color('white')
                                autotext.set_fontsize(20)
                                autotext.set_weight('bold')
                            
                            # Hacer etiquetas más grandes
                            for text in texts:
                                text.set_fontsize(20)
                                text.set_weight('bold')
                            
                            ax2.set_title(f"Distribución Electoral - {año}", fontsize=26, fontweight='bold', pad=25)
                            st.pyplot(fig2)
                    else:
                        st.info("No hay datos de coaliciones para graficar")
                
                with tab2:
                    if len(resultados['partidos']) > 0:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig, ax = plt.subplots(figsize=(16, 12))  # Más grande
                            colors_barras = [partido_colors.get(p, "gray") for p in resultados['partidos']["Partido"]]
                            bars = ax.bar(resultados['partidos']["Partido"], resultados['partidos']["Votos"], color=colors_barras)
                            
                            # Configurar texto MÁS grande
                            ax.tick_params(axis='x', labelsize=20, rotation=45)
                            ax.tick_params(axis='y', labelsize=20)
                            ax.set_title(f"Poder por Partido - {año}", fontsize=26, fontweight='bold', pad=25)
                            ax.set_xlabel("Partido", fontsize=22, fontweight='bold')
                            ax.set_ylabel("Número de Votos", fontsize=22, fontweight='bold')
                            
                            # Agregar valores en las barras con texto más grande
                            for bar in bars:
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(height):,}',
                                       ha='center', va='bottom', fontsize=18, fontweight='bold')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        with col2:
                            fig2, ax2 = plt.subplots(figsize=(14, 14))  # Más grande
                            colors_pie = [partido_colors.get(c, "gray") for c in resultados['partidos']["Partido"]]
                            
                            # Crear etiquetas más cortas para el pie
                            labels_cortas = [label.replace("Movimiento Ciudadano", "MC").replace("Nueva Alianza", "NA").replace("Encuentro Social", "PES") 
                                           for label in resultados['partidos']["Partido"]]
                            
                            wedges, texts, autotexts = ax2.pie(
                                resultados['partidos']["Votos"], 
                                labels=labels_cortas, 
                                autopct='%1.1f%%', 
                                colors=colors_pie, 
                                startangle=90,
                                textprops={'fontsize': 20}  # Texto MÁS grande
                            )
                            
                            # Hacer texto de porcentajes más grande y visible
                            for autotext in autotexts:
                                autotext.set_color('white')
                                autotext.set_fontsize(20)
                                autotext.set_weight('bold')
                            
                            # Hacer etiquetas más grandes
                            for text in texts:
                                text.set_fontsize(20)
                                text.set_weight('bold')
                            
                            ax2.set_title(f"Distribución de Poder - {año}", fontsize=26, fontweight='bold', pad=25)
                            st.pyplot(fig2)
                    else:
                        st.info("No hay partidos para graficar")
                
                with tab3:
                    if len(resultados['otros']) > 0:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig, ax = plt.subplots(figsize=(14, 10))  # Más grande
                            bars = ax.bar(resultados['otros']["Otros"], resultados['otros']["Votos"], color='orange')
                            
                            # Configurar texto MÁS grande
                            ax.tick_params(axis='x', labelsize=20, rotation=45)
                            ax.tick_params(axis='y', labelsize=20)
                            ax.set_title(f"Otros Votos - {año}", fontsize=26, fontweight='bold', pad=25)
                            ax.set_xlabel("Tipo", fontsize=22, fontweight='bold')
                            ax.set_ylabel("Número de Votos", fontsize=22, fontweight='bold')
                            
                            # Agregar valores en las barras con texto más grande
                            for bar in bars:
                                height = bar.get_height()
                                ax.text(bar.get_x() + bar.get_width()/2., height,
                                       f'{int(height):,}',
                                       ha='center', va='bottom', fontsize=18, fontweight='bold')
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                        
                        with col2:
                            fig2, ax2 = plt.subplots(figsize=(12, 12))  # Más grande
                            colors_pie = plt.cm.Set3(range(len(resultados['otros'])))
                            wedges, texts, autotexts = ax2.pie(
                                resultados['otros']["Votos"], 
                                labels=resultados['otros']["Otros"], 
                                autopct='%1.1f%%', 
                                colors=colors_pie, 
                                startangle=90,
                                textprops={'fontsize': 20}  # Texto MÁS grande
                            )
                            
                            # Hacer texto de porcentajes más grande y visible
                            for autotext in autotexts:
                                autotext.set_color('white')
                                autotext.set_fontsize(20)
                                autotext.set_weight('bold')
                            
                            # Hacer etiquetas más grandes
                            for text in texts:
                                text.set_fontsize(20)
                                text.set_weight('bold')
                            
                            ax2.set_title(f"Distribución Otros Votos - {año}", fontsize=26, fontweight='bold', pad=25)
                            st.pyplot(fig2)
                    else:
                        st.info("No hay otros tipos de votos para graficar")
                
                if año != años_disponibles[-1]:
                    st.divider()

else:
    st.warning("No se encontraron datos para los filtros seleccionados.")
    st.write("Información de debug:")
    st.write(f"Estado seleccionado: {estado_sel}")
    st.write(f"Distrito seleccionado: {distrito_sel}")
    st.write(f"Sección seleccionada: {seccion_sel}")
    if len(df_distrito) > 0:
        st.write(f"Secciones disponibles: {sorted(df_distrito['SECCION'].unique())}")