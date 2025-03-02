import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import AccessTokenExpired, AccessTokenInvalid
from ANNIEMUSIC.utils.database import get_assistant
from ANNIEMUSIC.utils.clonedb import clonebotdb  # Fix: Correct import path
from config import API_ID, API_HASH, LOG_GROUP_ID
from ANNIEMUSIC import app
from ANNIEMUSIC.misc import SUDOERS

CLONES = set()

@app.on_message(filters.command("clone") & SUDOERS)
async def clone_txt(client: Client, message: Message):
    """Clone a bot using a token."""
    userbot = await get_assistant(message.chat.id)

    if len(message.command) < 2:
        await message.reply_text("**⚠️ Provide a bot token after /clone command.**")
        return

    bot_token = message.text.split("/clone", 1)[1].strip()
    processing_msg = await message.reply_text("🔄 Processing bot token...")

    try:
        ai = Client(
            f"clone-{bot_token}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=bot_token,
            plugins=dict(root="ANNIEMUSIC/plugins"),
        )
        await ai.start()
        bot = await ai.get_me()

    except (AccessTokenExpired, AccessTokenInvalid):
        await processing_msg.edit_text("❌ Invalid bot token. Please provide a valid one.")
        return
    except Exception as e:
        await processing_msg.edit_text(f"⚠️ Error: `{str(e)}`")
        return

    await processing_msg.edit_text("✅ Cloning process started, please wait...")

    try:
        await app.send_message(LOG_GROUP_ID, f"**#New_Clone**\n\n**Bot:** @{bot.username}")
        await userbot.send_message(bot.username, "/start")

        details = {
            "bot_id": bot.id,
            "user_id": message.from_user.id,
            "name": bot.first_name,
            "token": bot_token,
            "username": bot.username,
        }
        await clonebotdb.insert_one(details)
        CLONES.add(bot.id)

        await processing_msg.edit_text(f"✅ Bot @{bot.username} cloned successfully!\n\nUse `/delclone` to remove.")
    except Exception as e:
        logging.exception("Error while cloning bot")
        await processing_msg.edit_text(f"⚠️ Error: `{e}`\nPlease report this issue.")

@app.on_message(filters.command(["deletecloned", "delclone"]) & SUDOERS)
async def delete_cloned_bot(client: Client, message: Message):
    """Delete a cloned bot."""
    if len(message.command) < 2:
        await message.reply_text("⚠️ Provide the bot token after the command.")
        return

    bot_token = message.command[1].strip()
    cloned_bot = await clonebotdb.find_one({"token": bot_token})

    if not cloned_bot:
        await message.reply_text("❌ No cloned bot found with this token.")
        return

    await clonebotdb.delete_one({"token": bot_token})
    CLONES.discard(cloned_bot["bot_id"])

    await message.reply_text(f"✅ Bot @{cloned_bot['username']} has been removed.")

@app.on_message(filters.command("clones") & SUDOERS)
async def list_cloned_bots(client: Client, message: Message):
    """List all cloned bots."""
    cloned_bots_list = await clonebotdb.find().to_list(length=100)

    if not cloned_bots_list:
        await message.reply_text("⚠️ No bots have been cloned yet.")
        return

    text = f"**Total Cloned Bots:** {len(cloned_bots_list)}\n\n"
    for bot in cloned_bots_list:
        text += f"🔹 **Bot:** @{bot['username']} | **ID:** {bot['bot_id']}\n"

    await message.reply_text(text)
