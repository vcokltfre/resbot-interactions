from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from discord_interactions import verify_key, InteractionResponseType, InteractionType

from json import dumps

from src.models import Interaction
from config import PUBKEY

app = FastAPI(docs_url=None)

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

    if data["type"] == InteractionType.APPLICATION_COMMAND:
        print(dumps(data))
        return {
            "type": InteractionResponseType.CHANNEL_MESSAGE,
            "data": {
                "content": "Test success!"
            }
        }