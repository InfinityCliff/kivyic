# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory

from kivy.uix.screenmanager import Screen, SlideTransition, CardTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, \
                            OptionProperty

from kivy.uix.behaviors import ButtonBehavior

from kivy.metrics import dp

import kivymd.material_resources as m_res
from kivymd.selectioncontrols import MDSwitch
from kivymd.button import MDFlatButton, MDIconButton
from kivymd.label import MDLabel

from kivymd.menu import MDDropdownMenu
from kivymd.theming import ThemableBehavior

from kivyic import path
from constants import *


Builder.load_string('''
#: include ''' + path + '''/settings_screen.kv
''')


class ICSettingList(GridLayout):  # from MDList
    '''ListItem container. Best used in conjunction with a
    :class:`kivy.uix.ScrollView`.

    When adding (or removing) a widget, it will resize itself to fit its
    children, plus top and bottom paddings as described by the MD spec.
    '''
    selected = ObjectProperty()
    _min_list_height = dp(16)
    _list_vertical_padding = dp(8)

    icon = StringProperty()

    def add_widget(self, widget, index=0):
        super(ICSettingList, self).add_widget(widget, index)
        self.height += widget.height

    def remove_widget(self, widget):
        super(ICSettingList, self).remove_widget(widget)
        self.height -= widget.height

class ICBaseSettingListItem(ThemableBehavior, FloatLayout): # from BaseListItem
    """
    Item on the Setting Screen.

    Parameters:
    setting_items:  Definition of settings

    type: option, switch, menu
    label: text label preceding item
    description: test description following item
    before: spacing before item, defaults to 0
    after: spacing after item, defaults to 0
    """
    #settings = DictProperty()
    #type_ = StringProperty()
    #text = StringProperty()
    #description = StringProperty()
    #before = NumericProperty(0)
    #after = NumericProperty(0)
    layout_container_h = ObjectProperty()
    title = StringProperty()
    title_label = ObjectProperty()
    description = StringProperty()
    desc_label = ObjectProperty()
    row_height = NumericProperty(dp(40))
    text = StringProperty()
    text_color = ListProperty(None)
    font_style = OptionProperty('Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title', 'Headline', 'Display1', 'Display2', 'Display3', 'Display4', 'Button', 'Icon'])
    divider = OptionProperty('Full', options=['Full', 'Inset', None], allownone=True)

    theme_text_color = StringProperty('Primary',allownone=True)
    title_container = ObjectProperty()
    _txt_left_pad = NumericProperty(dp(16))
    _txt_top_pad = NumericProperty()
    _txt_bot_pad = NumericProperty()
    _txt_right_pad = NumericProperty(m_res.HORIZ_MARGINS)

    def __init__(self, **kwargs):
        #self.text = 'Setting'
        super(ICBaseSettingListItem, self).__init__(**kwargs)

    def build(self, set_dict):
        pass
        #self.title = set_dict.get('title', '')
        #if self.title == '':
        #    self.remove_widget(self.title_label)

        #self.text = set_dict.get('text', '')

        #self.description = set_dict.get('description', '')
        #if self.description == '':
        #    self.remove_widget(self.desc_label)


class IRightBody:
    """
    Pseudo-interface for widgets that go in the right container for
    ListItems that support it.

    Implements nothing and requires no implementation, for annotation only.
    """
    pass


class IRightBodyTouch:
    """
    Same as :class:`~IRightBody`, but allows the widget to receive touch
    events instead of triggering the ListItem's ripple effect
    """
    pass


class ICContainerSupport:  # from ContainerSupport
    """
    Overrides add_widget in a ListItem to include support for I*Body
    widgets when the appropriate containers are present.
    """
    _touchable_widgets = ListProperty()

    def add_widget(self, widget, index=0):
        #if issubclass(widget.__class__, ILeftBody):
        #    self.ids['_left_container'].add_widget(widget)
        #elif issubclass(widget.__class__, ILeftBodyTouch):
        #    self.ids['_left_container'].add_widget(widget)
        #    self._touchable_widgets.append(widget)
        if issubclass(widget.__class__, IRightBody):
            self.ids['_right_container'].add_widget(widget)
        elif issubclass(widget.__class__, IRightBodyTouch):
            self.ids['_right_container'].add_widget(widget)
            self._touchable_widgets.append(widget)
        else:
            return super(ICBaseSettingListItem, self).add_widget(widget)

    def remove_widget(self, widget):
        super(ICBaseSettingListItem, self).remove_widget(widget)
        if widget in self._touchable_widgets:
            self._touchable_widgets.remove(widget)

    def on_touch_down(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'down'):
            return
        super(ICBaseSettingListItem, self).on_touch_down(touch)

    def on_touch_move(self, touch, *args):
        if self.propagate_touch_to_touchable_widgets(touch, 'move', *args):
            return
        super(ICBaseSettingListItem, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'up'):
            return
        super(ICBaseSettingListItem, self).on_touch_up(touch)

    def propagate_touch_to_touchable_widgets(self, touch, touch_event, *args):
        triggered = False
        for i in self._touchable_widgets:
            if i.collide_point(touch.x, touch.y):
                triggered = True
                if touch_event == 'down':
                    i.on_touch_down(touch)
                elif touch_event == 'move':
                    i.on_touch_move(touch, *args)
                elif touch_event == 'up':
                    i.on_touch_up(touch)
        return triggered


