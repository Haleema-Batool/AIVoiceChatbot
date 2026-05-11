
import streamlit as st
from dotenv import load_dotenv
import os
from gtts import gTTS
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import tempfile

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check API key
if not GROQ_API_KEY:
    st.error("Groq API key not found. Please check your .env file or Streamlit Secrets.")
    st.stop()

# Initialize Groq model
try:
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama3-8b-8192"
    )
except Exception as e:
    st.error(f"Error initializing Groq model: {e}")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="AI Voice Chatbot")

st.title("AI Voice Chatbot")
st.write("LangChain + Groq + Streamlit")

# User input
user_input = st.text_input("Type your message")

# Send button
if st.button("Send"):

    if user_input.strip() == "":
        st.warning("Please enter a message.")

    else:

        try:
            # Send message to AI
            response = llm.invoke([
                HumanMessage(content=user_input)
            ])

            ai_response = response.content

            # Display AI response
            st.success(ai_response)

            # Convert text to speech
            tts = gTTS(text=ai_response, lang="en")

            # Save temporary mp3
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:

                tts.save(fp.name)

                # Read audio file
                audio_file = open(fp.name, "rb")
                audio_bytes = audio_file.read()

                # Play audio
                st.audio(audio_bytes, format="audio/mp3")

        except Exception as e:
            st.error(f"Error: {e}")
