import requests
import streamlit as st
import time


st.set_page_config(
    page_title="Smart Agent",
)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": """
            Hola soy tu asistente virtual **NEWTOMS**. Si por algún motivo mi respuesta no cubre tus expectativas, solicita ayuda para atención personalizada. 
 
            **!Hazme tu pregunta!**
    """,
        }]

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

#def envio_ticket():
#    body = {
#        "name": "user1 test",
#        "email": "ttest@gmail.com",
#        "description":"tengo una incidencia",
#        }
#    response_pop = requests.post(
#        "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/tickets",
#        json=body,
#        )
#    if response_pop.status_code == 200:
#        data_json = response_pop.json()
#        id_ticket = data_json["ticket_id"]
#        msg = "Ticket creado exitosamente bajo el ID #" + id_ticket
#        st.session_state.messages.append({"role": "assistant", "content": msg})
#        st.chat_message("assistant").write(msg)

# Función para enviar la solicitud POST
def send_message(message, topic, language):
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
            if nuevo_ticket:
                st.session_state["nuevo_ticket"] = True  # Store in session state for persistence
                st.session_state["descript"] = descrip
                st.experimental_rerun()

if "nuevo_ticket" in st.session_state and st.session_state["nuevo_ticket"]:
    with st.expander("**Click aqui para crear un nuevo ticket**" if st.session_state["select_language"]=="Español" else "**Click here to create a new ticket**"):
        with st.form("Ticket", clear_on_submit=True):
            name = st.text_input('Nombre' if st.session_state["select_language"]=="Español" else "Name")
            email = st.text_input('Correo' if st.session_state["select_language"]=="Español" else "Email")
            descripcion = st.session_state["descript"] 
            descripcion_completa = st.text_area("Descripción" if st.session_state["select_language"]=="Español" else "Description", value=descripcion)
            submit= st.form_submit_button("Crear" if st.session_state["select_language"]=="Español" else "Create") 
        if submit:
            #st.spinner(st.success("Ticket creado exitosamente!"))
            st.session_state["nuevo_ticket"] = False
            #time.sleep(0.001)
            #envio_ticket()

            body = {
            "name": name,
            "email": email,
            "description" :descripcion_completa,
            }
            response_pop = requests.post(
            "https://7op9qcm679.execute-api.us-east-1.amazonaws.com/dev/tickets",
            json=body,
            )
            if response_pop.status_code == 200:
                data_json = response_pop.json()
                id_ticket = data_json["ticket_id"]
                msg = "Ticket creado exitosamente bajo el ID #" + id_ticket
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)

            st.experimental_rerun()
            
# Sidebar
sidebar = st.sidebar
with st.sidebar:
    st.image("logoSAv3.png")


# Fetch topics before displaying the selection box
topics_name = fetch_topics()

# Topic selection with user-friendly labels
topic = sidebar.selectbox("Seleccione un tópico", topics_name)

# Language selection
language = sidebar.selectbox("Seleccione un idioma", ["Español", "Ingles"])
st.session_state["select_language"] = language

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
    st.session_state["nuevo_ticket"] = False
    st.session_state["messages"] = [{
        "role": "assistant", 
        "content": """
        Hola soy tu asistente virtual **NEWTOMS**. Si por algún motivo mi respuesta no cubre tus expectativas, solicita ayuda para atención personalizada. 
 
        **!Hazme tu pregunta!**
    """,
        }]
    st.experimental_rerun()