import json
import aiohttp
import logging


class AvitoAPI:
    self_info = None
    user_id = None
    chat_id = 'u2i-kYQbFs2IueV9uqRYbnnqAw'

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
                self.self_info = self_info
                self.user_id = self_info['id']
                logging.info(f' user_id - {self.user_id}')
                return self_info

    async def get_history(self) -> list:
        """
         История чатов пользователя

        :return: messages_history
        """
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            async with session.get(url=f'https://api.avito.ru/messenger/v2/accounts/{self.user_id}/chats',
                                   headers=auth_token
                                   ) as response:
                data = await response.text()
                messages_history = json.loads(data)['chats']
                logging.info(f' confirmed {len(messages_history)} chats on a page')
                return messages_history

    async def message_read(self) -> None:
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            read_url = f'https://api.avito.ru/messenger/v1/accounts/{self.user_id}/chats/{self.chat_id}/read'
            async with session.get(url=read_url,
                                   headers=auth_token
                                   ) as response:
                data_status = response.status
                if data_status == 200:
                    logging.info(f' the last message from chat({self.chat_id}) has been read')
                else:
                    logging.error(f' problems with reading the last message from chat({self.chat_id})')

    async def last_message_get(self):
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            last_message_url = f'https://api.avito.ru/messenger/v2/accounts/{self.user_id}/chats/{self.chat_id}'
            async with session.get(url=last_message_url,
                                   headers=auth_token
                                   ) as response:
                data_last = await response.text()
                last_message = json.loads(data_last)['last_message']['content']['text']
            print(last_message)

    async def message_answer(self) -> dict:
        """
        Отправка сообщений на основе входящего текста по айди на тестовый диалог

        :return: success: информация об отправленном сообщении
        """
        async with aiohttp.ClientSession() as session:
            auth_token = await self.get_auth_token()
            send_url = f'https://api.avito.ru/messenger/v1/accounts/{self.user_id}/chats/{self.chat_id}/messages'
            message = {
                "message": {
                    "text": ''
                },
                "type": "text"
            }

            # answer = await chatGPT(last_message)
            async with session.post(url=send_url,
                                    json=message,
                                    headers=auth_token
                                    ) as response:
                data_send = await response.text()
                success = json.loads(data_send)
                return success
