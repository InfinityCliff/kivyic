from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

import kivymd.material_resources as m_res
from kivymd.theming import ThemableBehavior

from kivyic import path

Builder.load_file(path + '/menu.kv')


class ICMenuItem(ButtonBehavior, BoxLayout):
    _title = StringProperty()
    _filter = StringProperty()
    text = StringProperty

    def __init__(self, **kwargs):
        super(ICMenuItem, self).__init__(**kwargs)
        # TODO -   WORKING HERE - USE DICT TO PICK VALUE OF TITLE AND FILTER BASED ON TYPE OF TEXT, LIST, TUPLE, STRING WITH ,
        if type(self.text)

class ICDropdown(ThemableBehavior, DropDown):
    #theme_cls = ThemeManager
    items = ListProperty()
    '''See :attr:`~kivy.uix.recycleview.RecycleView.data`
    '''

    width_mult = NumericProperty(1)
    '''This number multiplied by the standard increment (56dp on mobile,
    64dp on desktop, determines the width of the menu items.

    If the resulting number were to be too big for the application Window,
    the multiplier will be adjusted for the biggest possible one.
    '''
    def on_select(self, value):
        print(value)
        super().on_select(value)

    def display_menu(self, caller):
        # We need to pick a starting point, see how big we need to be,
        # and where to grow to.

        c = caller.to_window(caller.right,
                             caller.top)  # Starting coords

        # ---ESTABLISH INITIAL TARGET SIZE ESTIMATE---
        target_width = self.width_mult * m_res.STANDARD_INCREMENT
        # If we're wider than the Window...
        if target_width > Window.width:
            # ...reduce our multiplier to max allowed.
            target_width = int(
                    Window.width / m_res.STANDARD_INCREMENT) * m_res.STANDARD_INCREMENT

        target_height = sum([dp(48) for i in self.items])
        # If we're over max_height...
        if 0 < self.max_height < target_height:
            target_height = self.max_height

        # ---ESTABLISH VERTICAL GROWTH DIRECTION---
        if self.ver_growth is not None:
            ver_growth = self.ver_growth
        else:
            # If there's enough space below us:
            if target_height <= c[1] - self.border_margin:
                ver_growth = 'down'
            # if there's enough space above us:
            elif target_height < Window.height - c[1] - self.border_margin:
                ver_growth = 'up'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space below us:
                if c[1] >= Window.height - c[1]:
                    ver_growth = 'down'
                    target_height = c[1] - self.border_margin
                # if there's more space above us:
                else:
                    ver_growth = 'up'
                    target_height = Window.height - c[1] - self.border_margin

        if self.hor_growth is not None:
            hor_growth = self.hor_growth
        else:
            # If there's enough space to the right:
            if target_width <= Window.width - c[0] - self.border_margin:
                hor_growth = 'right'
            # if there's enough space to the left:
            elif target_width < c[0] - self.border_margin:
                hor_growth = 'left'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space to the right:
                if Window.width - c[0] >= c[0]:
                    hor_growth = 'right'
                    target_width = Window.width - c[0] - self.border_margin
                # if there's more space to the left:
                else:
                    hor_growth = 'left'
                    target_width = c[0] - self.border_margin

        if ver_growth == 'down':
            tar_y = c[1] - target_height
        else:  # should always be 'up'
            tar_y = c[1]

        if hor_growth == 'right':
            tar_x = c[0]
        else:  # should always be 'left'
            tar_x = c[0] - target_width
        anim = Animation(x=tar_x, y=tar_y,
                         width=target_width, height=target_height,
                         duration=.3, transition='out_quint')
        menu = self.ids['md_menu']
        menu.pos = c
        anim.start(menu)
