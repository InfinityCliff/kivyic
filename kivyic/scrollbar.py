# https://github.com/kivy/kivy/wiki/A-draggable-scrollbar-using-a-slider


#!python
import kivy

from kivy.app import App
#from kivy.lang.builder import Builder
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation

from kivy.properties import StringProperty, ObjectProperty, NumericProperty, OptionProperty, ReferenceListProperty, \
                            ListProperty, AliasProperty, DictProperty
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

from kivyic import path, alphabet

from functools import partial

Builder.load_file(path + '/scrollbar.kv')

__all__ = ['AlphaScrollView']


class AlphaScrollPane(RelativeLayout):
    letter = StringProperty()
    scrollview = ObjectProperty()
    slider = ObjectProperty()
    content = ObjectProperty()
    container = ObjectProperty()

    def __init__(self, **kwargs):
        super(AlphaScrollPane, self).__init__(**kwargs)

        #layout1 = StackLayout(orientation='lr-bt')
        self.container = StackLayout(orientation='lr-bt')

        self.scrollview = AlphaScrollView(size_hint=(0.9, 0.95),
                                          content=self.content)

        self.slider = AlphaSlider(min=1, max=26, value=26, orientation='vertical', step=1, size_hint=(0.1, 0.95),
                                  value_track=False)
        self.slider.labels = alphabet

        self.slider.bind(value=partial(self.scroll_change, self.scrollview))

        self.scrollview._container.bind(minimum_height=self.scrollview._container.setter('height'))

        self.container.add_widget(self.scrollview)
        self.container.add_widget(self.slider)
        self.add_widget(self.container)

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


class AlphaSlider(Slider):
    labels = ListProperty()
    layout = ObjectProperty()
    #label_height = NumericProperty()

    def __init__(self, **kwargs):
        super(AlphaSlider, self).__init__(**kwargs)

    def on_labels(self, *args):
        self.layout.clear_widgets()
        #height = self.height / len(self.labels)
        for label in self.labels:
            lbl = AlphaSBLabel(text=str(label))
            #lbl.fbind('height', self.label_height)
            #self.fbind('height', lbl.height)
            self.layout.add_widget(lbl)

    #def on_height(self, *args):
    #    print('updating height')
    #    print(self.height)
    #    self.label_height = self.height / (len(self.labels))
    #    print(self.label_height)


class AlphaScrollViewException(Exception):
    """
    AlphaScrollView exception, fired when multiple content widgets are added to the
    popup.

    .. versionadded:: 0.1
    """


class AlphaScrollView(ScrollView):
    content = ObjectProperty()
    _container = ObjectProperty()

    def on_content(self, instance, value):
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

    def scroll_to(self, widget, padding=10, animate=True):
        if type(widget) is str:
            self.scroll_to_letter(widget)
        else:
            super().scroll_to(widget, padding=10, animate=True)

    def scroll_to_letter(self, letter, padding=10, animate=True):
        for child in reversed(self._container.children):
            if child.text[0] == letter:
                self._scroll_to_letter(child, padding=10, animate=True)
                break

    def _scroll_to_letter(self, widget, padding=10, animate=True):
        '''Scrolls the viewport to ensure that the given widget is visible,
        optionally with padding and animation. If animate is True (the
        default), then the default animation parameters will be used.
        Otherwise, it should be a dict containing arguments to pass to
        :class:`~kivy.animation.Animation` constructor.

        .. versionadded:: 0.1
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
        b = BoxLayout() # padding=[dp(11)])
        content = GridLayout(cols=1)
        for letter in alphabet:
            for i in range(1, 6):
                btn = Button(text=letter + str(i), size_hint_y=None, height=60, valign='middle', font_size=12)
                btn.text_size = btn.size
                content.add_widget(btn)
        asp = AlphaScrollPane(content=content)
        #asp = AlphaScrollPane()
        #asp.content = content
        b.add_widget(asp)
        return b


if __name__ == '__main__':
    ScrollApp().run()