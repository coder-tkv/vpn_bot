import os
import asyncio
import httpx
from marzban import MarzbanAPI, UserCreate, ProxySettings, UserModify
from datetime import datetime, timedelta
import logging


# Настройка логгера
log_format = "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
formatter = logging.Formatter(log_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

file_handler = logging.FileHandler("py_log.log", mode="w", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# API
api = MarzbanAPI(base_url=os.getenv('MARZBAN_HOST'))


class Controller:
    def __init__(self, token):
        self.logger = logging.getLogger(__name__)
        self.token = token

    @staticmethod
    def expire_timestamp(expire: datetime):
        new_utc_timestamp = int(expire.timestamp())
        return new_utc_timestamp

    async def add_user(self, name, expire):
        new_user = UserCreate(
            username=name,
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            expire=self.expire_timestamp(datetime.now() + timedelta(days=expire))
        )
        try:
            added_user = await api.add_user(user=new_user,
                                            token=self.token.access_token)
            self.logger.info(f"Добавлен пользователь: {added_user}")
            return True
        except httpx.HTTPStatusError as e:
            self.logger.error('HTTPStatusError', exc_info=True)
            return None

    async def get_user(self, name, log=True):
        try:
            user_info = await api.get_user(username=name,
                                           token=self.token.access_token)
            if log: self.logger.info(f"Получена информация о пользователе: {user_info}")
            return user_info
        except httpx.HTTPStatusError as e:
            self.logger.error('HTTPStatusError', exc_info=True)
            return None

    async def add_expire(self, name, expire):
        try:
            user = await self.get_user(name, log=False)

            modified_user = await api.modify_user(
                username=name,
                user=UserModify(
                    expire=self.expire_timestamp(datetime.fromtimestamp(user.expire) + timedelta(days=expire))
                ),
                token=self.token.access_token
            )
            self.logger.info(f"Изменен пользователь {modified_user}")
        except httpx.HTTPStatusError as e:
            self.logger.error('HTTPStatusError', exc_info=True)

    async def delete_user(self, name):
        try:
            await api.remove_user(username=name, token=self.token.access_token)
            self.logger.info(f"Пользователь удален: {name}")
        except httpx.HTTPStatusError as e:
            self.logger.error('HTTPStatusError', exc_info=True)

    async def get_connect(self, name):
        user = await self.get_user(name, log=False)
        if user:
            self.logger.info(f"Выдана ссылка для подключения пользователя {name}")
            return user.links[0]
        self.logger.error(f"Ошибка выдачи ссылки для подключения пользователя {name}")
        return None


async def start():
    token = await api.get_token(username=os.getenv('MARZBAN_USERNAME'), password=os.getenv('MARZBAN_PASSWORD'))
    controller = Controller(token)
    await controller.add_user('test', 80)
    await controller.get_user('test')
    print(await controller.get_connect('test'))
    await controller.add_expire('test', 60)
    await controller.delete_user('test')


if __name__ == '__main__':
    asyncio.run(start())
