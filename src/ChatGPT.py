import asyncio
import os

import openai
from dotenv import load_dotenv
from main import dot_env

load_dotenv(dotenv_path=dot_env)


async def chatGPT(request):
    SECRET_KEY = os.getenv('CHAT_GPT_KEY')
    print(SECRET_KEY)
    openai.api_key = SECRET_KEY
    completion = openai.Completion.create(
        engine='gpt-3.5-turbo',
        prompt=request,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = completion.choices[0].text
    print(response)

asyncio.run(chatGPT('Hi'))
