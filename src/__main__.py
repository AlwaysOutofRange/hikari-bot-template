import os

from core.bot import Bot

if os.name != "nt":
    import uvloop

    uvloop.install()

bot = Bot()
bot.run()
