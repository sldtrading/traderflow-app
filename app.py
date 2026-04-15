import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

st.set_page_config(page_title="Traderflow App", layout="wide")
st.title("📈 Bitácora de Trading Compartida")

# Conexión técnica
conn = st.connection("supabase", type=SupabaseConnection)

# Formulario para registrar órdenes
with st.sidebar:
    st.header("Nueva Orden")
    with st.form("registro"):
        f = st.date_input("Fecha")
        idx = st.selectbox("Índice", ["B1", "B3", "C1", "C5"])
        lot = st.number_input("Lotaje", value=2.5)
        res = st.number_input("Profit/Loss ($)")
        obs = st.text_area("Comentarios de la orden")
        enviar = st.form_submit_button("Guardar Operación")
        
        if enviar:
            conn.table("trading_journal").insert({
                "fecha": str(f), "indice": idx, "lotaje": lot, 
                "profit_loss": res, "comentario": obs
            }).execute()
            st.success("¡Orden guardada! Tu amigo ya puede verla.")

# Tabla de resultados
st.subheader("Historial de Operaciones")
datos = conn.table("trading_journal").select("*").order("fecha", desc=True).execute()
if datos.data:
    df = pd.DataFrame(datos.data)
    st.dataframe(df[["fecha", "indice", "lotaje", "profit_loss", "comentario"]], use_container_width=True)
    st.metric("Balance Total", f"$ {df['profit_loss'].sum():.2f}")
