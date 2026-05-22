import speech_recognition as sr
import pyttsx3
from groq import Groq

# PUT YOUR GROQ API KEY HERE

client = Groq(api_key="YOUR API KEY")

# TEXT TO SPEECH SETUP

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # change index if needed

engine.setProperty('rate', 170)

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

# SPEECH TO TEXT SETUP

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("\n Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        speak("Speech service is not available.")
        return None


# CHAT MEMORY

messages = [
    {"role": "system", "content": "You are a helpful, friendly voice assistant."}
]


# MAIN LOOP

def main():
    speak("Hello! I am your AI Chatbot. Say exit to stop, How can I help you ?")

    while True:
        user_input = listen()

        if user_input is None:
            speak("Sorry, I didn't understand.")
            continue

        if "exit" in user_input.lower() or "stop" in user_input.lower():
            speak("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # UPDATED MODEL (WORKING)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )

            reply = response.choices[0].message.content

            messages.append({"role": "assistant", "content": reply})

            speak(reply)

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong.")

# RUN

if __name__ == "__main__":
    main()
