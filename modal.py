import streamlit as st
from streamlit_modal import Modal



modal = Modal(
        "Crear nuevo ticket en Monday", 
        key="demo-modal",
    
        # Optional
        padding=20,    # default value
        max_width=600,  # default value

    )

#open_modal = st.button("Open")
#if open_modal:
modal.open()


if modal.is_open():
    with modal.container():
        st.text_input("Descripción", key="descripcion")
        st.text_input("Nombre del solicitante", key="nombre")
        st.text_input("Email", key="email")
        st.selectbox("Prioridad", ["Baja", "Media", "Alta"], key="prioridad")
        st.button("Crear")


    