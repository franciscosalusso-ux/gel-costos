import pandas as pd
import streamlit as st

st.set_page_config(page_title="🧪 Dashboard Costos Gel Neutro", layout="wide")
st.title("🧪 Dashboard Costos Gel Neutro")

# ---------- CARGAR HISTORIAL ----------
df = pd.read_csv("historial_precios.csv", parse_dates=["fecha"])

# ---------- PRECIOS ACTUALES ----------
st.header("📊 Precios actuales")

# Tomar último registro por producto
df_latest = df.sort_values("fecha").groupby("Product").tail(1)
st.dataframe(df_latest)

# ---------- COSTO POR POTE ----------
# Calculamos costo por pote según tu fórmula
df_latest_dict = df_latest.set_index("Product")["Price"].to_dict()

costo_pote = (
    df_latest_dict.get("Carbopol Acrypol 940", 0)/40 +
    df_latest_dict.get("Nipagin Metilparabeno", 0)/200 +
    df_latest_dict.get("Trietanolamina 85%", 0)/40 +
    df_latest_dict.get("Glicerina Refinada Alimenticia", 0)/40
)

st.metric("💰 Costo insumos por pote (sin envase)", f"${costo_pote:.2f}")

# ---------- GRAFICOS HISTORICOS ----------
st.header("📈 Evolución de precios")

# Pivot table para manejar duplicados
pivot = df.pivot_table(index="fecha", columns="Product", values="Price", aggfunc="mean")

for prod in pivot.columns:
    st.subheader(prod)
    st.line_chart(pivot[prod])

# Graficar evolución del costo por pote
st.subheader("💰 Evolución del costo insumos por pote")
# Calculamos costo por pote histórico
pivot["Costo por pote"] = (
    pivot.get("Carbopol Acrypol 940", 0)/40 +
    pivot.get("Nipagin Metilparabeno", 0)/200 +
    pivot.get("Trietanolamina 85%", 0)/40 +
    pivot.get("Glicerina Refinada Alimenticia", 0)/40
)
st.line_chart(pivot["Costo por pote"])
