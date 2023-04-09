from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.request import Request
from sanic import response

import re
import json
import httpx
import os
import openai

TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN"))
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()

app = Sanic(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

class ChatGPT:  
    

    def __init__(self):
        
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default = "gpt-3.5-turbo")



    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        

        response = openai.ChatCompletion.create(
	            model=self.model,
                messages = self.messages

                )

        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        
        print("AI回答內容：")        
        print(response['choices'][0]['message']['content'].strip())


        
        return response['choices'][0]['message']['content'].strip()

chatgpt = ChatGPT()


@app.route("/")
async def handle_request(request: Request) -> HTTPResponse:
    return response.text("Hello!")

@app.post("/callback")
async def callback(request: Request) -> HTTPResponse:
    data = json.loads(request.body)
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    ai_reply_response = chatgpt.get_response(text)  

    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={ai_reply_response}")

    return response.text("OK")

