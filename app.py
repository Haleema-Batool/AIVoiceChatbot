
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

# Check API key
if not GROQ_API_KEY:
    st.error("Groq API key not found")
    st.stop()

# Initialize Groq model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

# Streamlit page
st.set_page_config(page_title="AI Voice Chatbot")

# Title
st.title("AI Voice Chatbot")

st.write("LangChain + Groq + Voice AI")

# User input
user_input = st.text_input("Type your message")

# Send button
if st.button("Send"):

    if user_input.strip() != "":

        try:
            # AI response
            response = llm.invoke([
                HumanMessage(content=user_input)
            ])

            ai_response = response.content

            # Display response
            st.success(ai_response)

            # Convert text to speech
            tts = gTTS(text=ai_response, lang="en")

            # Save audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:

                tts.save(fp.name)

                audio_file = open(fp.name, "rb")

                audio_bytes = audio_file.read()

                # Play audio
                st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")
