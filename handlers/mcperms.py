from config import roles
from src.core import respond_default, getop


class MCPermsHandler:
    def __init__(self):
        pass

    async def call(self, data: dict) -> dict:
        rls = set(data["member"]["roles"]) & set(roles)

        if not rls:
            return respond_default("You do not have permissions to use this command!")

        ops = data["data"]["options"]
        action = getop("type", ops)
        server = getop("server", ops)
        mcname = getop("mcname", ops)
        member = getop("member", ops)
        pgroup = getop("group", ops)

        if action == "op_grant":
            if (not pgroup) or not member:
                return respond_default("You must select a group and member to grant permissions for.")
            content = f"Granted permission group {pgroup} on {server} to {mcname} ({member['user']['id']})."
        elif action == "op_revoke":
            content = f"Revoked permission group {pgroup} on {server} from {mcname}."
        else:
            content = "Not implemented."

        return respond_default(content)