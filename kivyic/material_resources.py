# -*- coding: utf-8 -*-
from kivy import platform
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd import fonts_path

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