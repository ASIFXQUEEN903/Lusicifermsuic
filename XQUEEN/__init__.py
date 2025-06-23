from XQUEEN.core.bot import Sona
from XQUEEN.core.dir import dirr
from XQUEEN.core.git import git
from XQUEEN.core.userbot import Userbot
from XQUEEN.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Sona()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
