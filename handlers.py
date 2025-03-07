from pyrogram import filters
from pyrogram.types import Message
from clone_manager import clone_bot, delete_clone, get_my_bots, total_cloned_bots
from bot import app

@app.on_message(filters.command("clone"))
async def clone_command(_, message: Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply("⚠️ Use: `/clone <bot_token>`")

    bot_token = args[1]
    result = await clone_bot(bot_token, message.from_user.id)
    await message.reply(result)

@app.on_message(filters.command("rmbot"))
async def remove_clone(_, message: Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply("⚠️ Use: `/rmbot <bot_token>`")

    bot_token = args[1]
    result = await delete_clone(bot_token, message.from_user.id)
    await message.reply(result)

@app.on_message(filters.command("mybot"))
async def my_clones(_, message: Message):
    result = await get_my_bots(message.from_user.id)
    await message.reply(result)

@app.on_message(filters.command("cloned"))
async def total_clones(_, message: Message):
    result = await total_cloned_bots()
    await message.reply(result)
