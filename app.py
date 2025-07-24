# app.py

import streamlit as st
import pandas as pd
import io

st.title("App para procesar Excel con encabezado y resumen")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    # Leer TODO el Excel como texto, para conservar encabezados como filas
    df_raw = pd.read_excel(uploaded_file, header=None)  # No asumir encabezado

    # Separar las partes
    header_rows = df_raw.iloc[:3]         # Primeras 3 filas (encabezado)
    data_rows = df_raw.iloc[3:-1]         # Filas intermedias (datos a triplicar)
    summary_row = df_raw.iloc[[-1]]       # Última fila (resumen)

    # Triplicar las filas de datos (4 veces total)
    data_tripled = pd.concat([data_rows]*4, ignore_index=True)

    # Concatenar todo nuevamente
    df_final = pd.concat([header_rows, data_tripled, summary_row], ignore_index=True)

    st.subheader("Vista previa del archivo procesado")
    st.dataframe(df_final)

    # Guardar a Excel para descarga
    output = io.BytesIO()
    df_final.to_excel(output, index=False, header=False, engine='openpyxl')
    output.seek(0)

    st.download_button(
        label="📥 Descargar Excel Procesado",
        data=output,
        file_name="salida_procesada.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
