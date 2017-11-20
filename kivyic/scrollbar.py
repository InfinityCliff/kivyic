# https://github.com/kivy/kivy/wiki/A-draggable-scrollbar-using-a-slider


#!python
import kivy
kivy.require('1.10.0')
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from functools import partial

Builder.load_string('''
<AlphaScrollView>:
    layout: _layout
    GridLayout:
        id: _layout
        cols: 1
        size_hint_y: None
''')


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

    letter = StringProperty()
    scrollview = ObjectProperty()
    slider = ObjectProperty()

    def build(self):
        popup = Popup(title='Draggable Scrollbar', size_hint=(0.8,1), auto_dismiss=False)

        #this layout is the child widget for the main popup
        layout1 = StackLayout(orientation='lr-bt')

        #this button is a child of layout1
        closebutton = Button(text='close', size_hint=(0.9,0.05))
        closebutton.bind(on_press=popup.dismiss)

        #another child of layout1 and this is the scrollview which will have a custom draggable scrollbar
        self.scrollview = AlphaScrollView(size_hint=(0.9,0.95))

        #the last child of layout1 and this will act as the draggable scrollbar
        self.slider = Slider(min=1, max=26, value=26, orientation='vertical', step=1, size_hint=(0.1, 0.95))

        #scrlv.bind(scroll_y=partial(self.slider_change, s))

        #what this does is, whenever the slider is dragged, it scrolls the previously added scrollview by the same amount the slider is dragged
        self.slider.bind(value=partial(self.scroll_change, self.scrollview))

        #layout2 = GridLayout(id='layout', cols=1, size_hint_y=None)
        self.scrollview.layout.bind(minimum_height=self.scrollview.layout.setter('height'))

        for ch in range(ord('A'), ord('Z') + 1):
            for i in range(1, 6):
                btn = Button(text=chr(ch) + str(i), size_hint_y=None, height=60, valign='middle', font_size=12)
                btn.text_size = (btn.size)
                self.scrollview.layout.add_widget(btn)
        #self.scrollview.add_widget(self.scrollview.layout)
        layout1.add_widget(closebutton)
        layout1.add_widget(self.scrollview)
        layout1.add_widget(self.slider)
        popup.content = layout1
        popup.open()

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
            s.value=value

if __name__ == '__main__':
    ScrollApp().run()