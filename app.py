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

# Cambiar el nombre de COSTO_POTE para mostrarlo bonito
df_latest_display = df_latest.copy()
df_latest_display["Product"] = df_latest_display["Product"].replace(
    {"COSTO_POTE": "Costo insumos para un pote sin plástico"}
)

# Guardar la fecha para mostrarla debajo
ultima_fecha = df_latest["fecha"].max()

# Mostrar tabla con Product y Price
st.dataframe(df_latest_display[["Product", "Price"]].reset_index(drop=True), use_container_width=True)

# Mostrar la fecha debajo
st.markdown(f"**Última actualización:** {ultima_fecha.date()}")

# ---------------- GRAFICO HISTORICO COSTO POTE ----------------
st.header("📈 Histórico de costo insumos para un pote sin plástico")

# Filtrar solo los registros de COSTO_POTE y ordenar por fecha
costo_pote_df = df[df["Product"] == "COSTO_POTE"].sort_values("fecha")

if not costo_pote_df.empty:
    # Crear DataFrame con fecha como índice y Price como valor
    historial_df = costo_pote_df.set_index("fecha")[["Price"]].rename(columns={"Price": "Costo_insumos_pote"})
    
    # Graficar
    st.line_chart(historial_df)
else:
    st.write("No hay datos históricos de COSTO_POTE para mostrar")

