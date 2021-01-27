from aiohttp import ClientSession

from bot_secrets.config import TOKEN, CHANNEL

BASE = "https://discord.com/api/v8"

AM = {"allowed_mentions":{"users":False}}


class HTTP:
    def __init__(self):
        self.sess = ClientSession(headers={'Authorization': f'Bot {TOKEN}'})

    async def init(self):
        if self.sess.closed:
            self.sess = ClientSession(headers={'Authorization': f'Bot {TOKEN}'})

    async def request(self, method, url, json = {}):
        async with self.sess.request(method, BASE + url, json=json) as resp:
            return await resp.json()

    async def send_message(self, channel: str, message: str):
        return await self.request("POST", f"/channels/{channel}/messages", json={"content":message, **AM})

    async def report(self, message: str):
        return await self.send_message(CHANNEL, message)
