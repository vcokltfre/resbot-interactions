from re import compile

from src.core import respond_ephemeral, getop

link = compile(r"https://(canary\.|ptb\.)?discord\.com/channels/\d{17,20}/\d{17,20}/\d{17,20}/?")


class ReportHandler:
    def __init__(self, http):
        self.http = http

    async def call(self, data: dict) -> dict:
        ops = data["data"]["options"]
        ml = getop("link", ops)
        reason = getop("reason", ops)

        ml = link.search(ml)
        if ml:
            ml = ml.group()
        else:
            return respond_ephemeral("That is not a valid Discord message link!")

        id = data["member"]["user"]["id"]
        msg = f"User <@{id}> ({id}) reported message <{ml}> for:\n```\n{reason[:1500]}\n```"

        print(await self.http.report(msg))

        return respond_ephemeral("The message has been reported to the staff team!")