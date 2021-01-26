from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from discord_interactions import verify_key, InteractionResponseType,

from config import PUBKEY, roles

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

    rls = set(data["member"]["roles"]) & set(roles)

    if not rls:
        return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": "You do not have permissions to use this command!"
        }
    }

    ops = data["data"]["options"]
    action = ops[0]["value"]
    server = ops[1]["value"]
    mcname = ops[2]["value"]
    pgroup = ops[3]["value"] if len(ops) == 4 else None

    if action == "op_grant":
        content = f"Granted permission group {pgroup} on {server} to {mcname}"
    elif action == "op_revoke":
        content = f"Revoked permission group {pgroup} on {server} from {mcname}"
    else:
        content = "Not implemented"

    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": content
        }
    }