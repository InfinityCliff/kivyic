from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import InstructionGroup
from kivy.properties import BooleanProperty, ListProperty
from itertools import compress


def color_canvas(widget, color=[0,0,0,1], before=False, after=True, canvas=False):
    # before = BooleanProperty(False)
    # after = BooleanProperty(False)
    # color = ListProperty()
    print('color_canvas')
    instructions = InstructionGroup()
    instructions.add(Color(1, 0, 0, 1))
    instructions.add(Rectangle(pos=widget.pos, size=widget.pos))
    canvas_base = list(compress([widget.canvas.before, widget.canvas.after, widget.canvas], [before, after, canvas]))[0]

    print(canvas_base)
    with canvas_base:
        Color(1, 0, 0, 1)
        Rectangle(pos=widget.pos, size=widget.pos)

    return instructions