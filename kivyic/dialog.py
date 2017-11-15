# -*- coding: utf-8 -*-

import os

from kivy.app import App
from kivy.lang import Builder
from kivy import Logger
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, OptionProperty, \
                            BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.modalview import ModalView
from kivy.uix.popup import PopupException
from kivy.clock import Clock

from kivymd.textfields import MDTextField
from kivymd.theming import ThemableBehavior, ThemeManager
from kivymd.elevationbehavior import RectangularElevationBehavior
from kivymd.button import MDFlatButton

from kivyic import path
from kivyic.fileexplorer import FileExplorer, get_home_directory

from functools import partial

Builder.load_file(path + '/dialog.kv')

__all__ = ['ICDialog', 'FileExplorerDialog', 'DialogOKDismiss']
__version__ = '0.1'

# BUG - helper text and hint text can not be set from python, only in kv, NEED TO TEST
class InputDialog(MDTextField):
    """
    A text input field to be inserted into a dialog box
    """
    pass


class ICDialog(ThemableBehavior, RectangularElevationBehavior, ModalView):
    """
    Dialog box with the ability to add action buttons
    """
    title = StringProperty('KivyIC Dialog Box')
    '''
    Title of the Dialog Box.

    :attr:`title` is an :class:`~kivy.properties.StringProperty` and
    defaults to 'KivyIC Dialog Box'.
    
    .. versionadded:: 0.1
    '''

    content = ObjectProperty(None)
    '''
    Container widget for what will be displayed in the Dialog Box.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    
    .. versionadded:: 0.1
    '''

    content_fit = OptionProperty('items', options=['window', 'items'])
    md_bg_color = ListProperty([0, 0, 0, .2])

    _container = ObjectProperty()
    _action_buttons = ListProperty([])
    _action_area = ObjectProperty()
    action_area_width = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(_action_buttons=self._update_action_buttons,
                  auto_dismiss=lambda *x: setattr(self.shadow, 'on_release',
                                                  self.shadow.dismiss if self.auto_dismiss else None))

    def add_action_button(self, text, action=None):
        """Add an :class:`FlatButton` to the right of the action area.

        :param icon: Unicode character for the icon
        :type icon: str or None
        :param action: Function set to trigger when on_release fires
        :type action: function or None
        """
        button = MDFlatButton(text=text,
                              size_hint=(None, None),
                              height=dp(36))
        if action:
            button.bind(on_release=action)
        # FIX - fix color
        button.text_color = self.theme_cls.primary_color
        button.md_bg_color = self.theme_cls.bg_light
        self._action_buttons.append(button)

    def add_widget(self, widget):
        if self._container:
            if self.content:
                raise PopupException(
                        'Popup can have only one widget as content')
            self.content = widget
        else:
            super(ICDialog, self).add_widget(widget)

    def open(self, *largs):
        '''Show the view window from the :attr:`attach_to` widget. If set, it
        will attach to the nearest window. If the widget is not attached to any
        window, the view will attach to the global
        :class:`~kivy.core.window.Window`.
        '''
        if self._window is not None:
            Logger.warning('ModalView: you can only open once.')
            return self
        # search window
        self._window = self._search_window()
        if not self._window:
            Logger.warning('ModalView: cannot open view, no window found.')
            return self
        self._window.add_widget(self)
        self._window.bind(on_resize=self._align_center,
                          on_keyboard=self._handle_keyboard)
        self.center = self._window.center
        self.bind(size=self._align_center)
        a = Animation(_anim_alpha=1., d=self._anim_duration)
        a.bind(on_complete=lambda *x: self.dispatch('on_open'))
        a.start(self)
        return self

    def dismiss(self, *largs, **kwargs):
        '''Close the view if it is open. If you really want to close the
        view, whatever the on_dismiss event returns, you can use the *force*
        argument:
        ::

            view = ModalView(...)
            view.dismiss(force=True)

        When the view is dismissed, it will be faded out before being
        removed from the parent. If you don't want animation, use::

            view.dismiss(animation=False)

        '''
        if self._window is None:
            return self
        if self.dispatch('on_dismiss') is True:
            if kwargs.get('force', False) is not True:
                return self
        if kwargs.get('animation', True):
            Animation(_anim_alpha=0., d=self._anim_duration).start(self)
        else:
            self._anim_alpha = 0
            self._real_remove_widget()
        return self

    def on_content(self, instance, value):
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

    def on_touch_down(self, touch):
        if self.disabled and self.collide_point(*touch.pos):
            return True
        return super(ICDialog, self).on_touch_down(touch)

    def _update_action_buttons(self, *args):
        self._action_area.clear_widgets()
        self.action_area_width = 0
        for btn in self._action_buttons:
            btn.content.texture_update()
            btn.width = btn.content.texture_size[0] + dp(16)
            self.action_area_width += btn.width
            self._action_area.add_widget(btn)
        spacing = sum(self._action_area.spacing) - self._action_area.spacing[0]
        self.action_area_width += spacing