class ICSettingLineSwitch(ICBaseSettingListItem, ICContainerSupport):  # from OneLineIconListItem & OneLineListItem
    """
    A one line setting item with a switch
    """
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _txt_left_pad = NumericProperty(dp(72))
    _num_lines = 1

    def __init__(self, **kwargs):
        super(ICSettingLineSwitch, self).__init__(**kwargs)
        self.height = dp(48)
        self.ids['_right_container'].add_widget(MDSwitch())

    def build(self, set_dict):
        self.text = set_dict['text']


class ICSettingLineOption(ICContainerSupport, ICBaseSettingListItem):
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _txt_left_pad = NumericProperty(dp(72))
    _num_lines = 1
    option_button = ObjectProperty()
    options = ListProperty()

    def __init__(self, **kwargs):
        super(ICSettingLineOption, self).__init__(**kwargs)
        self.height = dp(48)
        self.option_button = MDFlatButton(text='default')
        self.option_button.bind(on_release=self.open_option_menu)
        self.ids['_right_container'].add_widget(self.option_button)

    def build(self, set_dict):
        self.text = set_dict['text']
        self.add_options(set_dict['options'])

    def add_options(self, options):
        for option in options:
            self.options.append({'viewclass': 'MDMenuItem', 'text': option})

    def open_option_menu(self, instance):
        MDDropdownMenu(items=self.options, width_mult=2).open(self)


class ICSettingLineMenu(ICContainerSupport, ICBaseSettingListItem):
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _txt_left_pad = NumericProperty(dp(72))
    _num_lines = 1
    button = ObjectProperty()
    screen = StringProperty()

    def __init__(self, **kwargs):
        super(ICSettingLineMenu, self).__init__(**kwargs)
        self.height = dp(48)
        self.button = MDIconButton(icon='arrow-right')
        self.ids['_right_container'].add_widget(self.button)

    def build(self, set_dict):
        self.text = set_dict['text']
        if set_dict.get('screen', '') != '':
            self.screen = set_dict['screen']
            self.button.bind(on_release=self.change_screen)

    def change_screen(self, caller):
        print(self.screen)
        App.get_running_app().root.current = self.screen


class ICSettingTitleDescription(GridLayout):

    def build(self, set_dict):
        self.ids['title'].text = set_dict['title']
        self.ids['description'].text = set_dict['description']


class ICSettingTitle(MDLabel):
    pass


class ICSettingDesc(BoxLayout):
    pass


class ICSettingScreen(Screen):
    """
    Setting Screen

    Parameters:
    layout_container: Reference to GridLayout between the top and bottom menus

    Methods:
    """
    layout_container = ObjectProperty()
    done_screen = StringProperty()
    default_set_list = [{'text': 'Default Switch', 'type': 'switch', 'default': True, 'title': 'Default Switch Title', 'description': 'Default setting switch description'},
                        {'text': 'Default Menu', 'type': 'menu', 'title': 'DEFAULT OPTIONS', 'screen': '', 'description': 'this is a description for the seting'},
                        {'text': 'Default Option', 'type': 'option', 'options': ['A', 'B', 'C'], 'title': 'Default option title', 'description': 'Default setting option description'},
                       ]

    def __init__(self, **kwargs):
        super(ICSettingScreen, self).__init__(**kwargs)

    def build(self, set_list, done_screen):
        self.done_screen = done_screen
        if len(set_list) == 0:
            set_list = self.default_set_list

        for set_dict in set_list:
            if set_dict['type'] == 'option':
                si = ICSettingLineOption()

            if set_dict['type'] == 'switch':
                si = ICSettingLineSwitch()

            if set_dict['type'] == 'menu':
                si = ICSettingLineMenu()

            si.build(set_dict)
            self.layout_container.add_widget(si)

            if set_dict.get('title') != '':
                self.add_title(set_dict, si)
            #if set_dict.get('description', '') != '':
            #    self.add_description(set_dict, si)

    def add_title(self, set_dict, widget):
# TODO - WORKING HERE - ADD BOXLAYOUT TITLE CONTAINER TO OTHER TWO SETTING TYPES
        widget.title_container.add_widget(MDLabel(text=set_dict['title']))
        widget.height += widget.title_container.height

    def add_description(self, set_dict, widget):
        desc = ICSettingDesc()
        desc.ids['desc'].text = set_dict['description']
        widget.height += desc.height
        #desc.y = widget.y
        widget.add_widget(desc)

    def done(self):
        self.manager.transition = CardTransition(mode='pop', direction='down')
        self.manager.current = self.done_screen