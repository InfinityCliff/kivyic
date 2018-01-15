# -*- coding: utf-8 -*-

from kivy.app import App

from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty, OptionProperty

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivyic import ColorProperty

from itertools import compress
from functools import partial

import inspect


__all__ = ['dprint', 'CanvasFill']
__version__ = '0.0'

DEBUG = False
DEBUG_INTERNET = False


def dprint(depth, *args):
    for d in range(1, depth + 1):
        stack = inspect.stack()[d]
        if '/' in stack[1]:
            spl = '/'
        if '\\' in stack[1]:
            spl = '\\'
        print('[' + stack[3] + '\t]\t', stack[2], ': ', stack[1].split(spl)[-1])


class CanvasFill(Widget):
    """
    Place at end of Inheritance list and set fill_color and when to fill background
    """
    _fill = ListProperty()
    '''
    Fill color to bu used on the selected canvas.  Variable should not be set, instead
    set `fill_color`

    :attr:`fill` is an :class:`~kivy.properties.ListProperty` and
    defaults to [].

    .. versionadded:: 0.1
    '''

    fill_color = OptionProperty('clear', options=['red', 'gree', 'blue', 'yellow',
                                                 'white', 'black', 'magenta', 'cyan',
                                                 'orange', 'purple', 'clear'])
    '''
    Fill color to bu used on the selected canvas

    :attr:`fill_color` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'clear'.

    .. versionadded:: 0.1
    '''

    when = OptionProperty('none', options=['after', 'before', 'canvas', 'none'])
    '''
    Which canvas to fill background on.

    :attr:`when` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'none'.

    .. versionadded:: 0.1
    '''

    def __init__(self, **kwargs):
        self.fill_color = 'blue'
        super(CanvasFill, self).__init__(**kwargs)

    def on_fill_color(self, *args):
        self._fill = {'red':     [1, 0, 0, .3],
                      'green':   [0, 1, 0, .3],
                      'blue':    [0, 0, 1, 1],
                      'yellow':  [1, 1, 0, .3],
                      'white':   [1, 1, 1, .3],
                      'black':   [0, 0, 0, .3],
                      'magenta': [1, 0, 1, .3],
                      'cyan':    [0, 1, 1, .3],
                      'orange':  [1, .5, 0, .3],
                      'purple':  [.5, 0, 1, .3],
                      'clear':   [0, 0, 0, 0]
                      }[self.fill_color]

    def on_size(self, *args):
        """
        only draw the canvas after the size has been set, or may have remnant artifacts
        from default widget size
        """
        print(self.size)
        if self.when == 'after':
            self.canvas_after()
        if self.when == 'before':
            self.canvas_before()
        if self.when == 'canvas':
            self._canvas()

    def canvas_after(self, *args):
        if self.canvas:
            with self.canvas.after:
                Color(rgba=self._fill)
                Rectangle(size=self.size, pos=self.pos)
        else:
            Clock.schedule_once(self.canvas_after)

    def canvas_before(self, *args):
        if self.canvas:
            with self.canvas.before:
                Color(rgba=self._fill)
                Rectangle(size=self.size, pos=self.pos)
        else:
            Clock.schedule_once(self.canvas_before)

    def _canvas(self, *args):
        if self.canvas:
            with self.canvas:
                Color(rgba=self._fill)
                Rectangle(size=self.size, pos=self.pos)
        else:
            Clock.schedule_once(self._canvas)


class _CanvasLabel(Label, CanvasFill):
    text = 'Canvas Label'


class _CanvasBox (BoxLayout, CanvasFill):
    pass


class DebugTestApp(App):
    asp = ObjectProperty

    def build(self):
        b = BoxLayout()

        b.add_widget(_CanvasLabel(when='before', fill_color='white'))
        b.add_widget(_CanvasBox(when='after', fill_color='blue'))
        b.add_widget(_CanvasBox(when='after', fill_color='red'))
        b.add_widget(_CanvasLabel(when='before', fill_color='orange'))
        return b


if __name__ == '__main__':
    DebugTestApp().run()
