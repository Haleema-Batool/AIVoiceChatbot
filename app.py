
import streamlit as st
from dotenv import load_dotenv
import os
from gtts import gTTS
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
import tempfile

# Load API key
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# Streamlit UI
st.title("AI Voice Chatbot")
st.write("Chat with AI using LangChain + Groq")

# User input
user_input = st.text_input("Type your message")

if st.button("Send"):

    if user_input:

        # AI response
        response = llm.invoke([
            HumanMessage(content=user_input)
        ])

        ai_response = response.content

        st.write("AI:", ai_response)

        # Convert to voice
        tts = gTTS(ai_response)

        # Save temporary mp3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)

            audio_file = open(fp.name, "rb")
            audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
