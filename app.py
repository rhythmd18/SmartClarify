import streamlit as st
# from dotenv import load_dotenv
# import os
from langchain.prompts import PromptTemplate
import google.generativeai as genai

# load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

llm = genai.GenerativeModel('gemini-pro')
llm_vision = genai.GenerativeModel('gemini-pro-vision')

with st.sidebar:
    subject = st.selectbox("Select your Subject", ("Physics", "Chemistry", "Maths", "Computer Science"))


st.title("➕➖SciGemini➗✖️")
st.subheader('Your Personal AI Tutor for for the Sciences!')


prompt = PromptTemplate(
    input_variables=["doubt", "subject"],
    template="""You are an expert science tutor/
    Your name is SciGemini. You explain the concepts in simple terms that are very easy to understand/
    If the question is not strictly about the subject, please reject it politely and ask to rephrase/
    The question is: {doubt}/
    The subject is: {subject}/"""
)


doubt = st.text_input("Ask your doubt...")
doubt = prompt.format(doubt=doubt, subject=subject)

input_type = st.radio("Select Mode of Input...", ("Upload an image", "Take a picture"))
if input_type == "Upload an image":
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
else:
    img = st.camera_input("Take a picture")
submit = st.button("Submit")

def get_response(doubt, img):
    if img:
        response = llm_vision.generate_content([doubt, img])
    else:
        response = llm.generate_content(doubt)
    return response

if submit:
    with st.spinner('Thinking...'):
        response = get_response(doubt, img)
    st.markdown(response.text)
