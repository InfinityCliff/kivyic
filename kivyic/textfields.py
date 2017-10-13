# -*- coding: utf-8 -*-
import sys
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp


from kivy.properties import NumericProperty, StringProperty, \
                            OptionProperty, ListProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior

from kivymd.theming import ThemableBehavior
from kivymd.ripplebehavior import RectangularRippleBehavior
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBody, IRightBodyTouch

import kivymd.material_resources as m_res

Builder.load_string('''
 
    
<BaseTextInputItem>
    size_hint_y: None
    canvas:
        Color:
            rgba: self.theme_cls.divider_color if root.divider is not None else (0, 0, 0, 0)
        Line:
            points: (root.x ,root.y, root.x+self.width, root.y)\
                    if root.divider == 'Full' else\
                    (root.x+root._txt_left_pad, root.y,\
                    root.x+self.width-root._txt_left_pad-root._txt_right_pad,\
                    root.y)
    BoxLayout:
        id: _text_container
        orientation: 'vertical'
        pos: root.pos
        #padding: root._txt_left_pad, root._txt_top_pad, root._txt_right_pad, root._txt_bot_pad
        TextInput:
            id: _lbl_primary
            text: root.text
            padding: [5, 14]
            font_style: root.font_style
            theme_text_color: root.theme_text_color
            text_color: root.text_color

<OneLineAvatarTextInputItem>
    BoxLayout:
        id: _left_container
        size_hint: None, None
        x: root.x + dp(16)
        y: root.y + root.height/2 - self.height/2
        size: dp(40), dp(40)

<ThreeLineAvatarTextInputItem>
    BoxLayout:
        id: _left_container
        size_hint: None, None
        x: root.x + dp(16)
        y: root.y + root.height - root._txt_top_pad - self.height - dp(5)
        size: dp(40), dp(40)

<OneLineIconTextInputItem>
    BoxLayout:
        id: _left_container
        size_hint: None, None
        x: root.x + dp(16)
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)

<ThreeLineIconTextInputItem>
    BoxLayout:
        id: _left_container
        size_hint: None, None
        x: root.x + dp(16)
        y: root.y + root.height - root._txt_top_pad - self.height - dp(5)
        size: dp(48), dp(48)

<OneLineRightIconTextInputItem>
    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - m_res.HORIZ_MARGINS - self.width
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)

<ThreeLineRightIconTextInputItem>
    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - m_res.HORIZ_MARGINS - self.width
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)

<OneLineAvatarIconTextInputItem>
    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - m_res.HORIZ_MARGINS - self.width
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)

<TwoLineAvatarIconTextInputItem>
    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - m_res.HORIZ_MARGINS - self.width
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)

<ThreeLineAvatarIconTextInputItem>
    BoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.x + root.width - m_res.HORIZ_MARGINS - self.width
        y: root.y + root.height - root._txt_top_pad - self.height - dp(5)
        size: dp(48), dp(48)
''')


class BaseTextInputItem(ThemableBehavior, RectangularRippleBehavior,
                        ButtonBehavior, FloatLayout):
    '''Base class to all TextInputItems. Not supposed to be instantiated on its own.
    '''

    text = StringProperty()
    '''Text shown in the first line.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults
    to "".
    '''

    text_color = ListProperty(None)
    ''' Text color used if theme_text_color is set to 'Custom' '''

    font_style = OptionProperty(
            'Subhead', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                                'Headline', 'Display1', 'Display2', 'Display3',
                                'Display4', 'Button', 'Icon'])

    theme_text_color = StringProperty('Primary',allownone=True)
    ''' Theme text color for primary text '''

    secondary_text = StringProperty()
    '''Text shown in the second and potentially third line.

    The text will wrap into the third line if the ListItem's type is set to
    \'one-line\'. It can be forced into the third line by adding a \\n
    escape sequence.

    :attr:`secondary_text` is a :class:`~kivy.properties.StringProperty` and
    defaults to "".
    '''

    secondary_text_color = ListProperty(None)
    ''' Text color used for secondary text if secondary_theme_text_color 
    is set to 'Custom' '''

    secondary_theme_text_color = StringProperty('Secondary',allownone=True)
    ''' Theme text color for secondary primary text '''

    secondary_font_style = OptionProperty(
            'Body1', options=['Body1', 'Body2', 'Caption', 'Subhead', 'Title',
                              'Headline', 'Display1', 'Display2', 'Display3',
                              'Display4', 'Button', 'Icon'])

    divider = OptionProperty('Full', options=['Full', 'Inset', None], allownone=True)

    _txt_left_pad = NumericProperty(dp(16))
    _txt_top_pad = NumericProperty()
    _txt_bot_pad = NumericProperty()
    _txt_right_pad = NumericProperty(m_res.HORIZ_MARGINS)
    _num_lines = 2


