# https://github.com/kivy/kivy/wiki/A-draggable-scrollbar-using-a-slider


#!python
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation

from kivy.properties import StringProperty, ObjectProperty, NumericProperty, OptionProperty, ReferenceListProperty, \
                            ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.popup import Popup


from functools import partial

Builder.load_string('''

<AlphaScrollPane>:
    padding: '10dp'
    
        
<AlphaScrollView>:
    layout: _layout
    GridLayout:
        id: _layout
        cols: 1
        size_hint_y: None

<AlphaScrollBarOverlay>:

        
<AlphaSBLabel>:
    canvas.before:
        Color:
            rgba: 0,1,0,.3
        RoundedRectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 0,0,1,1
        Line:
            points: (self.x+self.height/2, self.right+self.height/2)
            #weight: 1
''')

__all__ = ['AlphaScrollView']


class AlphaScrollPane(RelativeLayout):
    letter = StringProperty()
    scrollview = ObjectProperty()
    slider = ObjectProperty()

    def __init__(self, **kwargs):
        super(AlphaScrollPane, self).__init__(**kwargs)

        layout1 = StackLayout(orientation='lr-bt')

        self.scrollview = AlphaScrollView(size_hint=(0.9, 0.95))

        self.slider = Slider(min=1, max=26, value=26, orientation='vertical', step=1, size_hint=(0.1, 0.95))

        self.slider.bind(value=partial(self.scroll_change, self.scrollview))

        self.scrollview.layout.bind(minimum_height=self.scrollview.layout.setter('height'))

        for ch in range(ord('A'), ord('Z') + 1):
            for i in range(1, 6):
                btn = Button(text=chr(ch) + str(i), size_hint_y=None, height=60, valign='middle', font_size=12)
                btn.text_size = (btn.size)
                self.scrollview.layout.add_widget(btn)
        layout1.add_widget(self.scrollview)
        layout1.add_widget(self.slider)
        self.add_widget(layout1)
        sbo = AlphaScrollBarOverlay()
        sbo.content = ['A', 'B']
        self.add_widget(sbo)

    def on_letter(self, *args):
        self.find_letter()

    def find_letter(self):
        self.scrollview.scroll_to(self.letter)

    def value_to_letter(self, value):
        self.letter = chr(abs(value - 26) + ord('A'))

    def scroll_change(self, scrlv, slider, value):
        self.value_to_letter(value)
        scrlv.scroll_y = slider.value_normalized

    def slider_change(self, s, instance, value):
        if value >= 0:
            #this to avoid 'maximum recursion depth exceeded' error
            s.value = value


class AlphaSBLabel(Label):
    pass


class AlphaScrollBarOverlay(GridLayout):

    step = NumericProperty(0)

    bar_width = NumericProperty('2dp')
    '''Width of the horizontal / vertical scroll bar. The width is interpreted
    as a height for the horizontal bar.

    .. versionadded:: 0.1

    :attr:`bar_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 2.
    '''

    bar_pos_x = OptionProperty('bottom', options=('top', 'bottom'))
    '''Which side of the ScrollView the horizontal scroll bar should go
    on. Possible values are 'top' and 'bottom'.

    .. versionadded:: 0.1

    :attr:`bar_pos_x` is an :class:`~kivy.properties.OptionProperty`,
    defaults to 'bottom'.

    '''

    bar_pos_y = OptionProperty('right', options=('left', 'right'))
    '''Which side of the ScrollView the vertical scroll bar should go
    on. Possible values are 'left' and 'right'.

    .. versionadded:: 0.1

    :attr:`bar_pos_y` is an :class:`~kivy.properties.OptionProperty` and
    defaults to 'right'.

    '''

    bar_pos = ReferenceListProperty(bar_pos_x, bar_pos_y)
    '''Which side of the scroll view to place each of the bars on.
     
    .. versionadded:: 0.1

    :attr:`bar_pos` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`bar_pos_x`, :attr:`bar_pos_y`)
    '''

    bar_margin = NumericProperty(0)
    '''Margin between the bottom / right side of the scrollview when drawing
    the horizontal / vertical scroll bar.

    .. versionadded:: 0.1

    :attr:`bar_margin` is a :class:`~kivy.properties.NumericProperty`, default
    to 0
    '''

    content = ListProperty()

    def __init__(self, **kwargs):
        super(AlphaScrollBarOverlay, self).__init__(**kwargs)

    def on_content(self, *args):
        self.clear_widgets()
        for c in self.content:
            self.add_widget(AlphaSBLabel(text=str(c)))


class AlphaScrollView(ScrollView):
    layout = ObjectProperty()

    def scroll_to(self, widget, padding=10, animate=True):
        if type(widget) is str:
            self.scroll_to_letter(widget)
        else:
            super().scroll_to(widget, padding=10, animate=True)

    def scroll_to_letter(self, letter, padding=10, animate=True):
        for child in reversed(self.layout.children):
            if child.text[0] == letter:
                self._scroll_to_letter(child, padding=10, animate=True)
                break

    def _scroll_to_letter(self, widget, padding=10, animate=True):
        '''Scrolls the viewport to ensure that the given widget is visible,
        optionally with padding and animation. If animate is True (the
        default), then the default animation parameters will be used.
        Otherwise, it should be a dict containing arguments to pass to
        :class:`~kivy.animation.Animation` constructor.

        .. versionadded:: 1.9.1
        '''
        if not self.parent:
            return

        # if _viewport is layout and has pending operation, reschedule
        if hasattr(self._viewport, 'do_layout'):
            if self._viewport._trigger_layout.is_triggered:
                Clock.schedule_once(
                        lambda *dt: self.scroll_to(widget, padding, animate))
                return

        if isinstance(padding, (int, float)):
            padding = (padding, padding)

        pos = self.parent.to_widget(*widget.to_window(*widget.pos))
        cor = self.parent.to_widget(*widget.to_window(widget.right,
                                                      widget.top))

        dx = dy = 0

        if cor[1] < self.top:
            dy = self.top - pos[1] - widget.height - dp(padding[1])
        else:
            dy = self.top - cor[1] - dp(padding[1])


        if pos[0] < self.x:
            dx = self.x - pos[0] + dp(padding[0])
        elif cor[0] > self.right:
            dx = self.right - cor[0] - dp(padding[0])

        dsx, dsy = self.convert_distance_to_scroll(dx, dy)
        sxp = min(1, max(0, self.scroll_x - dsx))
        syp = min(1, max(0, self.scroll_y - dsy))

        if animate:
            if animate is True:
                animate = {'d': 0.2, 't': 'out_quad'}
            Animation.stop_all(self, 'scroll_x', 'scroll_y')
            Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp


class ScrollApp(App):

    def build(self):
        b = BoxLayout(padding=dp(10))
        b.add_widget(AlphaScrollPane())
        return b


if __name__ == '__main__':
    ScrollApp().run()