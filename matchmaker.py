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
                categoria TEXT, votante TEXT)''')

conn.commit()

# Inicializar session_state para evitar reinicio
if 'votacion_completada' not in st.session_state:
    st.session_state['votacion_completada'] = False

# Encabezado de la app
st.text("25 Aniversario promoción Polígono Sur 97/99")

# Entrada para el nombre del usuario
nombre_usuario = st.text_input("Introduce tu nombre:")

# Definir el nombre del administrador (puedes cambiarlo por una contraseña si lo prefieres)
admin_usuario = "elmasca"

# Si el usuario es el propietario, mostrar todos los resultados
if nombre_usuario == admin_usuario:
    st.subheader("Resultados de todas las votaciones")
    c.execute("SELECT * FROM emparejamientos")
    todas_votaciones = c.fetchall()
    df_todas = pd.DataFrame(todas_votaciones, columns=["Nombre", "Categoría", "Votante"])
    st.table(df_todas)
elif nombre_usuario and not st.session_state['votacion_completada']:  # Si el usuario no es el propietario y no ha votado

    # Verificar si el usuario ya ha votado
    c.execute("SELECT nombre_usuario FROM votantes WHERE nombre_usuario = ?", (nombre_usuario,))
    if c.fetchone():
        st.warning("Ya has votado, no puedes volver a hacerlo.")
    else:
        # Lista de nombres
        nombres = [
            "Josemari", "Dani", "Ivan", "Pino", "Edu", "Juani", "Inma", 
            "Mari Angeles", "Ely", "Ternero", "Raúl", "Quique", "Miguel Ten", "Roberto"
        ]

        # Lista de categorías
        categorias = [
            "", "El/La + charlatán", "El/La + abuelo/a", "El/La + empanado/a", "El/La + fiestero/a", "El/La + forever young",
            "El/La + olvidadizo/a", "El/La + tardón/a", "El/La + Friki", "El/La + cabezón/a", "El/La + escaqueado/a", 
            "El/La + empollon/a", "El/La + dramático/a", "El/La + pasota", "El/La + pelota"
        ]

        # Diccionario para guardar los emparejamientos actuales
        emparejamientos = {}

        # Generar un combobox para cada nombre
        for nombre in nombres:
            categoria_seleccionada = st.selectbox(f"Creo que {nombre} es:", categorias, key=nombre)
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
                    c.execute("INSERT INTO emparejamientos (nombre, categoria, votante) VALUES (?, ?, ?)", (nombre, categoria, nombre_usuario))
            
            # Registrar que este usuario ha votado
            c.execute("INSERT INTO votantes (nombre_usuario) VALUES (?)", (nombre_usuario,))
            conn.commit()
            
            # Actualizar session_state para marcar que la votación fue completada
            st.session_state['votacion_completada'] = True
            st.success("Emparejamientos acumulados correctamente. Ya no puedes volver a votar.")

# Mostrar los resultados: persona con más votos por categoría
if nombre_usuario and nombre_usuario != admin_usuario:
    st.subheader("Persona con más votos por categoría")
    resultados = []
    for categoria in categorias:
        if categoria:
            c.execute("SELECT nombre, COUNT(*) as conteo FROM emparejamientos WHERE categoria = ? GROUP BY nombre ORDER BY conteo DESC LIMIT 1", (categoria,))
            resultado = c.fetchone()
            if resultado:
                resultados.append((categoria, resultado[0], resultado[1]))

    # Convertir resultados a DataFrame y mostrar en tabla
    if resultados:
        df_resultados = pd.DataFrame(resultados, columns=["Categoría", "Persona con más votos", "Votos"])
        st.table(df_resultados)
else:
    st.warning("Por favor, introduce tu nombre para continuar.")
