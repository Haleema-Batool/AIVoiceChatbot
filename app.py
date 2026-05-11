

# Get API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq model
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192"
# Speech recognizer
recognizer = sr.Recognizer()

# Text-to-speech engine
engine = pyttsx3.init()

# Streamlit UI
st.title("AI Voice Chatbot")
st.write("Speak with AI using LangChain + Groq")

# Function to speak text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen

def listen_voice():
    with sr.Microphone() as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Sorry, I could not understand."

    except sr.RequestError:
        return "Speech service error."

# Button
if st.button("Start Talking"):

    user_text = listen_voice()

    st.write("You:", user_text)

    # Send to AI
    response = llm.invoke([
        HumanMessage(content=user_text)
    ])

    ai_response = response.content

    st.write("AI:", ai_response)

    # Speak AI response
    speak_text(ai_response)
