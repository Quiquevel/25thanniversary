import streamlit as st
import pandas as pd
import sqlite3

# Crear la conexión a la base de datos SQLite
conn = sqlite3.connect('votos.db')
c = conn.cursor()

# Crear la tabla de votantes si no existe
c.execute('''CREATE TABLE IF NOT EXISTS votantes (
                nombre_usuario TEXT PRIMARY KEY)''')

# Crear la tabla de emparejamientos si no existe
c.execute('''CREATE TABLE IF NOT EXISTS emparejamientos (
                nombre TEXT,
                categoria TEXT)''')

conn.commit()

# Encabezado de la app
st.text("25 Aniversario promoción Polígono Sur 97/99")

# Entrada para el nombre del usuario
nombre_usuario = st.text_input("Introduce tu nombre:")

# Verificar si el nombre ha sido introducido antes de continuar
if nombre_usuario:
    
    # Verificar si el usuario ya ha votado
    c.execute("SELECT nombre_usuario FROM votantes WHERE nombre_usuario = ?", (nombre_usuario,))
    if c.fetchone():
        st.warning("Ya has votado, no puedes volver a hacerlo.")
    else:
        # Lista de nombres
        nombres = [
            "Josemari", "Dani", "Ivan", "Pino", "Edu", "Alberto", 
            "Juani", "Inma", "Mari Angeles", "Ely", "Ternero", 
            "Juanmi", "Raúl", "Quique", "Miguel Ten", "Roberto", "Mario", "Jorge"
        ]

        # Lista de categorías
        categorias = [
            "", "El/La + pelota", "El/La + morcillón/a", "El/La + despistado/a", "El/La + empollón/a", "El/La + cabezón/a",
            "El/La + charlatán/a", "El/La + cabrón/a", "El/La + seco/a", "El/La + escaqueado/a", "El/La + empanado/a", 
            "El/La + chulo/a", "El/La + viejo/a", "El/La + abuelo/a", "El/La + flamenco/a", "El/La + pasota", "El/La + desaparecido/a"
        ]

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

        # Botón para finalizar el emparejamiento
        if st.button("Finalizar y acumular emparejamientos"):
            # Guardar en la base de datos los emparejamientos
            for nombre, categoria in emparejamientos.items():
                if categoria:  # Solo guardar si se seleccionó una categoría
                    c.execute("INSERT INTO emparejamientos (nombre, categoria) VALUES (?, ?)", (nombre, categoria))
            
            # Registrar que este usuario ha votado
            c.execute("INSERT INTO votantes (nombre_usuario) VALUES (?)", (nombre_usuario,))
            conn.commit()
            st.success("Emparejamientos acumulados correctamente. Ya no puedes volver a votar.")
    
    # Mostrar los resultados: persona con más votos por categoría
    st.subheader("Persona con más votos por categoría")
    resultados = []
    for categoria in categorias:
        if categoria:
            c.execute("SELECT nombre, COUNT(*) as conteo FROM emparejamientos WHERE categoria = ? GROUP BY nombre ORDER BY conteo DESC LIMIT 1", (categoria,))
            resultado = c.fetchone()
            if resultado:
                resultados.append((categoria, resultado[0], resultado[1]))

    # Convertir resultados a DataFrame y mostrar en tabla
    df_resultados = pd.DataFrame(resultados, columns=["Categoría", "Persona con más votos", "Votos"])
    st.table(df_resultados)

else:
    st.warning("Por favor, introduce tu nombre para continuar.")
