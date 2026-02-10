import pandas as pd
import streamlit as st

st.title("🧪 Dashboard Costos Gel Neutro")

# Cargar historial
df = pd.read_csv("historial_precios.csv", parse_dates=["fecha"])

# ---------------- PRECIOS ACTUALES ----------------
st.header("📊 Precios actuales")

# Tomar último registro por producto
df_latest = df.sort_values("fecha").groupby("Product").tail(1)

# Guardar la fecha para mostrarla debajo
ultima_fecha = df_latest["fecha"].max()

# Mostrar solo Product y Price, sin índice
st.dataframe(df_latest[["Product", "Price"]], use_container_width=True)

# Mostrar la fecha debajo
st.markdown(f"**Última actualización:** {ultima_fecha.date()}")

# Mostrar costo por pote sin plástico (si existe)
if "COSTO_POTE" in df_latest["Product"].values:
    costo_pote = df_latest[df_latest["Product"] == "COSTO_POTE"]["Price"].values[0]
    st.metric("💰 Costo pote sin plástico (sin envase)", f"${costo_pote:.2f}")

# ---------------- GRAFICOS ----------------
st.header("📈 Evolución de precios")
productos = df["Product"].unique()

for prod in productos:
    data = df[df["Product"] == prod].sort_values("fecha")
    st.subheader(prod)
    
    # Verificar que haya datos válidos
    if not data.empty:
        data_chart = data.set_index("fecha")["Price"].dropna()
        st.line_chart(data_chart)
    else:
        st.write("No hay datos para mostrar")


