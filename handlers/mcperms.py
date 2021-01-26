from config import roles
from src.core import respond_default


class MCPermsHandler:
    def __init__(self):
        pass

    async def call(self, data: dict) -> dict:
        rls = set(data["member"]["roles"]) & set(roles)

        if not rls:
            return respond_default("You do not have permissions to use this command!")

        ops = data["data"]["options"]
        action = ops[0]["value"]
        server = ops[1]["value"]
        mcname = ops[2]["value"]
        pgroup = ops[3]["value"] if len(ops) == 4 else None

        if action == "op_grant":
            if not pgroup:
                return respond_default("You must select a group to grant permissions for.")
            content = f"Granted permission group {pgroup} on {server} to {mcname}."
        elif action == "op_revoke":
            content = f"Revoked permission group {pgroup} on {server} from {mcname}."
        else:
            content = "Not implemented."

        return respond_default(content)