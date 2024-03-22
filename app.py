import requests
import streamlit as st
from streamlit_modal import Modal

st.set_page_config(
    page_title="Smart Agent",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if message := st.chat_input("Send a message"):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)

# Topic translation dictionary (invisible to user)
topic_translations = {
    "Retail": "jairo.davila+demo#RETAIL",
    "Travel & Hospitality": "jairo.davila+demo#TRAVEL",
    "Industrial, engineering & construction": "jairo.davila+demo#ENGINEERING",
    "Financial services & insurance": "jairo.davila+demo#INSURANCE",
}

# Función para enviar la solicitud POST
def send_message(message, user_selected_topic, language):


    # Translate topic for internal use
    translated_topic = topic_translations.get(user_selected_topic)
    if not translated_topic:
        # Handle potential missing translation (optional: raise warning or use default)
        translated_topic = user_selected_topic  # Or provide a default value

    message = {
        "message": message,
        "language": language,
        "topic": translated_topic,
        "summary": "false",
        "chat_history": [],
    }
    response = requests.post(
        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/send-message",
        json=message,
    )
    if response.status_code == 200:
        with st.sidebar:
            st.success("Mensaje enviado correctamente")
        #    st.write(message)
        with st.chat_message("assistant"):
            data = response.text
            st.write(data)
            st.session_state.messages.append({"role": "assistant", "content": data})


     # Check for the string and set the boolean variable
        create_ticket_flag = "[CREATE TICKET]" in data
        st.session_state.create_ticket_flag = create_ticket_flag  # Store in session state
     #  st.write(create_ticket_flag)
        if create_ticket_flag:
            st.button("Crear ticket")
        else: st.empty()
        st.session_state.messages.append({"role": "assistant", "content": data})

# Sidebar
sidebar = st.sidebar
with st.sidebar:
    st.image("logoSA.png")


# Topic selection with user-friendly labels
topic = sidebar.selectbox("Seleccione un tópico", list(topic_translations.keys()))

# Language selection
language = sidebar.selectbox("Seleccione un idioma", ["Spanish", "English"])

# Trigger on chat input
if st.chat_message:
    send_message(message, topic, language)


# Función para enviar el request POST
def crear_ticket(descripcion):
    # Definir la URL y el body del requests
    url = "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/tickets"
    body = {
        "description": descripcion,
    }

# Enviar el request
    responseticket = requests.post(url, json=body)
    if responseticket.status_code == 200:
            st.success("Ticket creado con éxito")


modal = Modal(
    "Crear nuevo ticket en Monday", 
    key="demo-modal",
    
    # Optional
    padding=20,    # default value
    max_width=600,  # default value

)

with st.sidebar:
    nuevo_ticket = st.checkbox("Crear nuevo ticket")
    if nuevo_ticket:
        open_modal = st.button("Nuevo ticket")
        if open_modal:
            modal.open()
    else:
        st.empty()

# Si el modal está abierto, mostrar el contenido
if modal.is_open():
    with modal.container():
        # Campos del formulario
        descripcion = st.text_input("Descripción", key="descripcion")


        # Botón para crear el ticket
        boton_crear = st.button("Crear")

        # Si se hace clic en el botón "Crear", enviar el request
        if boton_crear:
            crear_ticket(descripcion)
