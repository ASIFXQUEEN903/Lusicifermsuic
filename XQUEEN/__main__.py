import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from XQUEEN import LOGGER, app, userbot
from XQUEEN.core.call import Sona
from XQUEEN.misc import sudo
from XQUEEN.plugins import ALL_MODULES
from XQUEEN.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("XQUEEN.plugins" + all_module)
    LOGGER("XQUEEN.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Sona.start()
    try:
        await Sona.stream_call("https://files.catbox.moe/gjfzn9.mp4")
    except NoActiveGroupCall:
        LOGGER("XQUEEN").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Sona.decorators()
    LOGGER("XQUEEN").info(
        "KAMA HEIGALA EBE QUEEN KU TG ANA NAHELE AUU THARE BOT OFF KARIDEBI MADE BY XQUEEN"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("XQUEEN").info("Stopping DEEP Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
