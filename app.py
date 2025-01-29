import gradio as gr
import speech_recognition as sr
from gtts import gTTS
import os
import openai

# Your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Function to convert audio to text using SpeechRecognition
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)
    
    with audio_data as source:
        audio = recognizer.record(source)
        
    try:
        user_text = recognizer.recognize_google(audio)
        print("🔹 Extracted text:", user_text)  # Print the extracted text
        return user_text
    except sr.UnknownValueError:
        print("🔹 Couldn't understand the audio")
        return "I didn't understand what you said"
    except sr.RequestError:
        print("🔹 Error connecting to Google API")
        return "Error connecting to the API"

# Function to interact with the ChatGPT API
def chat_with_gpt(user_text):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}],
    )
    ai_response = response['choices'][0]['message']['content']
    print("🔹 ChatGPT response:", ai_response)  # Print the response from ChatGPT
    return ai_response

# Function to convert text to speech using gTTS
def text_to_speech(ai_response):
    tts = gTTS(text=ai_response, lang='ar')
    audio_file = "response.mp3"
    tts.save(audio_file)
    print("🔹 Audio saved at:", audio_file)  # Print the audio file name
    return audio_file

# Main function to record audio, convert it to text, and send the text to ChatGPT
def voice_chat(audio):
    # Convert audio to text
    user_text = transcribe_audio(audio)
    
    # Send the text to ChatGPT and get the response
    ai_response = chat_with_gpt(user_text)
    
    # Convert the response to audio
    response_audio = text_to_speech(ai_response)
    
    return user_text, response_audio

# User interface using Gradio
text_reply = gr.Textbox(label="ChatGPT Text")
voice_reply = gr.Audio(label="Audio Response")

gr.Interface(
    fn=voice_chat,
    inputs=[gr.Audio(source="microphone", type="filepath")],  # Audio input from the microphone
    outputs=[text_reply, voice_reply],  # Outputs are text and audio
    title='AI Voice Assistant with ChatGPT AI',
    live=True
).launch(debug=True)
