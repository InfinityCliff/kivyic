# -*- coding: utf-8 -*-
import os
from kivy import Logger
__version_info__ = (0, 0, 0)
__version__ = '0.0.0'

path = os.path.dirname(__file__)
#fonts_path = os.path.join(path, "fonts/")
#images_path = os.path.join(path, 'images/')

Logger.info("KivyIC: KivyIC version: {}".format(__version__))