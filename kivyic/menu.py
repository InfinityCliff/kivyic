from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty, OptionProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import kivymd.material_resources as m_res
from kivymd.theming import ThemableBehavior
from kivymd.label import MDLabel

from kivyic import path

Builder.load_file(path + '/menu.kv')


class ICMenuItem(ButtonBehavior, BoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(ICMenuItem, self).__init__(**kwargs)
        self.register_event_type('on_select')
        #self.bind(on_release=self.on_select(self.text))

    def on_select(self, value):
        pass


class ICMenuFilterItem(ICMenuItem):
    _title = StringProperty()
    _filter = StringProperty()
    text = ObjectProperty()

    def on_text(self, instance, value):
        if type(self.text) in[list, tuple]:
            self._title, self._filter = self.text[0], self.text[1]
        if type(self.text) == dict:
            self._title, self._filter = self.text['title'], self.text['filter']
        if type(self.text) == str:
            self._title, self._filter = self.text.split()


menu_viewclass_def = {'ICMenuItem': ICMenuItem,
                      'ICFilterMenuItem': ICMenuFilterItem}


# TOFIX - menu height is too large, loot at display_menu function in dropdown
class ICMenu(BoxLayout):
    data = ListProperty()
    width_mult = NumericProperty(1)

    def on_data(self, instance, value):
        for dict_ in self.data:
            cls = menu_viewclass_def[dict_['viewclass']]
            mi = cls(text=dict_['text'])
            mi.bind(on_select=self.on_select)
            self.add_widget(mi)

    def on_select(self, obj, value):
        pass


class ICDropdown(ThemableBehavior, BoxLayout):
    items = ListProperty()
    '''See :attr:`~kivy.uix.recycleview.RecycleView.data`
    '''

    width_mult = NumericProperty(1)
    '''This number multiplied by the standard increment (56dp on mobile,
    64dp on desktop, determines the width of the menu items.

    If the resulting number were to be too big for the application Window,
    the multiplier will be adjusted for the biggest possible one.
    '''

    max_height = NumericProperty()
    '''The menu will grow no bigger than this number.

    Set to 0 for no limit. Defaults to 0.
    '''

    border_margin = NumericProperty(dp(4))
    '''Margin between Window border and menu
    '''

    ver_growth = OptionProperty(None, allownone=True,
                                options=['up', 'down'])
    '''Where the menu will grow vertically to when opening

    Set to None to let the widget pick for you. Defaults to None.
    '''

    hor_growth = OptionProperty(None, allownone=True,
                                options=['left', 'right'])
    '''Where the menu will grow horizontally to when opening

    Set to None to let the widget pick for you. Defaults to None.
    '''

    def open(self, caller):
        Window.add_widget(self)
        Clock.schedule_once(lambda x: self.display_menu(caller), -1)
        self.ids.ic_menu.bind(on_select=self.on_select)

    def on_select(self, obj, value):
        self.ids.ic_menu.text = value
        print(obj)
        # WORKING HERE - not sending up the  line, add prings to on_selcts down to see where it stops...

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
        menu = self.ids['ic_menu']
        # WORKING HERE TO GET MENU TO SHOW, LOOKS LIKE MENU DATA IS PASSING CORRECTLY JUST NOT OPENING
        menu.pos = c
        anim.start(menu)


    def on_touch_down(self, touch):
        if not self.ids['ic_menu'].collide_point(*touch.pos):
            self.dismiss()
            return True
        super(ICDropdown, self).on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        super(ICDropdown, self).on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        super(ICDropdown, self).on_touch_up(touch)
        self.dismiss()
        return True

    def dismiss(self):
        Window.remove_widget(self)