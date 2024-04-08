import requests
import streamlit as st

st.set_page_config(
    page_title="Smart Agent",
)

if "messages" not in st.session_state:
    st.session_state["ticket"] = False
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": """
        Hola Soy tu Asistente Virtual **NEWTOMS**. Si por algún motivo mi respuesta no cubre tus expectativas, solicita ayuda para atención personalizada. 
 
        **!Hazme tu pregunta!**
        """
        }]
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
        return topic_names
    else:
        # Handle error: display message or use default topics
        st.error("Error al obtener los tópicos")

# Fetch topics before displaying the selection box
topics_name = fetch_topics()

# Sidebar
sidebar = st.sidebar
with st.sidebar:
    st.image("logoSAv3.png")

# Topic selection with user-friendly labels
topic = sidebar.selectbox("Seleccione un tópico", topics_name)

# Language selection
language = sidebar.selectbox("Seleccione un idioma", ["Spanish", "English"])

# Accept user input
if message := st.chat_input("Escribe una pregunta"):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)
if message:
    message= {
        "message": message,
        "language": language,
        "topic": "jairo.davila+demo#"+topic,
        "summary": "false",
        "chat_history": message,
    }
    response = requests.post(
        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/send-message",
        json=message,
    )
    if response.status_code == 200:
        with st.chat_message("assistant"):
            data_json = response.json()
            message_text = data_json["message"]
            nuevo_ticket = data_json["create_ticket"]
            descrip = data_json["description"]
            st.write(message_text)
            st.session_state.messages.append({"role": "assistant", "content": message_text})
    

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if message == 'y' and not st.session_state["ticket"]:
    msg = "Crea un nuevo ticket en el siguiente formulario"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["ticket"] = True  # Flag to indicate signup process has started
if  st.session_state["ticket"] == True:
    with st.chat_message("assistant").form("ticket_form"):
        name = st.text_input("Nombre")
        email = st.text_input("Correo")
        descripcion = st.text_area("Descripción")
                
        submitted = st.form_submit_button("Enviar")
        if submitted:
            msg = "Ticket creado exitosamente!"
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.session_state["ticket"] = False  # Optionally reset signup flag

