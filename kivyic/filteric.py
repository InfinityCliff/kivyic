from collections import defaultdict

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from  kivy.uix.behaviors.button import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty

from kivyic import path

from kivymd.theming import ThemeManager

Builder.load_file(path + '/filteric.kv')


class FilterTag(ButtonBehavior, BoxLayout):
    text = StringProperty()
    fg_button_label = ObjectProperty()  # X delete button
    tag_color = ListProperty()          # background color of filter tags
    tag_button_color = ListProperty()   # Color of filter tag X button
    tag_font_color = ListProperty()     # Color of tag font
    tag_border = ListProperty()         # color of border around tag

    def __init__(self, **kwargs):
        super(FilterTag, self).__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.tag_color = kwargs.get('tag_color', [1, 1, 1, 1])
        self.tag_button_color = kwargs.get('tag_button_color', [0, 0, 1, 1])
        self.tag_font_color = kwargs.get('tag_font_color', [0, 0, 0, 1])
        self.tag_border = kwargs.get('tag_border', [0, 0, 1, 1])

    def on_release(self):
        pass


class FilterGroup(BoxLayout):
    tag_spacing = NumericProperty()     # spacing between filter tags
    name = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_delete_tag')
        super(FilterGroup, self).__init__(**kwargs)
        self.tag_spacing = dp(kwargs.get('tag_spacing', 5))

    def add_tags(self, tags):
        for tag in tags:
            filter_tag = FilterTag(text=tag)
            self.ids.button_container.add_widget(filter_tag)
            filter_tag.bind(on_release=self.delete_tag)

    def delete_tag(self, filter_tag):
        self.ids.button_container.remove_widget(filter_tag)
        self.dispatch('on_delete_tag', self.name, filter_tag.text)

    def on_delete_tag(self, filter_group, filter_tag):
        pass

    def on_name(self, instance, value):
        self.ids.lbl.text = value[:3].capitalize() + ':'


class ICFilterPanel(BoxLayout):
    theme_cls = ThemeManager()
    filter_criteria_dict = defaultdict(list)
    container = ObjectProperty()  # ICFilter panel list

    spacing = NumericProperty(dp(2))
    padding = ListProperty()
    background_color = ListProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_empty_filter_list')
        super(ICFilterPanel, self).__init__(**kwargs)
        self.padding = [dp(5), dp(10), dp(5), dp(5)]
        self.kwargs_ = kwargs
        self.background_color = kwargs.get('background_color', [1, 1, 1, 1])

    def on_empty_filter_list(self, *args):
        pass

    def add_filter(self, text, filter_):
        filter_list = sorted(list(set(filter_).difference(set(self.filter_criteria_dict[text]))))  # only add unique items
        self.filter_criteria_dict[text].extend(filter_list)
        self.update_panel_display()

    def _remove_filter_group(self):
        # to remove the group from the display panel
        pass

    def _remove_filter_criteria(self, instance, filter_group, filter_tag):
        self.filter_criteria_dict[filter_group].remove(filter_tag)
        if len(self.filter_criteria_dict[filter_group]) == 0:
            del self.filter_criteria_dict[filter_group]
        self.update_panel_display()

    def update_panel_display(self, *largs):
        self.container.clear_widgets()
        if len(self.filter_criteria_dict.items()):
            for group, filter_vals in self.filter_criteria_dict.items():
                fg = FilterGroup()
                fg.name = group
                fg.add_tags(filter_vals)
                fg.bind(on_delete_tag=self._remove_filter_criteria)
                self.container.add_widget(fg)
            self.height = self.minimum_height
        else:
            self.dispatch('on_empty_filter_list')

    def apply_filter(self, data):
        """
        filtes data on previously selected filter criteria
        :param data: dict {'unique identifier': {'filter criteria name': [criteria list]}}
        :return: Sorted list
        """
        filtered_list = []
        for item, criterion in data.items():
            add_item = False
            for filter_group, filter_tags in self.filter_criteria_dict.items():
                if len(set(criterion[filter_group]) & set(filter_tags)) >= len(set(filter_tags)):
                    add_item = True
                else:
                    add_item = False
            if add_item:
                filtered_list.append(criterion['name'])

        return sorted(filtered_list)
