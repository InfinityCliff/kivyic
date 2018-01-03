# -*- coding: utf-8 -*-
"""

"""
from kivy.app import App
from kivy.lang import Builder

from kivy.properties import (ObjectProperty, StringProperty, OptionProperty, NumericProperty,
                             ListProperty, BooleanProperty)
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import platform
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout


from kivymd.button import MDFlatButton, MDRaisedButton
from kivymd.button import MDIconButton
from kivymd.theming import ThemeManager, ThemableBehavior

from kivyic.dialog import ICDialog, DialogOKDismiss
from kivyic import path
import kivyic.material_resources as icm_res

import os

from functools import partial

__all__ = ('FileExplorer',)
__version__ = '0.0'
__events__ = ()

#Builder.load_file(path + '/menu.kv')


class TemplateClass(ThemableBehavior, BoxLayout):
    """

    """
    sort_key = None


class TemplateApp(App):
    """

    """
    theme_cls = ThemeManager()

    def build(self):
        #tc = FloatLayout(orientation='horizontal')
        tc = FloatLayout()
        b = Button(text='0',
                   size_hint=(None, None),
                   size=(30,30),
                   pos_hint={'center_x': .5})
        #tc.add_widget(Widget())
        tc.add_widget(b)
        #tc.add_widget(Widget())
        #b.center_x = tc.center_x
        print(tc.center_x)
        print(b.center_x)
        return tc


if __name__ == '__main__':
    TemplateApp().run()
