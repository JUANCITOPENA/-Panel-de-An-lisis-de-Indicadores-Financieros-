import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt

# Configuración inicial de Streamlit
st.set_page_config(
    page_title="Indicadores Bursátiles",
    layout="wide"
)

# Título de la app
st.title("📈 Aplicación de Indicadores Bursátiles")

# Función para crear el DataFrame de indicadores
def create_indicators_dataframe():
    data = {
        'Codigo': list(range(1, 25)),
        'Descripcion de Indicadores': [
            'SMART SCORE TIP RANKS', '52 WEEK HIGH / CURRENT PRICE', 
            'VOLUME', 'CURRENT PRICE', 'NOTICIAS ECONOMICAS Y FINANCIERAS',
            'OPERATING MARGIN', 'EPS', 'VOLUME AVERAGE', 'QUANT RATING',
            'PRICE/OPERATING CASH FLOW', 'PE RATIO ALPHA', 
            'LAST EARNINGS CALL CELL PHONE', 'BETA TIP RANKS', 
            'EMA TRADING VIEW', 'FORWARD PE', 'TRAILING PE', 
            'LAST 4 QUARTER EARNINGS SURPRISE', 'FREE CASH FLOW / MARGIN', 
            'CASH RATIO', '10 DAY CHANGE', 'EARNING REVISIONS', 
            '30 DAY CHANGE', 'AFTERHOURS PERFORMANCE', 'RATINGS SEEKING ALPHA'
        ],
        'FECHA EV.': [''] * 24,
        'SCORE': [
            6.0, 0.250, 139.00, 156.00, 4, 4.17, 0.34, 29.00, 237.00, 
            131.00, 186.00, 3.00, 2.00, 155.71, 28.24, 185.99, 4.00, 
            39, 0.52, 1, 1.22, 17, -3.42, 3.79
        ],
        'STATUS': [
            'REGULAR', 'EXCELENTE', 'EXCELENTE', 'BUENO', 'REGULAR', 
            'MALO', 'BUENO', 'BUENO', 'EXCELENTE', 'EXCELENTE', 
            'EXCELENTE', 'BUENO', 'EXCELENTE', 'REGULAR', 'EXCELENTE', 
            'MALO', 'EXCELENTE', 'BUENO', 'BUENO', 'MALO', 
            'REGULAR', 'BUENO', 'MALO', 'BUENO'
        ]
    }
    return pd.DataFrame(data)

# Función para colorear las celdas según el status
def color_status(val):
    color_map = {
        'EXCELENTE': 'background-color: green',
        'BUENO': 'background-color: lightgreen',
        'REGULAR': 'background-color: yellow',
        'MALO': 'background-color: red'
    }
    return color_map.get(val, '')

# Definir índices principales
indices = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT",
    "FTSE 100": "^FTSE",
    "DAX": "^GDAXI",
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "Shanghai Comp": "000001.SS",
    "Euro Stoxx 50": "^STOXX50E",
    "CAC 40": "^FCHI",
    "S&P/TSX Comp": "^GSPTSE",
    "IBEX 35": "^IBEX",
    "Swiss MI": "^SSMI",
    "ASX 200": "^AXJO",
    "KOSPI": "^KS11",
    "MOEX Russia": "IMOEX.ME",
    "Bovespa": "^BVSP",
    "IPC Mexico": "^MXX",
    "Nifty 50": "^NSEI",
    "SENSEX": "^BSESN",
    "FTSE MIB": "FTSEMIB.MI",
    "AEX": "^AEX",
    "BEL 20": "^BFX",
    "OMX Stockholm 30": "^OMX",
    "TA-35": "^TA35.TA",
    "WIG20": "WIG20.WA",
    "S&P/NZX 50": "^NZ50",
    "Straits Times": "^STI",
    "FTSE/JSE Top 40": "^JN0U.JO",
    
    # Empresas tecnológicas importantes
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Alphabet (Google)": "GOOGL",
    "Meta (Facebook)": "META",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    
    # Otras empresas importantes
    "Berkshire Hathaway": "BRK-A",
    "JPMorgan Chase": "JPM",
    "Johnson & Johnson": "JNJ",
    "Visa": "V",
    "Walmart": "WMT",
    "Procter & Gamble": "PG",
    
    # Empresas internacionales
    "Samsung": "005930.KS",
    "Toyota": "TM",
    "ASML Holding": "ASML",
    "Taiwan Semiconductor": "TSM",
    "Tencent": "0700.HK",
    "Alibaba": "BABA",
    
    # Índices adicionales
    "Nifty 50 (India)": "^NSEI",
    "CAC 40 (Francia)": "^FCHI",
    "IBEX 35 (España)": "^IBEX",
    "ASX 200 (Australia)": "^AXJO"
}

