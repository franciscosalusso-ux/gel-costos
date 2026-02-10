import pandas as pd
import streamlit as st

st.title("🧪 Dashboard Costos Gel Neutro")

# ---------------- CARGA DE DATOS ----------------
df = pd.read_csv("historial_precios.csv", parse_dates=["fecha"])

# Asegurarse de que Price sea numérico
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# ---------------- PRECIOS ACTUALES ----------------
st.header("📊 Precios actuales")

# Tomar último registro por producto
df_latest = df.sort_values("fecha").groupby("Product", as_index=False).tail(1)

# Guardar la fecha para mostrarla debajo
ultima_fecha = df_latest["fecha"].max()

# Mostrar solo Product y Price sin índice
st.dataframe(df_latest[["Product", "Price"]].reset_index(drop=True), use_container_width=True)

# Mostrar la fecha debajo
st.markdown(f"**Última actualización:** {ultima_fecha.date()}")

# Mostrar costo de pote sin plástico si existe
if "COSTO_POTE" in df_latest["Product"].values:
    costo_pote = df_latest.loc[df_latest["Product"] == "COSTO_POTE", "Price"].values[0]
    st.metric("💰 Costo de pote sin plástico (sin envase)", f"${costo_pote:.2f}")

# ---------------- GRAFICOS ----------------
st.header("📈 Evolución de precios")

# Filtrar solo productos que no sean el costo del pote
productos_insumos = [p for p in df["Product"].unique() if p != "COSTO_POTE"]

for prod in productos_insumos:
    data = df[df["Product"].str.strip() == prod].sort_values("fecha")
    
    st.subheader(prod)
    
    # Filtrar filas válidas y asegurarse de que fecha sea índice
    data_chart = data[["fecha", "Price"]].dropna().set_index("fecha")
    
    if not data_chart.empty:
        st.line_chart(data_chart)
    else:
        st.write("No hay datos para mostrar")



