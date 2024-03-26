import requests
import streamlit as st
import time
import random


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

# Function to fetch topics from the API
def fetch_topics():
    headers = {
        "admin": "jairo.davila+demo@newtoms.com",
        "channel": "WEB",
    }
    response = requests.get("https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/topics-channel", headers=headers)
    if response.status_code == 200:
        topics_data = response.json()
        topic_names = [topic["topic_name"] for topic in topics_data]
        #topic_id = [topic["topic_id"] for topic in topics_data]
        return topic_names
    else:
        # Handle error: display message or use default topics
        st.error("Error al obtener los tópicos")

# Accept user input
if message := st.chat_input("Escribe una pregunta"):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)

def popover():
    with st.popover("Crear nuevo ticket"):
        with st.form("tickets",clear_on_submit=True):
            st.markdown("**Nuevo ticket**")
            name = st.text_input("Nombre")
            email = st.text_input("Correo")
            descripcion = st.text_area("Descripción")
            submitted = st.form_submit_button("Enviar")

            if submitted:
            # Construir el cuerpo del request JSON
                body = {
                    "name": name,
                    "email": email,
                    "description": descripcion,
                }

                # Realizar la petición POST
                response = requests.post(
                        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/tickets",
                        json=body,
                )

                #Manejar la respuesta
                if response.status_code == 200:
                    with st.spinner("Ticket Creado exitosamente!"):
                        time.sleep(5)
                else:
                  st.error("Error al crear el ticket: " + str(response.status_code))

# Función para enviar la solicitud POST
def send_message(message, topic_ids, language):
    ticket_true = True
    message = {
        "message": message,
        "language": language,
        "topic": "jairo.davila+demo#"+topic,
        "summary": "false",
        "chat_history": [],
    }
    response = requests.post(
        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/send-message",
        json=message,
    )
    if response.status_code == 200:
        #with st.sidebar:
        #  st.success("Mensajes enviado correctamente")
         #   st.write(message)
        with st.chat_message("assistant"):
            data_json = response.json()
            message_text = data_json["message"]
            nuevo_ticket = data_json["create_ticket"]
            st.write(message_text)
            #st.write(nuevo_ticket)
            st.session_state.messages.append({"role": "assistant", "content": message_text})
        #with sidebar:
        #    nuevoticket = st.write(nuevo_ticket)
        


# Sidebar
sidebar = st.sidebar
with st.sidebar:
    st.image("logoSAv3.png")


# Fetch topics before displaying the selection box
topics_name = fetch_topics()

# Topic selection with user-friendly labels
topic = sidebar.selectbox("Seleccione un tópico", topics_name)

# Language selection
language = sidebar.selectbox("Seleccione un idioma", ["Spanish", "English"])

# Trigger on chat input
if st.chat_message:
    send_message(message, topic, language)

with st.sidebar:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    popover()