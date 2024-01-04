import streamlit as st
from PIL import Image
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import time


# Load API credentials
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)


# Setup memory
memory = ConversationBufferMemory(memory_key='chat_history', input_key='human_input')


# Setup session state
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'model' not in st.session_state:
    st.session_state['model'] = 'gemini-pro'

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
else:
    for message in st.session_state['chat_history']:
        memory.save_context({'human_input': message['human_input']}, {'output': message['AI']})


# Setup LLM
llm = genai.GenerativeModel('gemini-pro')
llm_chat = ChatGoogleGenerativeAI(model=st.session_state['model'], google_api_key=GOOGLE_API_KEY)
llm_vision = genai.GenerativeModel('gemini-pro-vision')


# Setup UI
with st.sidebar:
    st.subheader("Instructions:")
    st.markdown("""
             * Select your subject of choice
             * Ask your doubt in the text box provided
             * Upload an image of your doubt if required
             * And get your explanation instantly!""")
    subject = st.selectbox("Select your Subject", ("Physics", "Chemistry", "Maths", "Computer Science"))
    st.empty()
    st.markdown('***Please note:***\
                *Being an AI-based application, \
                responses are subject to inaccuracies and inconsistencies. \
                Kindly review the responses carefully before using them in your work. \
                Use this application solely for understanding complicated concepts \
                rather than for seeking solutions to questions.*')

st.header("➕➖SciGemini➗✖️")
st.subheader('Your Personal AI Tutor for the Sciences!')
st.text('Powered by Google Gemini')



# Setup prompt
prompt_template = PromptTemplate(
    input_variables=["doubt", "subject"],
    template="""You are an expert science tutor whose name is SciGemini./
    You explain the concepts in simple terms that are very easy to understand (even to a 10-year-old kid)./
    If the the question is left blank and there is no image either, ask the user to write the question./
    Spread out your response in points so that it is easy to grasp./
    Use LaTeX for mathematical equations (use $...$ for inline math expressions)./
    If the question or the image is not related to the subject strictly,/
    please refrain from describing anything and reject politely/
    and ask to rephrase the question or re-upload the image accordingly./

    Conversation history: 
    {chat_history}/

    The question is: {doubt}/
    The subject is: {subject}/
    
    Human: {human_input}/
    AI: 
    """
)



doubt = st.text_input("Ask your doubt...")
message = prompt_template.format(chat_history=[], doubt=doubt, subject=subject, human_input='')



# Setup Image upload/capture
input_type = st.radio("Select Mode of Inputting Image...", ("Upload an image", "Take a picture"))
if input_type == "Upload an image":
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if img:
        st.image(img, caption="Uploaded Image")
else:
    img = st.camera_input("Take a picture")
img = Image.open(img) if img else None
btn_placeholder = st.empty()



def get_response(doubt, img):
    if img:
        response = llm_vision.generate_content([doubt, img])
    else:
        response = llm.generate_content(doubt)
    return response




if st.session_state['submitted'] == False:
    submit = btn_placeholder.button('Submit')

    if submit:

        st.session_state['submitted'] = True
        btn_placeholder.empty()

        with st.chat_message('user'):
            st.markdown(doubt)
        st.session_state['messages'].append({'role': 'user', 'content': doubt})

        with st.spinner('Thinking...'):
            response = get_response(message, img)
        message = {'human_input': doubt, 'AI': response.text}
        st.session_state['chat_history'].append(message)

        with st.chat_message('assistant'):
            message_placeholder = st.empty()  # Create an empty placeholder
            full_response = '' # Initialize the full_response
            with st.spinner('Typing...'):
                for chunk in response.text.split(): # Split the response into chunks
                    full_response += chunk + ' '# Append the chunk to the full_response
                    time.sleep(0.05)
                    message_placeholder.text(full_response + '▌ ')  # Update the message_placeholder
            message_placeholder.markdown(response.text)
        st.session_state['messages'].append({'role': 'assistant', 'content': response.text})



# Setup chaining functionalities
llmchain = LLMChain(
    memory=memory,
    prompt=prompt_template,
    llm=llm_chat,
    verbose=True
)



if st.session_state['submitted']:

    for message in st.session_state['messages']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    follow_up = st.chat_input('Ask a follow-up question...')
    if follow_up:
        with st.chat_message('user'):
            st.markdown(follow_up)
        st.session_state['messages'].append({'role': 'user', 'content': follow_up})

        with st.spinner('Thinking...'):
            response = llmchain.run({'doubt': doubt, 'subject':subject, 'human_input': follow_up})
        message = {'human_input': follow_up, 'AI': response}
        st.session_state['chat_history'].append(message)

        with st.chat_message('assistant'):
            message_placeholder = st.empty()  # Create an empty placeholder
            full_response = '' # Initialize the full_response
            with st.spinner('Typing...'):
                for chunk in response.split(): # Split the response into chunks
                    full_response += chunk + ' '# Append the chunk to the full_response
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + '▌ ')  # Update the message_placeholder
            message_placeholder.markdown(response)
        st.session_state['messages'].append({'role': 'assistant', 'content': response})
