# For The-TG-Bot v3
# By Priyam Kalra, originally for curtana
# Modified to work for any device, by @Techy05

from asyncio import sleep
from modules.sql.fetch_sql import get_chat, save


@client.on(events(pattern="fetch ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    input_str = event.pattern_match.group(1)
    split = input_str.split()
    if split[0] == "-d":  # Setting default chat
        try:
            if "@" in split[1]:
                new_chat = split[1]
                save(new_chat)
                await event.edit(f"`Default fetch channel has been changed to` {new_chat}")
                await sleep(5)
            else:
                await event.edit("Invalid channel tag")
                await sleep(5)
        except:
            old_chat = get_chat()
            for channel in old_chat:
                chat = channel.keyword
            await client.send_message(event.chat_id, f"`Default fetch chat is` {chat}")
            return
    else:
        args = f"#{split[0]}"
        old_chat = get_chat()
        if old_chat:
            for channel in old_chat:
                chat = channel.keyword
        else:
            await event.edit("No Default Device set yet! Use `.help fetch` to know more")
            await sleep(5)
    await event.delete()
    async for message in client.iter_messages(chat):
        msg = message.text
        if msg is None:
            msg = ""
        if args.lower() in msg.lower():
            result = message
            break
        else:
            result = f"Nothing found for {args} in {chat}"
    await client.send_message(
        event.chat_id,
        result,
        reply_to=reply,
        parse_mode="HTML",
        force_document=False,
        silent=True
    )
    

ENV.HELPER.update({
    "fetch": "\
`.fetch <rom/recovery/kernel name>`\
\nUsage: Returns the latest build of a custom rom/recovery/kernel for a device.\
\n\n**HOW TO SET DEFAULT DEVICE:**\
\nFind the Telegram Channel of your phone and copy its tag\
\n\n`. fetch -d <channel_tag>`\
\n__For eg: .fetch device @realme1updates__\
"
})
