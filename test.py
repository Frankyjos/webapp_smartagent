import streamlit as st
import requests

# Función para realizar la solicitud al endpoint
def make_request(message, chat_history):
  # Definición del endpoint
  endpoint = "https://api.endpoint.com"

  # Definición del body de la solicitud
  body = {
    "message": message,
    "language": "es",
    "topic": "jairo.davila+demo#topic",
    "summary": "false",
    "chat_history": chat_history,
  }

  # Envío de la solicitud
  response = requests.post(endpoint, json=body)

  # Validación del código de respuesta
  if response.status_code == 200:
    return response.json()
  else:
    raise Exception("Error al realizar la solicitud: {}".format(response.status_code))

# Inicialización de variables
message_text = ""
chat_history = ""

# Creación de la interfaz de usuario
with st.form("chat_form"):
  st.text_input("Mensaje", key="message_text", value=message_text)
  st.form_submit_button("Enviar")

# Actualización del historial de chat
if message_text:
  chat_history = message_text

# Realización de la solicitud
if message_text:
  response = make_request(message_text, chat_history)
  
  # Mostrar la respuesta del endpoint
  if response:
    st.write(response)
