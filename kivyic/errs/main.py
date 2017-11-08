from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button

from kivyic.errs.my_classes import ModalViewContent
from kivyic.filebrowser import FileExplorer

main_kv = '''
BoxLayout:
    Button:
        text: 'modal view'
        on_release: app.open_file_dialog()
'''


class TestApp2(App):

    def build(self):
        main_widget = Builder.load_string(main_kv)
        #but = Button(text='modal view')
        #but.bind(on_release=self.open_file_dialog)
        #main_widget.add_widget(but)
        return main_widget

    def open_file_dialog(self):
        mv = ModalView(size_hint=(.8,.8))
        mvc = FileExplorer()
        mv.add_widget(mvc)
        mv.open()



if __name__ == '__main__':
    TestApp2().run()