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


class ICMultiPositionButton(ICIconButton):
    positions = ListProperty()
    _position = 0
    position = StringProperty()

    def on_press(self):
        if self._position == len(self.positions) - 1:
            self._position = -1
        self._position += 1
        self.position = self.positions[self._position]
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
        b.add_widget(ICMultiPositionButton(states=['0', '1', '2']))
        return b


if __name__ == '__main__':
    ButtonTestApp().run()

