# For The-TG-Bot v3
# Syntax .id

from telethon.utils import pack_bot_file_id as BotAPI


@client.on(events(pattern="id"))
async def handler(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    msg = f"Current Chat ID: `{event.chat_id}`\n"
    if reply:
        msg += f"From User ID: `{reply.from_id}`\n"
        if reply.fwd_from:
            msg += f"Forwarded from: `{reply.fwd_from.from_id}`\n"
        if reply.media:
            botapi_id = BotAPI(reply.media)
            msg += f"Bot API File ID: `{botapi_id}`"
    await event.edit(msg)


ENV.HELPER.update({"id": "\
`.id (as a reply)`\
\nUsage: Prints the current chat ID.\
\n\nAlso prints replied user ID, Forwarded from user ID, Bot API like file id.\
"})
