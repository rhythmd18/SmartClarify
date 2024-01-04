import streamlit as st
from PIL import Image
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI



GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)


llm = genai.GenerativeModel('gemini-pro')
llm_vision = genai.GenerativeModel('gemini-pro-vision')


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


st.title("➕➖SciGemini➗✖️")
st.subheader('Your Personal AI Tutor for the Sciences!')
st.text('Powered by Google Gemini')



if 'model' not in st.session_state:
    st.session_state['model'] = 'gemini-pro'

if 'messages' not in st.session_state:
    st.session_state['messages'] = []


prompt_template = PromptTemplate(
    input_variables=["doubt", "subject"],
    template="""You are an expert science tutor/
    Your name is SciGemini. You explain the concepts in simple terms that are very easy to understand (even to a 10-year-old kid)./
    If the question is left blank and there is no image either, ask the user to write the question./
    Spread out your response in points so that it is easy to grasp./
    Use LaTeX for mathematical equations (use $...$ for inline math expressions)./
    If the question or the image is not related to the subject strictly,/
    please refrain from describing anything and reject politely/
    and ask to rephrase the question or re-upload the image accordingly/
    The question is: {doubt}/
    The subject is: {subject}/"""
)


doubt = st.text_input("Ask your doubt...")
message = prompt_template.format(doubt=doubt, subject=subject)


input_type = st.radio("Select Mode of Inputting Image...", ("Upload an image", "Take a picture"))
if input_type == "Upload an image":
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if img:
        st.image(img)
else:
    img = st.camera_input("Take a picture")
img = Image.open(img) if img else None
submit = st.button("Submit")


def get_response(doubt, img):
    if img:
        response = llm_vision.generate_content([doubt, img])
    else:
        response = llm.generate_content(doubt)
    return response

if submit:
    with st.spinner('Thinking...'):
        response = get_response(message, img)
    st.write(response.text)
    prompt = st.chat_input('Ask a follow-up question...')
