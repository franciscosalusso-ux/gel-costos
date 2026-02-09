import pandas as pd
import streamlit as st

st.set_page_config(page_title="🧪 Dashboard Costos Gel", layout="wide")
st.title("🧪 Dashboard Costos Gel Neutro")

# ---------------- CARGAR DATOS ----------------
df = pd.read_csv("historial_precios.csv", parse_dates=["fecha"])

# ---------------- PRECIOS ACTUALES ----------------
st.header("📊 Precios actuales")

df_latest = df.sort_values("fecha").groupby("Product").tail(1)
st.dataframe(df_latest)

# Mostrar costo por pote destacado
costo_pote = df_latest[df_latest["Product"] == "COSTO_POTE"]["Price"].values
if len(costo_pote) > 0:
    st.metric("💰 Costo insumos por pote (sin envase)", f"${costo_pote[0]:.2f}")

# ---------------- GRAFICOS HISTORICOS ----------------
st.header("📈 Evolución de precios")

productos = df["Product"].unique()

for prod in productos:
    data = df[df["Product"] == prod]
    st.subheader(prod)
    st.line_chart(data.set_index("fecha")["Price"])

# ---------------- TABLA PIVOT ----------------
st.header("📊 Historial de precios (pivot)")
pivot = df.pivot_table(index="fecha", columns="Product", values="Price")
st.dataframe(pivot)
