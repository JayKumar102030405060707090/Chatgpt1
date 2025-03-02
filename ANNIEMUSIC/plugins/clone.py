from config import API_ID, API_HASH
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["clone"], prefixes=["."]))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply_text("**⚠️ Usage:** `.clone <session_string>`")

    session_string = msg.command[1]

    text = await msg.reply_text("🔄 Booting your client... Please wait!")
    
    try:
        client = Client(
            name="ANNIEMUSIC",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            plugins=dict(root="ANNIEMUSIC/plugins/bot")
        )
        await client.start()
        user = await client.get_me()

        await text.edit_text(
            f"✅ **Clone Successful!**\n\n"
            f"**Name:** {user.first_name}\n"
            f"**Username:** @{user.username if user.username else 'No Username'}"
        )

    except Exception as e:
        await text.edit_text(
            f"❌ **Error:** `{str(e)}`\n\n"
            "Please ensure the session string is valid."
        )
