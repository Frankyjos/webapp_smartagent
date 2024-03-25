import requests
import streamlit as st
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
            data_json = response.json()
            message_text = data_json["message"]
            nuevo_ticket = data_json["create_ticket"]
            st.write(message_text)
            st.write(nuevo_ticket)
            st.session_state.messages.append({"role": "assistant", "content": message_text})


# Sidebar
sidebar = st.sidebar
with st.sidebar:
        st.image("logoSAv2.png")


            # Topic selection with user-friendly labels
topic = sidebar.selectbox("Seleccione un tópico", list(topic_translations.keys()))

            # Language selection
language = sidebar.selectbox("Seleccione un idioma", ["Spanish", "English"])

            # Trigger on chat input
if st.chat_message:
        send_message(message, topic, language)
