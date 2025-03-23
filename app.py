
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="App Bolsa", layout="wide")
st.title("App Bolsa - NYSE, España, EuroStoxx y ETFs")

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'WMT', 'UNH', 'KO', 'PEP', 'V', 'BAC', 'HD', 'DIS', 'MA', 'PYPL', 'INTC', 'IBM', 'CSCO', 'ORCL', 'NFLX', 'T', 'CVX', 'PFE', 'XOM', 'C', 'MCD', 'BA', 'ABT', 'CRM', 'MRK', 'QCOM', 'NKE', 'SAN.MC', 'BBVA.MC', 'ITX.MC', 'IBE.MC', 'REP.MC', 'AMS.MC', 'ANA.MC', 'CABK.MC', 'CLNX.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IAG.MC', 'MAP.MC', 'TEF.MC', 'ACX.MC', 'AENA.MC', 'ALM.MC', 'BKT.MC', 'COL.MC', 'ELE.MC', 'ENC.MC', 'EQT.MC', 'FCC.MC', 'LOG.MC', 'MEL.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'R4.MC', 'SAB.MC', 'SGRE.MC', 'SPS.MC', 'VIS.MC', 'ZOT.MC', 'AIR.PA', 'ADS.DE', 'ALV.DE', 'BN.PA', 'ENEL.MI', 'ENGI.PA', 'OR.PA', 'SAP.DE', 'SIE.DE', 'SU.PA', 'TTE.PA', 'VOW3.DE', 'DTE.DE', 'DPW.DE', 'BAS.DE', 'BAYN.DE', 'BMW.DE', 'CRH.L', 'DAI.DE', 'KER.PA', 'LVMH.PA', 'MC.PA', 'MT.AS', 'PHIA.AS', 'RWE.DE', 'SGO.PA', 'URW.AS', 'ZAL.DE', 'ATCO-A.ST', 'HEIA.AS', 'IFX.DE', 'LIN.DE', 'UCG.MI', 'STLA.MI', 'ENI.MI', 'SPY', 'QQQ', 'DIA', 'VTI', 'IWM', 'EFA', 'EEM', 'VNQ', 'LQD', 'HYG', 'XLF', 'XLK', 'XLE', 'XLY', 'XLV', 'XLI', 'XLB', 'XLC', 'XLRE', 'ARKK', 'ARKW', 'ARKF', 'ARKG', 'ARKQ', 'ARKX', 'SOXX', 'SMH', 'IBB', 'VHT', 'IYZ', 'XRT', 'XHB', 'XME', 'ITA', 'IYT']

@st.cache_data(ttl=3600)
def obtener_datos(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="90d")
            info = stock.info
            if len(hist) >= 7:
                hoy = (hist["Close"][-1] - hist["Open"][-1]) / hist["Open"][-1] * 100
                semana = (hist["Close"][-1] - hist["Close"][-6]) / hist["Close"][-6] * 100
                ytd = (hist["Close"][-1] - hist["Close"][0]) / hist["Close"][0] * 100
                data.append({
                    "Ticker": ticker,
                    "Nombre": info.get("shortName", ""),
                    "Cambio Día (%)": round(hoy, 2),
                    "Cambio Semana (%)": round(semana, 2),
                    "Cambio YTD (%)": round(ytd, 2)
                })
        except:
            continue
    return pd.DataFrame(data)

df = obtener_datos(tickers)

if not df.empty:
    st.subheader("📈 Datos Generales")
    st.dataframe(df, use_container_width=True)

# --- Gráfico por ticker con medias móviles y volumen ---
if not df.empty:
    st.subheader("📊 Evolución del precio con medias móviles y volumen")
    seleccion = st.selectbox("Selecciona un ticker:", df["Ticker"])
    if seleccion:
        hist = yf.Ticker(seleccion).history(period="1y")
        hist["Media 50"] = hist["Close"].rolling(50).mean()
        hist["Media 200"] = hist["Close"].rolling(200).mean()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
        hist[["Close", "Media 50", "Media 200"]].plot(ax=ax1)
        ax1.set_ylabel("Precio")
        ax1.set_title(f"Evolución de {seleccion}")

        hist["Volume"].plot(kind="bar", ax=ax2, color="gray")
        ax2.set_ylabel("Volumen")
        ax2.set_xlabel("Fecha")

        st.pyplot(fig)
