import pandas as pd
import streamlit as st

st.set_page_config(page_title="Costos Gel", layout="wide")

st.title("🧪 Dashboard Costos Gel Neutro")

# === CAMBIAR POR TU REPO RAW ===
URL = "https://raw.githubusercontent.com/franciscosalusso-ux/gel-costos/main/historial_precios.csv"
df = pd.read_csv(URL, parse_dates=["fecha"])

# ---------------- PRECIOS ACTUALES ----------------
st.header("📊 Precios actuales")

df_latest = df.sort_values("fecha").groupby("Product").tail(1)
st.dataframe(df_latest)

# ---- Costo por pote ----
if "COSTO_POTE" in df_latest["Product"].values:
    costo_pote = df_latest[df_latest["Product"]=="COSTO_POTE"]["Price"].values[0]
    st.metric("💰 Costo insumos por pote (sin envase)", f"${costo_pote:,.2f}")
else:
    st.warning("⚠️ Todavía no se calculó COSTO_POTE")

# ---------------- GRAFICOS ----------------
st.header("📈 Evolución de precios")

pivot = df.pivot(index="fecha", columns="Product", values="Price")
st.line_chart(pivot)

# ---------------- GRAFICO COSTO POTE ----------------
if "COSTO_POTE" in df["Product"].values:
    st.subheader("📉 Evolución costo por pote")
    data_pote = df[df["Product"]=="COSTO_POTE"].set_index("fecha")["Price"]
    st.line_chart(data_pote)
