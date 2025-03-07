import os
import asyncio
import motor.motor_asyncio
from pyrogram import Client
from pymongo import MongoClient
from config import MONGO_DB_URI, CLONE_FOLDER

# Database Setup
client = MongoClient(MONGO_DB_URI)
db = client["MusicBot"]
clones_collection = db["cloned_bots"]

async def clone_bot(bot_token, owner_id):
    """ Clone a new bot and store it in the database """
    
    # Check if the bot is already cloned
    existing_bot = clones_collection.find_one({"bot_token": bot_token})
    if existing_bot:
        return f"🚫 Bot already cloned with ID: {existing_bot['_id']}"

    # Validate bot token
    try:
        bot = Client("temp_session", bot_token=bot_token)
        await bot.start()
        bot_info = await bot.get_me()
        await bot.stop()
    except Exception as e:
        return f"❌ Invalid bot token: {str(e)}"

    # Clone bot in database
    clone_data = {
        "_id": bot_info.id,
        "bot_token": bot_token,
        "username": bot_info.username,
        "owner_id": owner_id,
        "created_at": asyncio.get_event_loop().time()
    }
    clones_collection.insert_one(clone_data)

    return f"✅ Successfully cloned @{bot_info.username}!"

async def delete_clone(bot_token, owner_id):
    """ Delete a cloned bot """
    clone = clones_collection.find_one({"bot_token": bot_token, "owner_id": owner_id})
    if not clone:
        return "❌ No cloned bot found for this token."

    clones_collection.delete_one({"bot_token": bot_token})
    return f"✅ Clone bot @{clone['username']} has been deleted!"

async def get_my_bots(owner_id):
    """ Get a list of user's cloned bots """
    user_bots = clones_collection.find({"owner_id": owner_id})
    if not user_bots:
        return "❌ You have no cloned bots."

    bots_list = "\n".join([f"- @{bot['username']}" for bot in user_bots])
    return f"👥 Your Cloned Bots:\n{bots_list}"

async def total_cloned_bots():
    """ Get total number of cloned bots """
    count = clones_collection.count_documents({})
    return f"📊 Total Cloned Bots: {count}"
