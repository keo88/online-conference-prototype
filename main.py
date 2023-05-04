from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
import webbrowser

import openai
import pyaudio
import keyboard
import wave
import keyboard

CHANNELS = 1
FRAME_RATE = 16000
RECORD_SECONDS = 20
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

def record_microphone(chunk=1024):
    print('Press r to start recording')
    while True:
        if keyboard.is_pressed('r'):
            sample_format = pyaudio.paInt16  # 16 bits per sample
            channels = 1
            fs = 44100  # Record at 44100 samples per second
            filename = "output.wav"

            p = pyaudio.PyAudio()  # Create an interface to PortAudio

            print('\nStart recording... Press r to stop recording')

            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            frames = []  # Initialize array to store frames

            while True:
                if keyboard.is_pressed('r'):
                    break
                data = stream.read(chunk)
                frames.append(data)

            # Stop and close the stream 
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()

            print('\nFinished recording')

            # Save the recorded data as a WAV file
            wf = wave.open('./'+filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            rf = open('./'+filename, 'rb')
            return rf
        

os.environ["OPENAI_API_KEY"] = open("./api_key.txt", "r").read().strip()
def read_agent():
    text_file = open("./agent.txt", "r")

    #read whole file to a string
    data = text_file.read()
    
    #close file
    text_file.close()
    
    return data

agent_prompt = read_agent()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(agent_prompt),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

llm = ChatOpenAI(temperature=0.7)
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

k = memory.load_memory_variables({})
participants = 2
current_participant = 0
        

while(True):
    audio = record_microphone()
    message = openai.Audio.transcribe("whisper-1", audio)['text']
    
    named_message = f"Person {current_participant}: " + message
    print(named_message)
    conversation.predict(input=named_message)

    last_ai_message = k['history'][-1].content
    print(last_ai_message)

    if last_ai_message == 'close meeting':
        break

    if 'search' in last_ai_message:
        try:
            splitted = last_ai_message.split(' ')
            joined_msg = ' '.join(splitted[1:])[1:-1].strip()
            webbrowser.open(f'https://www.google.com/search?q={joined_msg}')
        except:
            pass

    current_participant = (current_participant + 1) % participants
