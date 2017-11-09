from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button

Builder.load_file('my_classes.kv')


class ModalViewContent(BoxLayout):
    pass


if __name__ == '__main__':
    class TestApp(App):

        def build(self):
            root = BoxLayout()
            mv = ModalView(size_hint=(.8,.8))

            mvc = ModalViewContent()
            mv.add_widget(mvc)
            but = Button(text='mv')
            but.bind(on_release=mv.open)
            root.add_widget(but)

            return root

    TestApp().run()
