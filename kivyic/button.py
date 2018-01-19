# -*- coding: utf-8 -*-

from kivyic import path
from kivyic.label import ICIconLabel

from kivy.app import App
from kivy.lang import Builder


from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty, NumericProperty
from kivymd.theming import ThemeManager

from kivymd.selectioncontrols import MDSwitch
from kivy.uix.switch import Switch
__all__ = ['ICIconButton', 'ICSwitch']
__version__ = '0.1'

Builder.load_file(path + '/button.kv')


class ICBaseButton(ButtonBehavior, Label):
    pass


class ICIconButton(ButtonBehavior, ICIconLabel):
    icon = StringProperty('checkbox-blank-circle')


class ICRoundedButton(ICBaseButton):
    pass


class ICMultiStateButton(ICIconButton):
    states = ListProperty()
    _state = 0
    state = StringProperty()

    def on_press(self):
        if self._state == len(self.states) - 1:
            self._state = -1
        self._state += 1
        self.state = self.states(self._state)
        super().on_press()


class ICSwitch(MDSwitch):
    outline = BooleanProperty()
    outline_color = ListProperty()
    outline_track_width = NumericProperty()
    #outline_line_width = NumericProperty()
    track_width = NumericProperty()

    def __init__(self, **kwargs):
        super(ICSwitch, self).__init__(**kwargs)


class ButtonTestApp(App):
    title = 'Button Test App'
    theme_cls = ThemeManager()
    music_player = ObjectProperty()

    def build(self):
        b = BoxLayout(orientation='vertical', size_hint_y=None)
        #b.height = b.minimum_height

        b.add_widget(ICIconButton())
        b.add_widget(MDSwitch())
        b.add_widget(ICSwitch(outline_color=[1,0,0,1],
                              track_width=12,
                              outline_track_width=24,
                              outline=False
                             ))
        b.add_widget(Switch())
        b.add_widget(ICMultiStateButton(states=['0', '1', '2']))
        return b


if __name__ == '__main__':
    ButtonTestApp().run()

