# SciGemini

This is a AI-based doubt solving app designed for high school and college students. Built using the Google's Gemini Pro model on top of Streamlit, it offers easy and elaborate explanations for concepts in the following subjects:

- Physics
- Chemistry
- Mathematics
- Computer Science

Get all your scientific doubts solved [here](https://rhythmd18-scigemini.streamlit.app/)!

## Description

This application utilizes the Google's brand new AI model named [Gemini](https://deepmind.google/technologies/gemini/#introduction). It employs [LangChain](https://python.langchain.com/docs/get_started/introduction) to craft a prompt based the user's selection of subject, query and the uploaded image. This generated prompt is sent to the Gemini API and the model provides an appropriate response that be helpful to the concerned user. The application leverages the multi-modal capabilities of the Gemini model as it can process both image and text queries to successfully generate a response!

## Demo

## Features

- Get explanations based on a query or an image or both
- Ability to upload image/take a picture of your doubt
- Get your explanations in a pointwise format
- Light/dark mode toggle
- Cross platform

## Tech Stack

**Client:** Streamlit

**Server:** Google Gemini-Pro API, LangChain

## Acknowledgements

- [Gemini Docs and API reference](https://ai.google.dev/docs)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [Streamlit Docs](https://docs.streamlit.io/)

## Support

For support, email duttarhythm18@gmail.com.
