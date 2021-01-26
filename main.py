from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from discord_interactions import verify_key

from src.models import Interaction
from config import pubkey

app = FastAPI(docs_url=None)

@app.post("/interactions")
async def interactions(req: Request):
    body = await req.body()
    sig = req.headers["X-Signature-Ed25519"]
    ts = req.headers["X-Signature-Timestamp"]

    if not verify_key(body, sig, ts, pubkey):
        raise HTTPException(400)

    print(await req.json())