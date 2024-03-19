import json
import aiohttp


class AvitoAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.data = {
            'keys': {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'},
            'headers': {
                'Content_type': 'application/x-www-form-urlencoded'}
        }

    def __str__(self):
        return f'client - {self.client_id}'

    async def get_auth_token(self) -> dict:
        """
        Получение headers с access токеном
        для отправки запросов на Авито API

        :return: headers
        """
        async with aiohttp.ClientSession() as session:
            keys = self.data['keys']
            headers = self.data['headers']
            async with session.post(url=f'https://api.avito.ru/token/',
                                    data=keys,
                                    headers=headers) as response:
                data = await response.text()
                auth_token = json.loads(data)['access_token']
                headers = {
                    'Authorization': f'Bearer {auth_token}',
                    'Content_type': 'application/json'
                }
                return headers

    async def get_self_info(self) -> dict:
        """
        Информация о профиле, в том числе id

        :return: self_info
        """
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            async with session.get(url=f'https://api.avito.ru/core/v1/accounts/self',
                                   headers=auth_token) as response:
                data = await response.text()
                self_info = json.loads(data)
                return self_info

    async def get_history(self) -> list:
        """
         История чатов пользователя

        :return: messages_history
        """
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            self_info = await self.get_self_info()
            user_id = self_info['id']
            async with session.get(url=f'https://api.avito.ru/messenger/v2/accounts/{user_id}/chats',
                                   headers=auth_token
                                   ) as response:
                data = await response.text()
                messages_history = json.loads(data)['chats']
                return messages_history

    async def send_message(self, text: str) -> dict:
        """
        Отправка сообщений на основе входящего текста по айди на тестовыы диалог

        :param text: текст сообщения
        :return: success: информация об отправленном сообщении
        """
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            self_info = await self.get_self_info()
            user_id = self_info['id']
            # messages_history = await self.get_history()
            chat_id = 'u2i-kYQbFs2IueV9uqRYbnnqAw'
            message = {
                    "message": {
                        "text": text
                    },
                    "type": "text"
            }

            async with session.post(url=f'https://api.avito.ru/messenger/v1/accounts/'
                                        f'{user_id}/chats/{chat_id}/messages',
                                    json=message,
                                    headers=auth_token
                                    ) as response:
                data = await response.text()
                success = json.loads(data)
                return success

