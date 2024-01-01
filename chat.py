import streamlit as st
import random
import time
import google.generativeai as genai

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

st.title('Echo Bot')

if 'gemini_model' not in st.session_state:
    st.session_state['gemini_model'] = 'gemini-pro'

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input('Ask a follow-up question...'):
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state['messages'].append({'role': 'user', 'content': prompt})

    with st.spinner('Thinking...'):
        response = model.generate_content(prompt)
        with st.chat_message('assistant'):
            message_placeholder = st.empty()  # Create an empty placeholder
            full_response = '' # Initialize the full_response
            for chunk in response.text.split(): # Split the response into chunks
                full_response += chunk + ' '# Append the chunk to the full_response
                time.sleep(0.05)
                message_placeholder.markdown(full_response + '▌ ')  # Update the message_placeholder
            message_placeholder.markdown(response.text)
    st.session_state['messages'].append({'role': 'assistant', 'content': response.text})


    