import asyncio
import logging
import os
import sys
from pprint import pprint

from dotenv import load_dotenv
from pathlib import Path

from src.avitoAPI import AvitoAPI

BASE_DIR = Path(__file__).parent
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)


async def main():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    avito_api = AvitoAPI(client_id, client_secret)
    auth_token = await avito_api.get_auth_token()
    pprint(auth_token)
    self_info = await avito_api.get_self_info()
    pprint(self_info['id'])
    text = 'Test AvitoAPI'
    await avito_api.send_message(text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
