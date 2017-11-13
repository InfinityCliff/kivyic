# -*- coding: utf-8 -*-
import sys
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.metrics import dp, sp



from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty,\
                            OptionProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.behaviors import ButtonBehavior

from kivyic.label import ICIconLabel  # not sure why but this is needed or will not find ICIconLabel
from kivyic import path
from kivymd.theming import ThemableBehavior
from kivymd.ripplebehavior import RectangularRippleBehavior
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBody, IRightBodyTouch
from kivymd.button import MDIconButton
from kivymd.textfields import TextfieldLabel
from kivymd.selectioncontrols import MDCheckbox
import kivymd.material_resources as m_res

Builder.load_file(path + '/textfields.kv')


# FIXME - on selection move cursor to end of line and no text selected
class ICTextFieldPlain(ThemableBehavior, TextInput, FocusBehavior):
    helper_text = StringProperty("This field is required")
    helper_text_mode = OptionProperty('none', options=['none', 'on_error', 'persistent', 'on_focus'])

    max_text_length = NumericProperty(None)
    required = BooleanProperty(False)

    color_mode = OptionProperty('primary', options=['primary', 'accent', 'custom'])
    line_color_normal = ListProperty()
    line_color_focus = ListProperty()
    error_color = ListProperty()

    error = BooleanProperty(False)
    _text_len_error = BooleanProperty(False)

    _hint_lbl_font_size = NumericProperty(sp(16))
    _hint_y = NumericProperty(dp(38))
    _line_width = NumericProperty(0)
    _current_line_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    _current_error_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    _current_hint_text_color = ListProperty([0.0, 0.0, 0.0, 0.0])
    _current_right_lbl_color = ListProperty([0.0, 0.0, 0.0, 0.0])

    def __init__(self, **kwargs):
        self._msg_lbl = TextfieldLabel(font_style='Caption',
                                       halign='left',
                                       valign='middle',
                                       text=self.helper_text)

        self._right_msg_lbl = TextfieldLabel(font_style='Caption',
                                             halign='right',
                                             valign='middle',
                                             text="")

        self._hint_lbl = TextfieldLabel(font_style='Subhead',
                                        halign='left',
                                        valign='middle')
        super(ICTextFieldPlain, self).__init__(**kwargs)
        self.line_color_normal = self.theme_cls.divider_color
        self.line_color_focus = self.theme_cls.primary_color
        self.error_color = self.theme_cls.error_color

        self._current_hint_text_color = self.theme_cls.disabled_hint_text_color
        self._current_line_color = self.theme_cls.primary_color

        self.bind(helper_text=self._set_msg,
                  hint_text=self._set_hint,
                  _hint_lbl_font_size=self._hint_lbl.setter('font_size'),
                  helper_text_mode=self._set_message_mode,
                  max_text_length=self._set_max_text_length,
                  text=self.on_text)
        self.theme_cls.bind(primary_color=self._update_primary_color,
                            theme_style=self._update_theme_style,
                            accent_color=self._update_accent_color)
        self.has_had_text = False

    def _update_colors(self, color):
        self.line_color_focus = color
        if not self.error and not self._text_len_error:
            self._current_line_color = color
            if self.focus:
                self._current_line_color = color

    def _update_accent_color(self, *args):
        if self.color_mode == "accent":
            self._update_colors(self.theme_cls.accent_color)

    def _update_primary_color(self, *args):
        if self.color_mode == "primary":
            self._update_colors(self.theme_cls.primary_color)

    def _update_theme_style(self, *args):
        self.line_color_normal = self.theme_cls.divider_color
        if not any([self.error, self._text_len_error]):
            if not self.focus:
                self._current_hint_text_color = self.theme_cls.disabled_hint_text_color
                self._current_right_lbl_color = self.theme_cls.disabled_hint_text_color
                if self.helper_text_mode == "persistent":
                    self._current_error_color = self.theme_cls.disabled_hint_text_color

    def on_width(self, instance, width):
        if any([self.focus, self.error, self._text_len_error]) and instance is not None:
            self._line_width = width
        self._msg_lbl.width = self.width
        self._right_msg_lbl.width = self.width
        self._hint_lbl.width = self.width

    def on_focus(self, *args):
        Animation.cancel_all(self, '_line_width', '_hint_y',
                             '_hint_lbl_font_size')
        if self.max_text_length is None:
            max_text_length = sys.maxsize
        else:
            max_text_length = self.max_text_length
        if len(self.text) > max_text_length or all([self.required, len(self.text) == 0, self.has_had_text]):
            self._text_len_error = True
        if self.error or all([self.max_text_length is not None and len(self.text) > self.max_text_length]):
            has_error = True
        else:
            if all([self.required, len(self.text) == 0, self.has_had_text]):
                has_error = True
            else:
                has_error = False

        if self.focus:
            self.has_had_text = True
            Animation.cancel_all(self, '_line_width', '_hint_y',
                                 '_hint_lbl_font_size')
            if len(self.text) == 0:
                Animation(_hint_y=dp(14),
                          _hint_lbl_font_size=sp(12), duration=.2,
                          t='out_quad').start(self)
            Animation(_line_width=self.width, duration=.2, t='out_quad').start(self)
            if has_error:
                Animation(duration=.2, _current_hint_text_color=self.error_color,
                          _current_right_lbl_color=self.error_color,
                          _current_line_color=self.error_color).start(self)
                if self.helper_text_mode == "on_error" and (self.error or self._text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                elif self.helper_text_mode == "on_error" and not self.error and not self._text_len_error:
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.helper_text_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.helper_text_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
            else:
                Animation(duration=.2, _current_hint_text_color=self.line_color_focus,
                          _current_right_lbl_color=self.theme_cls.disabled_hint_text_color).start(self)
                if self.helper_text_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                if self.helper_text_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.helper_text_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
        else:
            if len(self.text) == 0:
                Animation(_hint_y=dp(38),
                          _hint_lbl_font_size=sp(16), duration=.2,
                          t='out_quad').start(self)
            if has_error:
                Animation(duration=.2, _current_line_color=self.error_color,
                          _current_hint_text_color=self.error_color,
                          _current_right_lbl_color=self.error_color).start(self)
                if self.helper_text_mode == "on_error" and (self.error or self._text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                elif self.helper_text_mode == "on_error" and not self.error and not self._text_len_error:
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.helper_text_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.helper_text_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
            else:
                Animation(duration=.2, _current_line_color=self.line_color_focus,
                          _current_hint_text_color=self.theme_cls.disabled_hint_text_color,
                          _current_right_lbl_color=(0, 0, 0, 0)).start(self)
                if self.helper_text_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
                elif self.helper_text_mode == "persistent":
                    Animation(duration=.2, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)
                elif self.helper_text_mode == "on_focus":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)

                Animation(_line_width=0, duration=.2, t='out_quad').start(self)

    def on_text(self, instance, text):
        if len(text) > 0:
            self.has_had_text = True
        if self.max_text_length is not None:
            self._right_msg_lbl.text = "{}/{}".format(len(text), self.max_text_length)
            max_text_length = self.max_text_length
        else:
            max_text_length = sys.maxsize
        if len(text) > max_text_length or all([self.required, len(self.text) == 0, self.has_had_text]):
            self._text_len_error = True
        else:
            self._text_len_error = False
        if self.error or self._text_len_error:
            if self.focus:
                Animation(duration=.2, _current_hint_text_color=self.error_color,
                          _current_line_color=self.error_color).start(self)
                if self.helper_text_mode == "on_error" and (self.error or self._text_len_error):
                    Animation(duration=.2, _current_error_color=self.error_color).start(self)
                if self._text_len_error:
                    Animation(duration=.2, _current_right_lbl_color=self.error_color).start(self)
        else:
            if self.focus:
                Animation(duration=.2, _current_right_lbl_color=self.theme_cls.disabled_hint_text_color).start(self)
                Animation(duration=.2, _current_hint_text_color=self.line_color_focus,
                          _current_line_color=self.line_color_focus).start(self)
                if self.helper_text_mode == "on_error":
                    Animation(duration=.2, _current_error_color=(0, 0, 0, 0)).start(self)
        if len(self.text) != 0 and not self.focus:
            self._hint_y = dp(14)
            self._hint_lbl_font_size = sp(12)

    def on_text_validate(self):
        self.has_had_text = True
        if self.max_text_length is None:
            max_text_length = sys.maxsize
        else:
            max_text_length = self.max_text_length
        if len(self.text) > max_text_length or all([self.required, len(self.text) == 0, self.has_had_text]):
            self._text_len_error = True

    def _set_hint(self, instance, text):
        self._hint_lbl.text = text

    def _set_msg(self, instance, text):
        self._msg_lbl.text = text
        self.helper_text = text

    def _set_message_mode(self, instance, text):
        self.helper_text_mode = text
        if self.helper_text_mode == "persistent":
            Animation(duration=.1, _current_error_color=self.theme_cls.disabled_hint_text_color).start(self)

    def _set_max_text_length(self, instance, length):
        self.max_text_length = length
        self._right_msg_lbl.text = "{}/{}".format(len(self.text), length)

    def on_color_mode(self, instance, mode):
        if mode == "primary":
            self._update_primary_color()
        elif mode == "accent":
            self._update_accent_color()
        elif mode == "custom":
            self._update_colors(self.line_color_focus)

    def on_line_color_focus(self, *args):
        if self.color_mode == "custom":
            self._update_colors(self.line_color_focus)

    def on_touch_down(self, touch):
        if not touch.is_double_tap:
            self.focus = False
        else:
            #super(ICTextFieldPlain, self).on_touch_down(touch)
            self.focus = True
            self.select_text(0,0) #len(self.text)-1, len(self.text)-1)
            return


class BaseTextInputItem(ThemableBehavior, RectangularRippleBehavior,
                        ButtonBehavior, FloatLayout):
    """
    Base class to all TextInputItems. Not supposed to be instantiated on its own.
    """

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


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


class ICSearchInput(ThemableBehavior, BoxLayout, FocusBehavior):
    hint_text = StringProperty('hint text')
    text_input = ObjectProperty()
    text = StringProperty()

    def on_text_validate(self, instance, value):
        pass

    def on_cancel(self):
        self.text_input.text = ''
        self.focus = False

    def on_text(self, instance, value):
        self.text = value
