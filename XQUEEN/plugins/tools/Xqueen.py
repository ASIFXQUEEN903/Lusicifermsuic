from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from BrandrdXMusic import app


@app.on_message(filters.command("repo"))
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/1aac9a42f6f35138da34b.jpg",
        caption="""
𓆩🍁𓆪 𝐇𝐞𝐲 𝐁𝐚𝐛𝐲 💞

𓍯 𝐂𝐋𝐈𝐂𝐊 𝐎𝐍 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍 𝐁𝐄𝐋𝐎𝐖 𝐓𝐎 𝐆𝐄𝐓 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓'𝐒 𝐒𝐎𝐔𝐑𝐂𝐄 💫

𓆩🩷 𝐌𝐀𝐃𝐄 𝐖𝐈𝐓𝐇 𝐋𝐎𝐕𝐄 𝐁𝐘 𝐗𝐐𝐔𝐄𝐄𝐍 𓆪
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𓆩⚡ 𝙊𝙋𝙀𝙉 𝙍𝙀𝙋𝙊 ⚡𓆪", url="https://github.com/WCGKING/BrandrdXMusic"
                    )
                ]
            ]
        ),
    )


__MODULE__ = "Sᴏᴜʀᴄᴇ"
__HELP__ = """
## 🌀 Rᴇᴘᴏ Mᴏᴅᴜʟᴇ

➤ `/repo` – Get the stylish source code repo of this bot.
"""
