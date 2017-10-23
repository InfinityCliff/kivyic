from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField

Builder.load_string('''
<InputDialog>:
    size_hint_y: None
    multiline: True
    hint_text: root.hint_text
    helper_text: root.helper_text
    helper_text_mode: "persistent"
        
<EditNotesPopup>:
    size_hint: .8, None
    height: dp(400)
    auto_dismiss: False

<DialogOKDismiss>:
    size_hint: .8, None
    height: dp(400)
    auto_dismiss: False
''')


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

