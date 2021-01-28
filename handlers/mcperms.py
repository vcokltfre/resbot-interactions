from config import mcperms_roles
from src.core import respond_default, respond_ephemeral, getop, require

groups = {
    "group_builder": "Builder",
    "group_builder_plus": "Builder+",
    "group_ppa": "Private Project Access"
}


class MCPermsHandler:
    def __init__(self, http):
        self.http = http

    @staticmethod
    def msg_grant(group: str, server: str, mcname: str, member: str) -> str:
        group = groups[group]
        return f"Granted permission group `{group}` on server `{server}` to member <@{member}> (MCName: {mcname})"

    @staticmethod
    def msg_revoke(server: str, mcname: str) -> str:
        return f"Revoked permissions on server `{server}` from {mcname}"

    async def call(self, data: dict) -> dict:
        rls = set(data["member"]["roles"]) & set(mcperms_roles)

        if not rls:
            return respond_ephemeral("You do not have permission to use this command!")

        ops = data["data"]["options"]
        action = getop("type", ops)
        server = getop("server", ops)
        mcname = getop("mcname", ops)
        member = getop("member", ops)
        pgroup = getop("group", ops)

        if action == "op_grant":
            if not require(member, pgroup):
                return respond_ephemeral("You must select a group and member to grant permissions for.")
            content = self.msg_grant(group=pgroup, server=server, mcname=mcname, member=member)
        elif action == "op_revoke":
            content = self.msg_revoke(server=server, mcname=mcname)
        else:
            data = await self.http.get_user(server, mcname)
            content = str(data)

        return respond_default(content)