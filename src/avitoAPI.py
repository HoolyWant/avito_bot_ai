import asyncio

import aiohttp

KEYS = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}
headers = {
    'Authorization': 'Bearer ' + CLIENT_SECRET
}


async def get_history(client_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'https://api.avito.ru/messenger/v2/accounts/{client_id}/chats',
                               headers=headers
                               ) as response:
            html = await response.text()
            print(html)

async def get_token():
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'https://api.avito.ru/token',
                               headers=headers
                               ) as response:
            html = await response.text()
            print(html)
