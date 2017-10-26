from collections import defaultdict

from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.properties import DictProperty

from kivyic import path

Builder.load_file(path + '/filteric.kv')


class FilterGroupButton(GridLayout):
    pass


class FilterGroup(GridLayout):
    pass


class ICFilterPanel(GridLayout):
    filter_dict = defaultdict(list)

    def add_filter(self, text, filter_):
        self.filter_dict['text'].extend(filter_)
