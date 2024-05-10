import os
import speech_recognition as sr
import subprocess
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# Inicialización del reconocedor de voz
recognizer = sr.Recognizer()


def listen_to_speech():
    """Función para escuchar y transcribir la voz a texto."""
    with sr.Microphone() as source:
        print("Escuchando...")
        audio_data = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Reconocido: {text}")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return None
        except sr.RequestError as e:
            print(f"Error en el servicio de reconocimiento; {e}")
            return None


def speak(text):
    """Función para convertir texto a voz usando el comando `say` de macOS."""
    subprocess.run(["say", text])


def query_gpt(prompt, model="gpt-3.5-turbo", max_tokens=100):
    """Envía una pregunta al LLM y recibe la respuesta."""
    print(f"prompt: {prompt}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
        )
        answer = response.choices[0].message.content.strip()
        print(f"GPT Response: {answer}")
        return answer
    except Exception as e:
        print(f"Error al interactuar con GPT: {e}")
        return "Lo siento, ocurrió un error al procesar la respuesta."


def main():

    print("Interactive Voice Chat with GPT Model")
    speak("Bienvenido humano, haz tus preguntas y te responderé.")

    while True:
        prompt = listen_to_speech()
        if prompt:
            response = query_gpt(prompt)
            speak(response)
        else:
            speak("No entendí lo que dijiste. Intenta de nuevo.")


if __name__ == "__main__":
    main()
