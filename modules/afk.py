# For The-TG-Bot v3
# Syntax (.afk <optional reason>)

import asyncio
import datetime
from telethon.tl.functions.account import GetPrivacyRequest
from telethon.tl.types import InputPrivacyKeyStatusTimestamp


client.storage.USER_AFK = {}
client.storage.afk_time = None
client.storage.last_afk_message = {}

@client.on(events(outgoing=True))
async def set_not_afk(event):
    current_message = event.message.text.lower()
    if "afk" not in current_message and "yes" in client.storage.USER_AFK:
        time = afk_time() if client.storage.afk_time else "a while"
        msg = await client.send_message(event.chat_id, f"No more AFK!\n`was AFK for {time}`", silent=True)
        
        client.storage.USER_AFK = {}
        client.storage.afk_time = None
        if event.chat_id in client.storage.last_afk_message:
            await client.storage.last_afk_message[event.chat_id].delete()
        await asyncio.sleep(2)
        await msg.delete()
        

@client.on(events(pattern="afk ?(.*)"))
async def handler(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    if not client.storage.USER_AFK:
        client.storage.afk_time = datetime.datetime.now()
        client.storage.USER_AFK.update({"yes": reason})
        if reason:
            await event.edit(f"**I'm goin' AFK**, __cuz {reason}.__")
        else:
            await event.edit(f"**I'm goin' AFK.**")
            

@client.on(events(incoming=True, func=lambda e: bool(e.mentioned or e.is_private)))
async def on_afk(event):
    if event.fwd_from:
        return
    current_message_text = event.message.text.lower()
    if "afk" in current_message_text:
        return False
    if client.storage.USER_AFK and not (await event.get_sender()).bot:
        reason = client.storage.USER_AFK["yes"]
        chat_id = str(event.chat_id).replace("-100", "")
        user_id = event.from_id
        if await privacy(int(chat_id), user_id):
            afk_since = afk_time()
        else:
            afk_since = "a while ago"
        if reason:
            message_to_reply = f"**I have been AFK** since {afk_since}\n`cuz {reason}`\n\n__Feel free to chat with this bot as long as you like.__" 
        else:
            message_to_reply = f"**I have been AFK** since {afk_since}\n\n__Feel free to chat with this bot as long as you like.__"
        msg = await event.reply(message_to_reply)
        await asyncio.sleep(1)
        if event.chat_id in client.storage.last_afk_message:
            await client.storage.last_afk_message[event.chat_id].delete()
        client.storage.last_afk_message[event.chat_id] = msg


def afk_time():
    now = datetime.datetime.now()
    datime_since_afk = now - client.storage.afk_time
    time = float(datime_since_afk.seconds)
    days = time // (24 * 3600)
    time = time % (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    if days == 1:
        afk_since = "yesterday"
    elif days > 1:
        if days > 6:
            date = now + datetime.timedelta(
                days=-days, hours=-hours, minutes=-minutes)
            afk_since = date.strftime("%A, %Y %B %m, %H:%I")
        else:
            wday = now + datetime.timedelta(days=-days)
            afk_since = wday.strftime('%A')
    elif hours > 1:
        afk_since = f"{int(hours)}h {int(minutes)}m"
    elif minutes > 0:
        afk_since = f"{int(minutes)}m {int(seconds)}s"
    else:
        afk_since = f"{int(seconds)}s"
    return afk_since


"""Only the people who can see "last seen" time, 
will be able to see "afk time"""

async def privacy(chat_id, user_id):
    status = await client(GetPrivacyRequest(InputPrivacyKeyStatusTimestamp()))
    if "DisallowAll" in str(status.rules):
        for term in status.rules:
            if "PrivacyValueAllowUsers" in str(term):
                whiteusers = term.users
                for id in whiteusers:
                    if id == user_id:
                        return True
            if "PrivacyValueAllowChatParticipants" in str(term):
                whitechats = term.chats
                for id in whitechats:
                    if id == chat_id:
                        return True
        return False
    elif "AllowAll" in str(status.rules):
        for term in status.rules:
            if "PrivacyValueDisallowUsers" in str(term):
                blackusers = term.users
                for id in blackusers:
                    if id == user_id:
                        return False
            if "PrivacyValueDisallowChatParticipants" in str(term):
                blackchats = term.chats
                for id in blackchats:
                    if id == chat_id:
                        return False
        return True
        

ENV.HELPER.update({"afk": "\
`.afk <optional_reason>`\
\nUsage: Automatically replies to PMs and mentions while you're away.\
"})
