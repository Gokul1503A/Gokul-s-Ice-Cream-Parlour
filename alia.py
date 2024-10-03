import ollama
from gtts import gTTS

convo = []

Flag = True

def StreamResponse(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model = 'alia', messages= convo, stream= True)
    

    for chunk in stream:
        content = chunk['message']['content']
        response += content
        convo.append({'role': 'assistant', 'content': response})
    tts = gTTS(response, lang='en', tld='co.in')
    tts.save('response.mp3')
    


    

