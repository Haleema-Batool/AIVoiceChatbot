
import streamlit as st
from dotenv import load_dotenv
import os
from gtts import gTTS
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import tempfile

# Load environment variables
load_dotenv()

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
)

# Streamlit UI
st.title("AI Voice Chatbot")
st.write("LangChain + Groq Voice Assistant")

# User input
user_input = st.text_input("Enter your message")

if st.button("Send"):

    if user_input:

        # Send message to AI
        response = llm.invoke([
            HumanMessage(content=user_input)
        ])

        ai_response = response.content

        # Show response
        st.write("AI:", ai_response)

        # Convert text to speech
        tts = gTTS(text=ai_response, lang="en")

        # Save temporary mp3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:

            tts.save(fp.name)

            audio_file = open(fp.name, "rb")

            audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
