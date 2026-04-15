import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# Configuración visual de la página
st.set_page_config(page_title="Traderflow App", layout="wide")
st.title("📈 Bitácora de Trading Compartida")

# Conexión técnica con los "Misterios" (Secrets)
conn = st.connection("supabase", type=SupabaseConnection)

# Formulario en la barra lateral para registrar órdenes
with st.sidebar:
    st.header("Nueva Orden")
    with st.form("registro"):
        f = st.date_input("Fecha")
        idx = st.selectbox("Índice", ["B1", "B3", "C1", "C5"])
        lot = st.number_input("Lotaje", value=0.0, step=0.01)
        res = st.number_input("Profit/Loss ($)", value=0.0, step=0.1)
        obs = st.text_area("Comentarios de la orden")
        enviar = st.form_submit_button("Guardar Operación")

    if enviar:
        try:
            conn.table("trading_journal").insert({
                "fecha": str(f),
                "índice": idx,
                "lotaje": lot,
                "beneficio_pérdida": res,
                "comentario": obs
            }).execute()
            st.success("¡Operación guardada con éxito!")
        except Exception as e:
            st.error(f"Error al guardar: {e}")

# Sección principal: Historial de Operaciones
st.subheader("📋 Historial de Operaciones")

# Consultar los datos a Supabase
try:
    datos = conn.table("trading_journal").select("*").order("fecha", desc=True).execute()
    
    if datos.data:
        df = pd.DataFrame(datos.data)
        
        # Aseguramos que las columnas se muestren en un orden limpio
        columnas_visibles = ["fecha", "índice", "lotaje", "beneficio_pérdida", "comentario"]
        st.dataframe(df[columnas_visibles], use_container_width=True)
        
        # Cálculo del balance total
        total = df["beneficio_pérdida"].sum()
        st.metric("Balance Total", f"$ {total:.2f}")
    else:
        st.info("Aún no hay operaciones registradas. ¡Comienza por añadir una!")
        
except Exception as e:
    st.error("Todavía hay un detalle por conectar o la tabla está vacía.")