# Sidebar de parámetros
st.sidebar.header("Parámetros de Visualización")
select_all = st.sidebar.checkbox("Seleccionar todos los índices")
selected_indices = st.sidebar.multiselect(
    "Selecciona índices bursátiles", 
    list(indices.keys()), 
    default=list(indices.keys()) if select_all else ["S&P 500", "Dow Jones", "Apple", "Microsoft","Alibaba"]
)

# Selección de rango de fechas
date_option = st.sidebar.radio(
    "Selecciona el rango de tiempo",
    ("1 Día", "1 Semana", "1 Mes", "3 Meses", "6 Meses", "1 Año", "YTD (Año en curso)"),
    index=1  # Esto asegura que el valor predeterminado sea "1 Semana" (índice 1)
)

today = dt.date.today()
start_date = {
    "1 Día": today - dt.timedelta(days=1),
    "1 Semana": today - dt.timedelta(weeks=1),
    "1 Mes": today - dt.timedelta(days=30),
    "3 Meses": today - dt.timedelta(days=90),
    "6 Meses": today - dt.timedelta(days=180),
    "1 Año": today - dt.timedelta(days=365),
    "YTD (Año en curso)": dt.date(today.year, 1, 1)
}[date_option]

# Mostrar la fecha de inicio seleccionada
st.write(f"Fecha de inicio seleccionada: {start_date}")



# Función para generar narrativas de los indicadores con emojis y enumeración
def generate_narratives(indicators_df):
    narratives = []
    for idx, row in indicators_df.iterrows():
        # Emojis alusivos según el estado del indicador
        if row['STATUS'] == 'EXCELENTE':
            emoji = "🚀📈"
        elif row['STATUS'] == 'BUENO':
            emoji = "👍📊"
        elif row['STATUS'] == 'REGULAR':
            emoji = "⚠️📉"
        else:
            emoji = "🔴❌"
        
        # Construcción de la narrativa
        narrative = f"{idx + 1}. **Indicador**: '{row['Descripcion de Indicadores']}'\n"
        narrative += f"   **Valor**: {row['SCORE']}\n"
        narrative += f"   **Estado**: '{row['STATUS']}' {emoji}\n"
        
        # Añadiendo el análisis según el estado
        if row['STATUS'] == 'EXCELENTE':
            narrative += "   🚀 Esto indica una tendencia positiva, es un excelente momento para considerar la inversión en este índice.\n"
        elif row['STATUS'] == 'BUENO':
            narrative += "   👍 Aunque la tendencia es positiva, podría haber oportunidades aún mejores en otros indicadores.\n"
        elif row['STATUS'] == 'REGULAR':
            narrative += "   ⚠️ La tendencia es moderada, y se recomienda monitorear este indicador más de cerca antes de tomar decisiones de inversión.\n"
        else:
            narrative += "   🔴 El indicador está en una zona negativa, lo cual indica precaución antes de invertir.\n"
        
        narratives.append(narrative)
    return narratives


# Validar selección de índices
if not selected_indices:
    st.error("Por favor selecciona al menos un índice")
else:
    for index_name in selected_indices:
        st.subheader(f"Análisis del índice {index_name}")
        ticker = indices[index_name]
        data = yf.download(ticker, start=start_date, end=today)
        
        if data.empty:
            st.warning(f"No se encontraron datos para {index_name}")
            continue
        
        # Mostrar datos
        st.write("Datos más recientes")
        st.dataframe(data.tail(30))
        
        # Gráfica
        st.line_chart(data['Close'])
        
         # Indicadores
        st.header("📊 Indicadores")
        indicators_df = create_indicators_dataframe()
        st.dataframe(indicators_df.style.applymap(color_status, subset=['STATUS']))
        
        # Narrativas
        st.header("📜 Narrativas de los Indicadores")
        narratives = generate_narratives(indicators_df)
        for narrative in narratives:
            st.write(narrative)
