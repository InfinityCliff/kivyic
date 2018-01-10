# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivyic import path
from kivyic.label import ICIconLabel

from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty

__all__ = ['ICIconButton']
__version__ = '0.1'

Builder.load_file(path + '/button.kv')


class ICBaseButton(ButtonBehavior, Label):
    pass


class ICIconButton(ButtonBehavior, ICIconLabel):
    icon = StringProperty('checkbox-blank-circle')


class ICRoundedButton(ICBaseButton):
    pass
