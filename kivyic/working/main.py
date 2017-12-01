from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivymd.dialog import MDDialog
from kivymd.theming import ThemeManager
from kivy.uix.gridlayout import GridLayout

class DynamicWidget(object):
    @classmethod
    def spawn(cls, name, **attributes):
        new_class = type(name, (cls,), attributes)
        globals()[name] = new_class
        return new_class(name)

    def __init__(self, name, text):
        self.name = name
        self.text = text
t = Label
dclass = type("dc", (t,),{})
dlabel = dclass(text='2', size_hint_y=None, height=60, valign='middle', font_size=12)

t = Button
dbutton = dclass(text='3', size_hint_y=None, height=60, valign='middle', font_size=12)

class TestApp2(App):
    theme_cls = ThemeManager()
    filename = StringProperty()

    def build(self):
        g = GridLayout(cols=1)
        #s = DynamicWidget.spawn('2', text='2t')
        g.add_widget(Button(text='1', size_hint_y=None, height=60, valign='middle', font_size=12))
        g.add_widget(dlabel)
        g.add_widget(dbutton)
        return g


if __name__ == '__main__':
    TestApp2().run()