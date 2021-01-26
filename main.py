from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from discord_interactions import verify_key

from config import PUBKEY
from handlers.mcperms import MCPermsHandler
from src.core import respond_default

app = FastAPI(docs_url=None)

handlers = {
    "mcperms": MCPermsHandler()
}

@app.post("/interactions")
async def interactions(req: Request):
    body = await req.body()
    sig = req.headers["X-Signature-Ed25519"]
    ts = req.headers["X-Signature-Timestamp"]

    if not verify_key(body, sig, ts, PUBKEY):
        raise HTTPException(400)

    data = await req.json()

    if data["type"] == 1:
        return {"type":1}

    if name := data["data"]["name"] in handlers:
        try:
            return await handlers[name].call(data)
        except:
            return respond_default("An error occurred while processing the command.")