class ContainerSupportTI:
    """
    Overrides add_widget in a TextInputItem to include support for I*Body
    widgets when the appropriate containers are present.
    """
    _touchable_widgets = ListProperty()

    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, ILeftBody):
            self.ids['_left_container'].add_widget(widget)
        elif issubclass(widget.__class__, ILeftBodyTouch):
            self.ids['_left_container'].add_widget(widget)
            self._touchable_widgets.append(widget)
        elif issubclass(widget.__class__, IRightBody):
            self.ids['_right_container'].add_widget(widget)
        elif issubclass(widget.__class__, IRightBodyTouch):
            self.ids['_right_container'].add_widget(widget)
            self._touchable_widgets.append(widget)
        else:
            return super(BaseTextInputItem, self).add_widget(widget)

        def remove_widget(self, widget):
            super(BaseTextInputItem, self).remove_widget(widget)
        if widget in self._touchable_widgets:
            self._touchable_widgets.remove(widget)

    def on_touch_down(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'down'):
            return
        super(BaseTextInputItem, self).on_touch_down(touch)

    def on_touch_move(self, touch, *args):
        if self.propagate_touch_to_touchable_widgets(touch, 'move', *args):
            return
        super(BaseTextInputItem, self).on_touch_move(touch, *args)

    def on_touch_up(self, touch):
        if self.propagate_touch_to_touchable_widgets(touch, 'up'):
            return
        super(BaseTextInputItem, self).on_touch_up(touch)

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

class OneLineTextInputItem(BaseTextInputItem):
    '''
    A one line list item
    '''
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _num_lines = 1

    def __init__(self, **kwargs):
        super(OneLineTextInputItem, self).__init__(**kwargs)
        self.height = dp(48)


class TwoLineTextInputItem(BaseTextInputItem):
    '''
    A two line list item
    '''
    _txt_top_pad = NumericProperty(dp(20))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)

    def __init__(self, **kwargs):
        super(TwoLineTextInputItem, self).__init__(**kwargs)
        self.height = dp(72)


class ThreeLineTextInputItem(BaseTextInputItem):
    '''
    A three line list item
    '''
    _txt_top_pad = NumericProperty(dp(16))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _num_lines = 3

    def __init__(self, **kwargs):
        super(ThreeLineTextInputItem, self).__init__(**kwargs)
        self.height = dp(88)


class OneLineAvatarTextInputItem(ContainerSupportTI, BaseTextInputItem):
    _txt_left_pad = NumericProperty(dp(72))
    _txt_top_pad = NumericProperty(dp(20))
    _txt_bot_pad = NumericProperty(dp(19))  # dp(24) - dp(5)
    _num_lines = 1

    def __init__(self, **kwargs):
        super(OneLineAvatarTextInputItem, self).__init__(**kwargs)
        self.height = dp(56)


class TwoLineAvatarTextInputItem(OneLineAvatarTextInputItem):
    _txt_top_pad = NumericProperty(dp(20))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _num_lines = 2

    def __init__(self, **kwargs):
        super(BaseTextInputItem, self).__init__(**kwargs)
        self.height = dp(72)


class ThreeLineAvatarTextInputItem(ContainerSupportTI, ThreeLineTextInputItem):
    _txt_left_pad = NumericProperty(dp(72))


class OneLineIconTextInputItem(ContainerSupportTI, OneLineTextInputItem):
    _txt_left_pad = NumericProperty(dp(72))


class TwoLineIconTextInputItem(OneLineIconTextInputItem):
    _txt_top_pad = NumericProperty(dp(20))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _num_lines = 2

    def __init__(self, **kwargs):
        super(BaseTextInputItem, self).__init__(**kwargs)
        self.height = dp(72)


class ThreeLineIconTextInputItem(ContainerSupportTI, ThreeLineTextInputItem):
    _txt_left_pad = NumericProperty(dp(72))


class OneLineRightIconTextInputItem(ContainerSupportTI, OneLineTextInputItem):
    # dp(40) = dp(16) + dp(24):
    _txt_right_pad = NumericProperty(dp(40) + m_res.HORIZ_MARGINS)


class TwoLineRightIconTextInputItem(OneLineRightIconTextInputItem):
    _txt_top_pad = NumericProperty(dp(20))
    _txt_bot_pad = NumericProperty(dp(15))  # dp(20) - dp(5)
    _num_lines = 2

    def __init__(self, **kwargs):
        super(BaseTextInputItem, self).__init__(**kwargs)
        self.height = dp(72)


class ThreeLineRightIconTextInputitem(ContainerSupportTI, ThreeLineTextInputItem):
    # dp(40) = dp(16) + dp(24):
    _txt_right_pad = NumericProperty(dp(40) + m_res.HORIZ_MARGINS)


class OneLineAvatarIconTextInputItem(OneLineAvatarTextInputItem):
    # dp(40) = dp(16) + dp(24):
    _txt_right_pad = NumericProperty(dp(40) + m_res.HORIZ_MARGINS)


class TwoLineAvatarIconTextInputItem(TwoLineAvatarTextInputItem):
    # dp(40) = dp(16) + dp(24):
    _txt_right_pad = NumericProperty(dp(40) + m_res.HORIZ_MARGINS)


class ThreeLineAvatarIconTextInputItem(ThreeLineAvatarTextInputItem):
    # dp(40) = dp(16) + dp(24):
    _txt_right_pad = NumericProperty(dp(40) + m_res.HORIZ_MARGINS)