class FileExplorerDialog(ICDialog):
    title = StringProperty('File Explorer Dialog')
    '''
    Title of the dialog window.
    
    :data:`title` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'File Explorer Dialog'.
    .. version added:: 0.1
    '''

    # FIX - works on windows, need to set to $Home on Linux
    initial_directory = StringProperty()
    '''
    Starting directory for file explorer.

    :data:`initial_directory` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'C:/Users/<user name>/' for windows, $HOME for Linux.
    .. version added:: 0.1
    '''

    filter = ListProperty()
    '''
    Filter to apply to files shown in file view.

    :data:`filter` is an :class:`~kivy.properties.ListProperty`,
    defaults to '*.*'.
     
    .. version added:: 0.1
    '''

    # TODO -- v 0.2 - add ability to select multiple files
    file_name_s = StringProperty()
    '''
    Name of selected file(s).  If multiple files are selected, each file will
    be separated by a comma.

    :data:`file_name_s` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.
     
    .. version added:: 0.1
    '''
    def __init__(self, **kwargs):
        super(FileExplorerDialog, self).__init__(**kwargs)
        user_path = os.path.join(get_home_directory(), 'Documents')

        file_explorer = FileExplorer(select_string='Select',
                                     favorites=[(user_path, 'Documents')])
        file_explorer.bind(on_success=self._fbrowser_success,
                           on_canceled=self._fbrowser_canceled,
                           on_submit=self._fbrowser_submit)
        file_explorer.file_selection_container.clear_widgets()
        self.content = file_explorer

        self.add_action_button("Dismiss",
                               action=lambda *x: file_explorer.dispatch('on_canceled'))
        self.add_action_button("OK",
                               action=lambda *x: file_explorer.dispatch('on_success'))

        Clock.schedule_once(partial(self._post_init, file_explorer))

    def _post_init(self, file_explorer, *args):
        file_explorer.filter_button.width = self.action_area_width

    def _fbrowser_canceled(self, instance):
        self.dismiss()

    def _fbrowser_success(self, instance):
        # ERR - self.file_name_s = instance.selection[0] / IndexError: list index out of range
        self.file_name_s = instance.selection[0]
        self.dismiss()

    def _fbrowser_submit(self, instance):
        self.file_name_s = instance.selection[0]
        self.dismiss()

    def add_button(self, buttons):
        """
        add action butttons via a dict
        :param buttons: dict: {button name: action}
        :return: None
        """
        for text, action in buttons.items():
            self.add_action_button(text, action=lambda *x: action())


class DialogOKDismiss(ICDialog):
    """
    Ok - Dismiss Dialog with Input Text field

    Parameters:
        text: str: value of input text field
        helper_text: str: helper text to provide feedback to user
        hint_text: str: to provide feedback to user

    Usage:
        bind to response to determine user action, true if click OK false if Dismiss
        bind to text to get information typed
    """
    text = StringProperty()
    '''
    String in the Input Text Field. Can be used to set of retrieve data.

    :data:`text` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.
     
    .. version added:: 0.1
    '''

    hint_text = StringProperty()
    '''
    Text that will show in text input prior to receiving focus, setting mode
    to persistant will cause to raise above input line while user is typing.

    :data:`hint_text` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.
     
    .. version added:: 0.1
    '''

    helper_text = StringProperty()
    '''
    Text that will show below text input. Text will stay before and after focus

    :data:`helper_text` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.
     
    .. version added:: 0.1
    '''

    response = BooleanProperty()
    '''
    Stores action of user when exiting dialog.  
    True if user clicks ok.
    False if user clicks Dismiss.

    :data:`response` is an :class:`~kivy.properties.BooleanProperty`,
     
    .. version added:: 0.1
    '''

    def __init__(self, **kwargs):
        super(DialogOKDismiss, self).__init__(**kwargs)
        content = InputDialog(hint_text=self.hint_text,
                              helper_text=self.helper_text)
        self.bind(text=self.setter(content.text))
        self.content = content
        self.add_action_button("OK",
                               action=lambda *x: self.click(True))
        self.add_action_button("Dismiss",
                               action=lambda *x: self.click(False))
        self.content.focus = True

    def click(self, response):
        self.response = response
        self.dismiss()


class TestApp(App):
    title = 'Dialog Test App'
    theme_cls = ThemeManager()

    def build(self):
        self.root = BoxLayout()
        self.open_file_dialog()
        return self.root

    def open_file_dialog(self):
        d = FileExplorerDialog()
        d.open()

if __name__ == '__main__':
    TestApp().run()