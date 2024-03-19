import asyncio
import json

import aiohttp

from src.settings import KEYS, HEADERS


async def get_history(keys):
    async with aiohttp.ClientSession() as session:
        auth_token = get_auth_token
        async with session.get(url=f'https://api.avito.ru/messenger/v2/accounts/{keys["client_id"]}/chats',
                               headers=auth_token
                               ) as response:
            html = await response.text()
            print(html)


async def get_auth_token(keys, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'https://api.avito.ru/token/',
                                data=keys,
                                headers=headers) as response:
            data = await response.text()
            auth_token = json.loads(data)['access_token']
            return auth_token

asyncio.run(get_auth_token(KEYS, HEADERS))
