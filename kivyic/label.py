from kivy.lang import Builder

from kivymd.label import MDLabel  # TODO assimilate MDLabel
from kivy.properties import StringProperty

from kivyic import path

Builder.load_string('''
#: include ''' + path + '''/label.kv
''')


class ICIconLabel(MDLabel):
    icon = StringProperty('checkbox-blank-circle')
