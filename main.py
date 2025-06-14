import os
import asyncio
from marzban import MarzbanAPI, UserCreate, ProxySettings
from datetime import datetime, timedelta

api = MarzbanAPI(base_url=os.getenv('MARZBAN_HOST'))

def expire_timestamp(expire: datetime):
    new_utc_timestamp = int(expire.timestamp())
    return new_utc_timestamp

class Controller:
    def __init__(self, token):
        self.token = token

    async def add_user(self, name, expire):
        new_user = UserCreate(
            username=name,
            proxies={"vless": ProxySettings(flow="xtls-rprx-vision")},
            expire=expire_timestamp(datetime.now() + timedelta(days=expire))
        )
        added_user = await api.add_user(user=new_user, token=self.token.access_token)
        print("Добавленный пользователь: ", added_user)


async def main():
    token = await api.get_token(username=os.getenv('MARZBAN_USERNAME'), password=os.getenv('MARZBAN_PASSWORD'))
    user = Controller(token)
    await user.add_user('test', 30)


asyncio.run(main())
