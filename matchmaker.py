import streamlit as st
import pandas as pd
# Inicializa la variable de estado para acumular los emparejamientos
if 'emparejamientos_acumulados' not in st.session_state:
    st.session_state.emparejamientos_acumulados = {categoria: [] for categoria in [
        "El + pelota", "El + morcillón", "El + despistado", "El + empollón", "El + cabeza",
        "El + charlatán", "El + cabrón", "El + seco", "El + escaqueado", "El + empanado", 
        "El + chulo", "La + vieja", "El + abuelo", "El + flamenco"
    ]}
st.text("25 Aniversario promoción Polígono Sur 97/99")
# Entrada para el nombre del usuario
nombre_usuario = st.text_input("Introduce tu nombre:")
# Verificar si el nombre ha sido introducido antes de continuar
if nombre_usuario:
    # Lista de nombres
    nombres = [
        "Josemari", "Dani Garra", "Ivan Morcilla", "Pino Culito Húmedo", "Edu", 
        "Juani", "Inma Phoebe", "Mari Angeles", "Ely", "Ternero", 
        "Juanmi", "Raúl", "Quique", "Miguel Ten"
    ]
    # Lista de categorías
    categorias = [
        "", "El + pelota", "El + morcillón", "El + despistado", "El + empollón", "El + cabeza",
        "El + charlatán", "El + cabrón", "El + seco", "El + escaqueado", "El + empanado", 
        "El + chulo", "La + vieja", "El + abuelo", "El + flamenco"
    ]
    # Título de la aplicación
    st.title(f"{nombre_usuario}, nomina a una persona por categoría")
    # Diccionario para guardar los emparejamientos actuales
    emparejamientos = {}
    # Generar un combobox para cada nombre
    for nombre in nombres:
        categoria_seleccionada = st.selectbox(f"Emparejar {nombre} con:", categorias, key=nombre)
        emparejamientos[nombre] = categoria_seleccionada
    # Mostrar los emparejamientos seleccionados
    st.subheader("Emparejamientos seleccionados")
    for nombre, categoria in emparejamientos.items():
        st.write(f"{nombre} → {categoria}")
    # Botón para acumular los emparejamientos
    if st.button("Finalizar y acumular emparejamientos"):
        # Acumular los emparejamientos en el estado de la aplicación
        for nombre, categoria in emparejamientos.items():
            if categoria and categoria in st.session_state.emparejamientos_acumulados:
                st.session_state.emparejamientos_acumulados[categoria].append(nombre)
        st.success("Emparejamientos acumulados correctamente.")
    # Mostrar el listado de quién lleva más votos por categoría
    st.subheader("Persona con más votos por categoría")
    resultados = []
    for categoria, votos in st.session_state.emparejamientos_acumulados.items():
        if votos:
            ganador = pd.Series(votos).value_counts().idxmax()
            conteo = pd.Series(votos).value_counts().max()
            resultados.append((categoria, ganador, conteo))
    # Convertir a DataFrame y mostrar en una tabla
    df_resultados = pd.DataFrame(resultados, columns=["Categoría", "Persona con más votos", "Votos"])
    st.table(df_resultados)
else:
    st.warning("Por favor, introduce tu nombre para continuar.")
