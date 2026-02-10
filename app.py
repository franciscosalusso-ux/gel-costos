import pandas as pd
import streamlit as st

st.title("🧪 Dashboard Costos Gel Neutro")

# ---------------- CARGA DE DATOS ----------------
df = pd.read_csv("historial_precios.csv")

# Quitar espacios en los nombres de productos
df["Product"] = df["Product"].str.strip()

# Asegurarse de que Price sea numérico
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# Asegurarse de que fecha sea datetime
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

# ---------------- PRECIOS ACTUALES ----------------
st.header("📊 Precios actuales")

# Tomar último registro por producto
df_latest = df.sort_values("fecha").groupby("Product", as_index=False).tail(1)

# Cambiar el nombre de COSTO_POTE
df_latest_display = df_latest.copy()
df_latest_display["Product"] = df_latest_display["Product"].replace(
    {"COSTO_POTE": "Costo insumos para un pote sin plástico"}
)

# Guardar la fecha para mostrarla debajo
ultima_fecha = df_latest["fecha"].max()

# Mostrar solo Product y Price sin índice
st.dataframe(df_latest_display[["Product", "Price"]].reset_index(drop=True), use_container_width=True)

# Mostrar la fecha debajo
st.markdown(f"**Última actualización:** {ultima_fecha.date()}")

# Mostrar costo de pote sin plástico si existe
if "COSTO_POTE" in df_latest["Product"].values:
    costo_pote = df_latest.loc[df_latest["Product"] == "COSTO_POTE", "Price"].values[0]
    st.metric("💰 Costo insumos para un pote sin plástico", f"${costo_pote:.2f}")

# ---------------- GRAFICOS ----------------
st.header("📈 Evolución de precios")

# Filtrar todos los productos, incluyendo COSTO_POTE
productos = df["Product"].unique()

for prod in productos:
    data = df[df["Product"] == prod].sort_values("fecha")
    
    # Cambiar nombre para mostrar en gráfico si es COSTO_POTE
    prod_displ_

