import streamlit as st
# from dotenv import load_dotenv
# import os
from langchain.prompts import PromptTemplate
from PIL import Image
import google.generativeai as genai

# load_dotenv()

# os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
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


st.title("➕➖SciGemini➗✖️")
st.subheader('Your Personal AI Tutor for the Sciences!')
st.write('Powered by Google Gemini')


prompt = PromptTemplate(
    input_variables=["doubt", "subject"],
    template="""You are an expert science tutor/
    Your name is SciGemini. You explain the concepts in simple terms that are very easy to understand (even to a 10-year-old kid)./
    If the question is left blank and there is no image either, ask the user to write the question./
    Spread out your response in points so that it is easy to grasp./
    Use LaTeX for mathematical equations./
    If the question or the image is not related to the subject strictly,/
    please refrain from describing anything and reject politely/
    and ask to rephrase the question or re-upload the image accordingly/
    The question is: {doubt}/
    The subject is: {subject}/"""
)


doubt = st.text_input("Ask your doubt...")
message = prompt.format(doubt=doubt, subject=subject)

input_type = st.radio("Select Mode of Inputting Image...", ("Upload an image", "Take a picture"))
if input_type == "Upload an image":
    img = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
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
    if img:
        st.image(img)
    st.write(response.text)
