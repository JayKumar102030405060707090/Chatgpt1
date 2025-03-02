from ANNIEMUSIC.utils.database import mongodb

cloneownerdb = mongodb.cloneownerdb
clonebotdb = mongodb.clonebotdb
clonebotnamedb = mongodb.clonebotnamedb


# Save Clone Bot Owner
async def save_clonebot_owner(bot_id: int, user_id: int):
    """Save the owner of a cloned bot."""
    await cloneownerdb.insert_one({"bot_id": bot_id, "user_id": user_id})


async def get_clonebot_owner(bot_id: int):
    """Retrieve the owner of a cloned bot."""
    result = await cloneownerdb.find_one({"bot_id": bot_id})
    return result.get("user_id") if result else None


# Save Clone Bot Username
async def save_clonebot_username(bot_id: int, user_name: str):
    """Save the username of a cloned bot."""
    await clonebotnamedb.insert_one({"bot_id": bot_id, "user_name": user_name})


async def get_clonebot_username(bot_id: int):
    """Retrieve the username of a cloned bot."""
    result = await clonebotnamedb.find_one({"bot_id": bot_id})
    return result.get("user_name") if result else None
