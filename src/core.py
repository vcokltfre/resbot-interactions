from discord_interactions import InteractionResponseType, InteractionResponseFlags

def respond_default(message: str) -> dict:
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {
            "content": message,
            "allowed_mentions":{
                "users": False
            }
        }
    }

def respond_ephemeral(message: str) -> dict:
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE,
        "data": {
            "content": message,
            "allowed_mentions":{
                "users": False
            },
            "flags": InteractionResponseFlags.EPHEMERAL
        }
    }

def getop(name: str, ops: list):
    for op in ops:
        if op["name"] == name:
            return op["value"]
    return None

def require(*things):
    for thing in things:
        if not thing:
            return False
    return True