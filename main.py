from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from discord_interactions import verify_key, InteractionType, InteractionResponseType
from traceback import format_exc
from supress import supressed

from config import PUBKEY
from handlers.mcperms import MCPermsHandler
from handlers.report import ReportHandler
from src.core import respond_ephemeral
from src.http import HTTP

app = FastAPI(docs_url=None)

http = HTTP()

handlers = {
    "mcperms": MCPermsHandler(http),
    "report": ReportHandler(http)
}

@app.post("/interactions")
async def interactions(req: Request):
    body = await req.body()
    sig = req.headers["X-Signature-Ed25519"]
    ts = req.headers["X-Signature-Timestamp"]

    with supressed():
        verified = verify_key(body, sig, ts, PUBKEY)

    if not verified:
        raise HTTPException(400)

    data = await req.json()

    if data["type"] == InteractionType.PING:
        return {"type":InteractionResponseType.PONG}

    print(data)
    await http.init()

    name = data["data"]["name"]
    if name in handlers:
        try:
            return await handlers[name].call(data)
        except:
            return respond_ephemeral(f"An error occurred while processing the command:\n```py\n{format_exc(1900)}```")
    return respond_ephemeral("This command has not yet been implemented.")
