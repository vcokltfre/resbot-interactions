from discord_interactions import InteractionResponseType

def respond_default(message: str) -> dict:
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": message
        }
    }

def getop(name: str, ops: list):
    for op in ops:
        if op["name"] == name:
            return op["value"]
    return None