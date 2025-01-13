import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Evaluación de Rendimiento del Personal")

# Subir archivo Excel
uploaded_file = st.file_uploader("Sube tu archivo Excel con la información del personal", type=["xlsx"])

if uploaded_file:
    # Leer archivo subido
    data = pd.read_excel(uploaded_file)
    st.write("Datos cargados correctamente:")
    st.dataframe(data)

    # Configurar criterios de evaluación
    st.sidebar.title("Configurar Criterios")
    criterios = {
        "Puntualidad": st.sidebar.slider("Peso Puntualidad (%)", 0, 100, 30),
        "Cumplimiento de Objetivos": st.sidebar.slider("Peso Cumplimiento de Objetivos (%)", 0, 100, 50),
        "Trabajo en Equipo": st.sidebar.slider("Peso Trabajo en Equipo (%)", 0, 100, 20),
    }

    # Normalizar pesos a 100%
    total_pesos = sum(criterios.values())
    criterios = {k: v / total_pesos for k, v in criterios.items()}

    # Calificar al personal
    st.subheader("Asignar Calificaciones")
    for criterio in criterios.keys():
        data[criterio] = st.number_input(f"Calificación predeterminada para {criterio} (1-10)", min_value=1, max_value=10, value=8)

    # Calcular calificación total
    data["Calificación Total"] = data.apply(
        lambda row: sum(row[criterio] * peso for criterio, peso in criterios.items()), axis=1
    )

    st.subheader("Resultados de la Evaluación")
    st.dataframe(data)

    # Mostrar gráfico
    st.subheader("Gráfico de Rendimiento")
    plt.figure(figsize=(10, 5))
    plt.bar(data["Nombre"], data["Calificación Total"], color="skyblue")
    plt.xlabel("Empleados")
    plt.ylabel("Calificación Total")
    plt.title("Rendimiento del Personal")
    st.pyplot(plt)

    # Botón para descargar resultados
    def convertir_excel(df):
        return df.to_excel(index=False, engine="openpyxl")

    resultados = convertir_excel(data)

    st.download_button(
        label="Descargar Resultados",
        data=resultados,
        file_name="Resultados_Evaluacion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
