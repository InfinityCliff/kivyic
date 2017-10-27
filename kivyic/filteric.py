from collections import defaultdict

from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

from kivyic import path

Builder.load_file(path + '/filteric.kv')


class FilterGroupButton(GridLayout):
    text = StringProperty()


class FilterGroup(BoxLayout):
    pass


class ICFilterPanel(BoxLayout):
    filter_dict = defaultdict(list)
    container = ObjectProperty()  # ICFilter panel list

    def add_filter(self, text, filter_):
        filter_list = sorted(list(set(filter_).difference(set(self.filter_dict[text]))))  # only add unique items
        self.filter_dict[text].extend(filter_list)
        self.update()

    def update(self):
        self.container.clear_widgets()
        for group, filter_vals in self.filter_dict.items():
            fg = FilterGroup()
            fg.ids.lbl.text = group
            for val in filter_vals:
                fg.ids.button_container.add_widget(FilterGroupButton(text=val))
            self.container.add_widget(fg)
