import streamlit as st
import pandas as pd
import io
import os

st.title("App para procesar Excel con encabezado y resumen")

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    # Leer todo el Excel sin encabezado
    df_raw = pd.read_excel(uploaded_file, header=None)

    # Separar encabezado, datos, resumen
    header_rows = df_raw.iloc[:3]
    data_rows = df_raw.iloc[3:-1]
    summary_row = df_raw.iloc[[-1]]

    # Expandir cada fila intermedia 4 veces seguidas
    expanded_rows = []
    for _, row in data_rows.iterrows():
        for _ in range(4):
            expanded_rows.append(row)

    data_expanded = pd.DataFrame(expanded_rows).reset_index(drop=True)

    # Concatenar todo
    df_final = pd.concat([header_rows, data_expanded, summary_row], ignore_index=True)

    st.subheader("Vista previa del archivo procesado")
    st.dataframe(df_final)

    # Crear nombre de archivo de salida basado en el original
    original_name = uploaded_file.name
    name_root, _ = os.path.splitext(original_name)
    processed_filename = f"{name_root} - procesado.xlsx"

    # Guardar Excel en memoria
    output = io.BytesIO()
    df_final.to_excel(output, index=False, header=False, engine='openpyxl')
    output.seek(0)

    # Botón para descarga
    st.download_button(
        label=f"📥 Descargar: {processed_filename}",
        data=output,
        file_name=processed_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
