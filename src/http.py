from aiohttp import ClientSession

from bot_secrets.config import TOKEN, CHANNEL

BASE = "https://discord.com/api/v8"


class HTTP:
    def __init__(self):
        self.sess = ClientSession(headers={'Authorization': f'Bot {TOKEN}'})

    async def init(self):
        if self.sess.closed:
            self.sess = ClientSession(headers={'Authorization': f'Bot {TOKEN}'})

    async def send_message(self, channel: str, message: str):
        async with self.sess.post(BASE + f"/channels/{channel}/messages", json={"content":message}) as resp:
            return await resp.json()

    async def report(self, message: str):
        return await self.send_message(CHANNEL, message)