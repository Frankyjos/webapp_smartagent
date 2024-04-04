import requests
import streamlit as st
import time


st.session_state["ticket"] = False
st.session_state["permanece"] = "abierto"
#st.set_page_config(
#    page_title="Smart Agent",
#)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": """
        Soy tu Asistente Virtual **NEWTOMS**, y estoy aquí para brindarte todo el apoyo que necesites.

        Si por algún motivo mi respuesta no cubre tus expectativas, recuerda que puedes escribir "GENERAR UN TICKET" para recibir una atención personalizada y resolver tus inquietudes.
        
        **!Hazme tu  pregunta!**
    """,
        }]
    st.session_state["ticket"] = False

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
    with st.expander("Crea un nuevo ticket"):
        with st.form("nuevo ticket", clear_on_submit=True):
            st.markdown("**Nuevo ticket**")
            name = st.text_input("Nombre")
            email = st.text_input("Correo")
            descripcion = st.session_state["descript"]
            st.text_area("Descripción", value=descripcion)
            submitted = st.form_submit_button("Enviar")
        if submitted:      
                body = {
                    "name": name,
                    "email": email,
                    "description": descripcion,
                }

                response_pop = requests.post(
                        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/tickets",
                        json=body,
                )#
                st.empty()
                if response_pop.status_code == 200:
                    with st.success("Ticket Creado exitosamente!"):
                        time.sleep(10)
                        st.empty()
                    
                else:
                    st.error("Error al crear el ticket: " + str(response_pop.status_code))
        st.session_state["ticket"] = False 
        st.stop()

# Función para enviar la solicitud POST
def send_message(message, topic, language):
    message= {
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
        with st.chat_message("assistant"):
            data_json = response.json()
            message_text = data_json["message"]
            nuevo_ticket = data_json["create_ticket"]
            descrip = data_json["description"]
            st.write(message_text)
            st.session_state.messages.append({"role": "assistant", "content": message_text})
            if nuevo_ticket:
                st.session_state["ticket"] = True
                #st.sidebar.write("ticket activo: " , st.session_state["ticket"])
                st.session_state["descript"] = descrip
                popover()
            #else: st.sidebar.write("mientras el ticket no activa: " , st.session_state["ticket"])


#ticket =  st.session_state["ticket"]
#if ticket:
#    popover()

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
prompt= st.chat_input
if prompt:
    send_message(message, topic, language)

# Reset button for chat history
reset_button = st.sidebar.button("Reiniciar Conversación")
if reset_button:
  # Clear chat history
 #st.session_state.messages = []
 #st.experimental_rerun()
    bienvenido_1 = ("Soy tu Asistente Virtual NEWTOMS, y estoy aquí para brindarte todo el apoyo que necesites.")
    bienvenido_2= ("Si por algún motivo mi respuesta no cubre tus expectativas, recuerda que puedes escribir GENERAR UN TICKET para recibir una atención personalizada y resolver tus inquietudes.")
    bienvenido_3 = ("!Hazme tu pregunta!")

    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": """
        Soy tu Asistente Virtual **NEWTOMS**, y estoy aquí para brindarte todo el apoyo que necesites.

        Si por algún motivo mi respuesta no cubre tus expectativas, recuerda que puedes escribir "GENERAR UN TICKET" para recibir una atención personalizada y resolver tus inquietudes.

        **!Hazme tu  pregunta!**
    """,
        }]
    st.session_state["ticket"] = False
    st.experimental_rerun()