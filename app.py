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

# Mostrar costo insumos para un pote si existe
if "COSTO_POTE" in df_latest["Product"].values:
    costo_pote = df_latest.loc[df_latest["Product"] == "COSTO_POTE", "Price"].values[0]
    st.metric("💰 Costo insumos para un pote sin plástico", f"${costo_pote:.2f}")

# ---------------- GRAFICO HISTORICO COSTO POTE ----------------
st.header("📈 Histórico de costo insumos para un pote sin plástico")

# Filtrar insumos (todos menos COSTO_POTE)
insumos = [p for p in df["Product"].unique() if p != "COSTO_POTE"]

# Filtrar solo los registros de COSTO_POTE
costo_pote_df = df[df["Product"] == "COSTO_POTE"].sort_values("fecha")

if not costo_pote_df.empty:
    historial_costos = []

    for fecha in costo_pote_df["fecha"]:
        # Para cada insumo, tomar el último precio conocido antes o en esa fecha
        costo_total = 0
        for insumo in insumos:
            insumo_data = df[(df["Product"] == insumo) & (df["fecha"].notna()) & (df["fecha"] <= fecha)]
            if not insumo_data.empty:
                ultimo_precio = insumo_data.sort_values("fecha").iloc[-1]["Price"]
                costo_total += ultimo_precio
            else:
                # Si no hay precio registrado nunca, asumimos 0
                costo_total += 0
        historial_costos.append({"fecha": fecha, "Costo_insumos_pote": costo_total})

    historial_df = pd.DataFrame(historial_costos).set_index("fecha")
    st.line_chart(historial_df)
else:
    st.write("No hay datos históricos de COSTO_POTE para mostrar")

