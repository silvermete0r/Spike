import speech_recognition as sr
import pyttsx3
import openai
import json

# OpenAI API Key Setup
openai.api_key = 'YOUR_API_KEY'

# Load JSON commands
with open('commands.json', 'r') as json_file:
    commands = json.load(json_file)

# Text to Speech using pyttsx3
def SpeakText(command):
    engine = pyttsx3.init('sapi5')
    engine.say(command)
    engine.runAndWait()

# Generate GPT response
def gpt_response(command):
    user_message = "User Response: " + command + "\n"

    chatbot_message = """
     - You are a chatbot that can answer questions about the city of Astana, you can also answer questions about the weather, the time, the date, the location of the nearest cafe, the location of the nearest hotel, the location of the nearest hospital, the location of the nearest police station, the location of the nearest pharmacy, the location of the nearest shopping center, the location of the nearest park, the location of the nearest museum, the location of the nearest cinema, the location of the nearest theater, the location of the nearest library, the location of the nearest school, the location of the nearest university, the location of the nearest stadium, the location of the nearest mosque, the location of the nearest church, the location of the nearest synagogue, the location of the nearest gas station, the location of the nearest bank, the location of the nearest ATM, the location of the nearest bus stop, the location of the nearest train station, the location of the nearest airport.
    """

    chat_history = chatbot_message + user_message

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=chat_history,
        max_tokens=50,
        temperature=0.8,
        top_p=1.0,
        n=1,
        stop=None,
        temperature_decay_rate=0.9
    )

    chatbot_reply = response.choices[0].text.strip().split("Elon Musk GPT: ")[1]

    return chatbot_reply

# Generate response for user
def generate_response(command):
    if command in commands:
        return commands[command]
    else:
        return gpt_response(command)

def TakeCommand():
    # Initialize the recognizer
    try:
        recognizer = sr.Recognizer()

        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

            # Recognize speech using Google Web Speech API
            try:
                text = recognizer.recognize_google(audio)
                print("User said: {}".format(text))
                answer = generate_response(text)
                SpeakText(answer)
            except sr.UnknownValueError:
                print("Sorry, I could not understand you!")
            except sr.RequestError as e:
                print("Error with the request; {0}".format(e))
    except:
        print("Something went wrong!")

def main():
    while True:
        TakeCommand()

if __name__ == '__main__':
    main()