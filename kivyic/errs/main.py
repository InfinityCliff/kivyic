from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button

from kivyic.errs.my_classes import ModalViewContent
from kivyic.filebrowser import FileExplorer
from kivymd.dialog import MDDialog
from kivymd.theming import ThemeManager

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

    def build(self):
        main_widget = Builder.load_string(main_kv)
        #but = Button(text='modal view')
        #but.bind(on_release=self.open_file_dialog)
        #main_widget.add_widget(but)
        return main_widget

    def open_file_dialog(self):
        mvc = FileExplorer()
        #mvc = Button(text='test', valign='top', size_hint_y=None)
        #mvc.bind(texture_size=mvc.setter('size'))
        mvc.size_hint_y = None
        mvc.height = '200dp'
        mv = MDDialog(size_hint=(.8, .8), content=mvc, title='File Explorer')
        mv.add_action_button("Dismiss",
                             action=lambda *x: mv.dismiss())
        #mv.add_widget(mvc)
        mv.open()



if __name__ == '__main__':
    TestApp2().run()