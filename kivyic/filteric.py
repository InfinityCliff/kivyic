from collections import defaultdict

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty


from kivyic import path

Builder.load_file(path + '/filteric.kv')


class FilterGroupButton(BoxLayout):
    text = StringProperty()
    fg_button_label = ObjectProperty()
    #height = NumericProperty()

    def __init__(self, **kwargs):
        super(FilterGroupButton, self).__init__(**kwargs)
        self.text = kwargs.get('text', '')
        #self.height = dp(kwargs.get('height', 15))

# TODO  WORKING HERE TO SET UP PARAMETERS ON INIT
class FilterGroup(BoxLayout):
    tag_spacing = NumericProperty()   #spacing between filter tags

    def __init__(self, **kwargs):
        super(FilterGroup, self).__init__(**kwargs)
        self.tag_spacing = dp(kwargs.get('tag_spacing', 5))


class ICFilterPanel(BoxLayout):
    filter_dict = defaultdict(list)
    container = ObjectProperty()  # ICFilter panel list

    spacing = NumericProperty(dp(2))
    padding = ListProperty()

    def __init__(self, **kwargs):
        super(ICFilterPanel, self).__init__(**kwargs)
        self.padding = [dp(5), dp(10), dp(5), dp(5)]

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
                fgb = FilterGroupButton(text=val)
                fg.ids.button_container.add_widget(fgb)

            self.container.add_widget(fg)
        self.height = self.minimum_height