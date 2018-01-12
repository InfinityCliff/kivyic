# -*- coding: utf-8 -*-
from kivy import platform
from kivy.core.window import Window
from kivy.metrics import dp

from kivyic import ColorProperty

#__all__ = []
__version__ = '0.1'

if platform != "android" and platform != "ios":
    DEVICE_TYPE = "desktop"
elif Window.width >= dp(600) and Window.height >= dp(600):
    DEVICE_TYPE = "tablet"
else:
    DEVICE_TYPE = "mobile"

if DEVICE_TYPE == "mobile":
    MENU_ROW_HEIGHT = dp(48)
else:
    MENU_ROW_HEIGHT = dp(20)


# =====================================================================================
'''   Colors   '''
# =====================================================================================
SPOTIFY_GREY =          ColorProperty([40,   40,  40, 1])
SPOTIFY_LT_GREY =       ColorProperty([146, 154, 171, 1])
SPOTIFY_GREEN =         ColorProperty([29,  185,  84, 1])
SPOTIFY_BRT_GREEN =     ColorProperty([0,   255,   0, 1])
SPOTIFY_DARK_GREEN =    ColorProperty([29,  185,  84, .5])
SPOTIFY_TEXT =          ColorProperty([165, 160, 149, 1])
SPOTIFY_TEXT_ACTIVE =   ColorProperty([255, 255, 255, 1])
SPOTIFY_BUTTON =        ColorProperty([167, 167, 167, 1])
SPOTIFY_BUTTON_ACTIVE = SPOTIFY_GREEN
SPOTIFY_BUTTON_DOWN =   ColorProperty([255, 255, 255, 1])
SPOTIFY_PLAYLISTS =     ColorProperty([91,   81,  59, 1])
SPOTIFY_DAILY_MIX =     ColorProperty([14,  137, 114, 1])
SPOTIFY_SONGS =         ColorProperty([29,   50,  99, 1])
SPOTIFY_ALBUMS =        ColorProperty([68,   82,  77, 1])
SPOTIFY_ARTISTS =       ColorProperty([33,   46,  53, 1])

IC_BLUE =               ColorProperty([33,   150,  243, 1])
IC_SHADE_BLUE =         ColorProperty([197,  226,  249, 1])
IC_GREY =               ColorProperty([155,  155,  155, 1])
