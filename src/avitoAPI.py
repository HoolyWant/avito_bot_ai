import asyncio
import json

import aiohttp

from src.settings import KEYS


async def get_history(keys):
    async with aiohttp.ClientSession() as session:
        auth_token = get_auth_token
        async with session.get(url=f'https://api.avito.ru/messenger/v2/accounts/{keys["client_id"]}/chats',
                               headers=auth_token
                               ) as response:
            html = await response.text()
            print(html)


async def get_auth_token(keys):
    async with aiohttp.ClientSession() as session:
        json_keys = json.dumps(keys)
        async with session.post(url=f'https://api.avito.ru/token',
                                data=json_keys) as response:
            html = await response.text()
            print(html)

asyncio.run(get_auth_token(KEYS))
