# -*- coding: utf-8 -*-

from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty

from kivyic import ColorProperty

from itertools import compress
from functools import partial

import inspect

__all__ = ['dprint']
__version__ = '0.0'


def dprint(depth, *args):
    for d in range(1, depth + 1):
        print(d, ':', inspect.stack()[d][3])



def color_canvas(widget, color=None, before=False, after=True, canvas=False):
    Clock.schedule_once(partial(_color_canvas, widget, color, before, after, canvas))


def _color_canvas(widget, color=None, before=False, after=True, canvas=False, *args):
    if color is None:
        color = [0, 0, 1, .3]
    #print(widget)
    print('::', widget.pos, widget.size)
    #print(widget.parent)
    canvas_base = list(compress([widget.canvas.before, widget.canvas.after, widget.canvas], [before, after, canvas]))[0]
    #print(canvas_base)
    with widget.canvas.after:
        Color(color)
        Rectangle(pos=widget.pos, size=widget.size)


class CanvasBehavior:
    canvas_color = ListProperty([255,0,0,1])

    def __init__(self, **kwargs):
        super(CanvasBehavior, self).__init__(**kwargs)
        with self.canvas.after:
            Color(self.canvas_color)
            Rectangle(size=self.size, pos=self.pos)