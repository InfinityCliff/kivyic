import os

from kivy.lang import Builder
from kivy import Logger
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.filechooser import FileChooserListLayout
from kivy.animation import Animation

from kivy.uix.modalview import ModalView
from kivy.uix.popup import PopupException
from kivy.graphics import Rectangle, Color
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

from kivyic import path
from kivyic.filebrowser import FileExplorer, get_home_directory

from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField
from kivymd.theming import ThemableBehavior
from kivymd.elevationbehavior import RectangularElevationBehavior
from kivymd.button import MDFlatButton
from kivymd.menu import MDDropdownMenu

Builder.load_file(path + '/dialog.kv')



class InputDialog(MDTextField):
    #note_input = ObjectProperty()
    height_input = NumericProperty()
    #text_input = ObjectProperty()
    #text = StringProperty()
    #hint_text = StringProperty()
    #helper_text = StringProperty()

    def __init__(self, text, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        #self.note_input.text = text
        #Clock.schedule_once(
        #    self.bind(text=self.setter(self.text_input.text)))


class EditNotesPopup(MDDialog):
    def __init__(self, title, secondary_text, caller, **kwargs):
        super(EditNotesPopup, self).__init__(**kwargs)
        content = InputDialog(text=secondary_text)
        self.title = title
        self.content = content

        self.add_action_button("OK",
                               action=lambda *x: caller.add_task_container(self.title,
                                                                           self.content.note_input.text))
        self.add_action_button("Dismiss",
                               action=lambda *x: self.dismiss())


class ICDialog(ThemableBehavior, RectangularElevationBehavior, ModalView):
    title = StringProperty('KivyIC Dialog Box')
    '''Title of the Dialog Box.

    :attr:`title` is an :class:`~kivy.properties.StringProperty` and
    defaults to 'KivyIC Dialog Box'.
    '''

    content = ObjectProperty(None)
    '''Container widget for what will be displayed in the Dialog Box.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    md_bg_color = ListProperty([0, 0, 0, .2])

    _container = ObjectProperty()
    _action_buttons = ListProperty([])
    _action_area = ObjectProperty()

    def __init__(self, **kwargs):
        super(ICDialog, self).__init__(**kwargs)
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
        # TODO - fix color
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
        for btn in self._action_buttons:
            btn.content.texture_update()
            btn.width = btn.content.texture_size[0] + dp(16)
            self._action_area.add_widget(btn)


class FileExplorerDialog(ICDialog):
    title = StringProperty()                # dialog box title
    initial_directory = StringProperty()    # starting directory for file dialog
    filter = ListProperty()                 # file filter list
    filter_index = NumericProperty(2)       # current active file filter, defaults to all *.*
    action_buttons = ListProperty()         # Buttons in the dialog
    file_name = StringProperty()            # Name of selected file

    def __init__(self, **kwargs):
        super(FileExplorerDialog, self).__init__(**kwargs)
        user_path = os.path.join(get_home_directory(), 'Documents')
        self.content = FileExplorer()
        #self.content = FileExplorer(select_string='Select',
        #                            favorites=[(user_path, 'Documents')])
        #self.content.bind(on_success=self._fbrowser_success,
        #          on_canceled=self._fbrowser_canceled,
        #          on_submit=self._fbrowser_submit)

    def add_button(self, buttons):
        for text, action in buttons.items():
            self.add_action_button(text, action=lambda *x: action())


class DialogOKDismiss(MDDialog):
    text = StringProperty()
    secondary_text = StringProperty()
    #ok = ObjectProperty()

    __events__ = ('on_ok', 'on_open', 'on_dismiss')

    def __init__(self, **kwargs):
        super(DialogOKDismiss, self).__init__(**kwargs)
        #self.register_event_type('on_ok')
        content = InputDialog(text=self.text)
        self.text = 'default'
        self.bind(text=self.setter(content.text))
        self.content = content
        self.add_action_button("OK",
                               action=lambda *x: self.ok())
        self.add_action_button("Dismiss",
                               action=lambda *x: self.dismiss())
        self.content.focus=True

    def ok(self):
        self.dispatch('on_ok')
        return

    def on_ok(self):
        self.dismiss()

