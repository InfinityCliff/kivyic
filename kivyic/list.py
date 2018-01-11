# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

__all__ = []
__version__ = '0.1'


class ListTestApp(App):
    title = 'Music Player Test App'

    def build(self):
        b = BoxLayout(padding=[dp(10)])
        return b


if __name__ == '__main__':
    ListTestApp().run()
