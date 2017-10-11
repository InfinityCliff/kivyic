from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivymd.dialog import MDDialog

Builder.load_string('''
<InputDialog>:
    text: text
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    MDTextField:
        id: text
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

# Popup--------------------------------------------------------------
class InputDialog(BoxLayout):
    note_input = ObjectProperty()
    height_input = NumericProperty()
    text = StringProperty()
    hint_text = StringProperty()
    helper_text = StringProperty
    def __init__(self, text, **kwargs):
        super(InputDialog, self).__init__(**kwargs)
        self.note_input.text = text


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
    secondary_text = StringProperty()

    def __init__(self, **kwargs):
        super(DialogOKDismiss, self).__init__(**kwargs)
        content = InputDialog(text=self.secondary_text)

        self.content = content

        self.add_action_button("OK",
                               action=lambda *x: self.dismiss())
        self.add_action_button("Dismiss",
                               action=lambda *x: self.dismiss())

        # ^Popup------------------------------------------------------------^