# app.py

import streamlit as st
import pandas as pd
import io

st.title("App para procesar Excel con encabezado y resumen")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    # Leer todo el Excel como filas, sin interpretar encabezados
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Separar las partes
    header_rows = df_raw.iloc[:3]         # Primeras 3 filas
    data_rows = df_raw.iloc[3:-1]         # Datos que vamos a duplicar
    summary_row = df_raw.iloc[[-1]]       # Última fila (resumen)

    # Triplicar cada fila y mantener el orden
    expanded_rows = []
    for _, row in data_rows.iterrows():
        for _ in range(4):  # original + 3 copias
            expanded_rows.append(row)

    data_expanded = pd.DataFrame(expanded_rows).reset_index(drop=True)

    # Concatenar todo: encabezado + datos expandidos + resumen
    df_final = pd.concat([header_rows, data_expanded, summary_row], ignore_index=True)

    # Mostrar resultado
    st.subheader("Vista previa del archivo procesado")
    st.dataframe(df_final)

    # Guardar para descarga
    output = io.BytesIO()
    df_final.to_excel(output, index=False, header=False, engine='openpyxl')
    output.seek(0)

    st.download_button(
        label="📥 Descargar Excel Procesado",
        data=output,
        file_name="salida_procesada.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
