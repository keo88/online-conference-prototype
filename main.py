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
import urllib

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
    message = input()
    if message == 'exit':
        break
    
    named_message = f"Person {current_participant}: " + message
    print(named_message)
    conversation.predict(input=named_message)

    last_ai_message = k['history'][-1].content
    print(last_ai_message)

    if 'search' in last_ai_message:
        try:
            splitted = last_ai_message.split(' ')
            joined_msg = ' '.join(splitted[1:])[1:-1]
            target_url = f'https://www.google.com/search?q={urllib.parse.quote(joined_msg)}'
            webbrowser.open(target_url)
        except:
            pass

    current_participant = (current_participant + 1) % participants