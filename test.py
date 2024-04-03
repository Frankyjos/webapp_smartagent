#from openai import OpenAI
import streamlit as st
import pandas as pd

st.title("Test")
st.caption("My Test powered by OpenAI LLM and Streamlit")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello!"}]
    st.session_state["signup"] = False
    st.session_state["pin"] = False

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
    try:
        user_database = pd.read_csv('your_local_directory')
    except FileNotFoundError:
        st.chat_message("assistant").write("Do you wanna join here?")
        st.session_state["pin"]=True
    else:
        st.chat_message("assistant").write('Please enter your username.')

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
if prompt == 'y':
    st.session_state["pin"]=True
    msg = "Okay! Nice to meet you sir. Please fill in the blanks for sign up."
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["signup"] = True
if st.session_state["signup"] == True:
    x=0
    with st.chat_message("assistant").form("Sign up Form"):
        username = st.text_input('Tell me the name you want to be called in here.')
        if username:
            x+=1
        password = st.text_input("Your Password", key="chatbot_api_key", type="password")
        if password:
            x+=1
        age = st.text_input('How old are you?')
        if age:
            x+=1
        nationality = st.text_input('Where are you from?')
        if nationality:
            x+=1
        city = st.text_input('Tell me which city are you living in.')
        if city:
            x+=1
        problem = st.text_input("What's your biggest problem right now?")
        if problem:
            x+=1
        col1,col2=st.columns([9,1])
        with col2:
            button=st.form_submit_button('ok')
        if button:
            if x==6:
                col1,col2,col3=st.columns([2,7,1])
                with col2:
                    st.write("This is your signup information.")
                    st.write("If you want to change your information, please fill it out now.")
                    st.write("""If you're happy with it, please say "I like it!" in the chat.""")
                    st.title('')
                df = pd.DataFrame({
                    "User Name": [username],
                    "Password": [password],
                    "age": [age],
                    "nationality": [nationality],
                    "city": [city],
                    "problem": [problem]
                })
                st.dataframe(df, use_container_width=True, hide_index=True)            
            else:
                pass