# ![](https://github.com/rhythmd18/SmartClarify/blob/main/assets/Asset%209%403x.png)

This is a AI-based doubt solving app designed for high school and college students. Built using the Google's Gemini Pro model on top of Streamlit, it offers easy and elaborate explanations for concepts in the following subjects:

- Physics
- Chemistry
- Mathematics
- Computer Science

Get all your scientific doubts solved [here](https://rhythmd18-smartclarify.streamlit.app/)!

## Description

This application utilizes the Google's brand new AI model named [Gemini](https://deepmind.google/technologies/gemini/#introduction). It employs [LangChain](https://python.langchain.com/docs/get_started/introduction) to craft a prompt based the user's selection of subject, query and the uploaded image. This generated prompt is sent to the Gemini API and the model provides an appropriate response. The application leverages the multi-modal capabilities of the Gemini model as it can process both image and text queries to successfully generate a response. The user can then continue on with their conversation with the bot if their doubt regarding the concerned topic is still unclear.

## Demo



https://github.com/rhythmd18/SmartClarify/assets/109751995/29e21804-87fd-45e2-bf5b-694f823a205f



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
