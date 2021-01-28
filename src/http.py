from aiohttp import ClientSession

from bot_secrets.config import TOKEN, CHANNEL, MC_TOKEN

BASE = "https://discord.com/api/v8"
MCPBASE = "https://mcperms.mcatho.me/mcserver"

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

    async def get_user(self, server: str, userid: str):
        async with self.sess.get(MCPBASE + f"/{server}/{userid}", headers={"auth":MC_TOKEN}) as resp:
            if resp.status > 299:
                return False
            return await resp.json()

    async def grant_perms(self, server: str, group: str, userid: str, mcname: str):
        async with self.sess.post(MCPBASE + f"/{server}/{group}/{userid}/{mcname}", headers={"auth":MC_TOKEN}) as resp:
            if resp.status > 299:
                return False
            return await resp.json()

    async def revoke_perms(self, server: str, userid: str,):
        async with self.sess.delete(MCPBASE + f"/{server}/{userid}", headers={"auth":MC_TOKEN}) as resp:
            if resp.status > 299:
                return False
            return await resp.json()