# -*- coding: utf-8 -*-
from kivy.lang import Builder

from kivyic import path
from kivymd.label import MDLabel
from kivy.properties import StringProperty

Builder.load_file(path + '/label.kv')


class ICIconLabel(MDLabel):
    icon = StringProperty('checkbox-blank-circle')
