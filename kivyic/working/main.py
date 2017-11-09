from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivymd.dialog import MDDialog
from kivymd.theming import ThemeManager

from kivyic.dialog import ICDialog, FileExplorerDialog
from kivyic.filebrowser import FileExplorer
from kivyic.working.my_classes import ModalViewContent

main_kv = '''
GridLayout:
    Button:
        size_hint: None, None
        size: 100, 20
        text: 'modal view'
        on_release: app.open_file_dialog()
'''


class TestApp2(App):
    theme_cls = ThemeManager()
    filename = StringProperty()
    def build(self):
        main_widget = Builder.load_string(main_kv)
        #but = Button(text='modal view')
        #but.bind(on_release=self.open_file_dialog)
        #main_widget.add_widget(but)
        return main_widget

    def open_file_dialog(self):
        mv = FileExplorerDialog(size_hint=(.8, .8), title='File Explorer',
                                content_fit='window')

        mv.bind(file_name=self.setter('filename'))
        mv.open()

    def on_filename(self, instance, value):
        print(self.filename)

    def open_file_dialog2(self):
        mvc = FileExplorer()
        mv = ICDialog(size_hint=(.8, .8), content=mvc, title='File Explorer',
                      content_fit='window')
        mv.add_action_button("Import",
                             action=lambda *x: mvc.ok())
        mv.add_action_button("Dismiss",
                             action=lambda *x: mv.dismiss())
        mv.open()



if __name__ == '__main__':
    TestApp2().run()