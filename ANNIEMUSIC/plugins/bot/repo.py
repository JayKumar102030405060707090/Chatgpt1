from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ANNIEMUSIC import app
from config import BOT_USERNAME




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
     
            [ 
            InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ ʙᴀʙᴇs✪", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
            ],
     
            [
             InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/INNOCENT_FUCKER"),
             InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/YARO_KA_ADDAA"),
             ],
     
             [
             #InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ", url="https://t.me/RADHA_MUSIC_SUPPORT"),          
             #InlineKeyboardButton("︎ᴍᴜsɪᴄ", url=f"https://github.com/Naincysoni21/Radhamusic"),
             ],
     
              ]
 
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://envs.sh/y9e.mp4",
        caption=start_txt,
        reply_markup=reply_markup
    )
