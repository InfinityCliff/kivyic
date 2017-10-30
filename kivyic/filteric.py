from collections import defaultdict

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from  kivy.uix.behaviors.button import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty

from kivyic import path

from kivymd.theming import ThemeManager

Builder.load_file(path + '/filteric.kv')


class FilterGroupButton(ButtonBehavior, BoxLayout):
    text = StringProperty()
    fg_button_label = ObjectProperty()  # X delete button
    tag_color = ListProperty()          # background color of filter tags
    tag_button_color = ListProperty()   # Color of filter tag X button
    tag_font_color = ListProperty()     # Color of tag font
    tag_border = ListProperty()         # color of border around tag

    def __init__(self, **kwargs):
        super(FilterGroupButton, self).__init__(**kwargs)
        self.text = kwargs.get('text', '')
        self.tag_color = kwargs.get('tag_color', [1, 1, 1, 1])
        self.tag_button_color = kwargs.get('tag_button_color', [0, 0, 1, 1])
        self.tag_font_color = kwargs.get('tag_font_color', [0, 0, 0, 1])
        self.tag_border = kwargs.get('tag_border', [0, 0, 1, 1])

    def on_release(self):
        pass
        #self.remove_widget(self)


class FilterGroup(BoxLayout):
    tag_spacing = NumericProperty()     # spacing between filter tags
    name = StringProperty()

    def __init__(self, **kwargs):
        super(FilterGroup, self).__init__(**kwargs)
        self.tag_spacing = dp(kwargs.get('tag_spacing', 5))

    def add_tags(self, tags):
        for tag in tags:
            fgb = FilterGroupButton(text=tag)
            self.ids.button_container.add_widget(fgb)
            fgb.bind(on_release=self.delete_tag)

    def delete_tag(self, instance):
        self.ids.button_container.remove_widget(instance)

    def on_name(self, instance, value):
        self.ids.lbl.text = value[:3].capitalize() + ':'

class ICFilterPanel(BoxLayout):
    theme_cls = ThemeManager()
    filter_dict = defaultdict(list)
    container = ObjectProperty()  # ICFilter panel list

    spacing = NumericProperty(dp(2))
    padding = ListProperty()
    background_color = ListProperty()

    def __init__(self, **kwargs):
        super(ICFilterPanel, self).__init__(**kwargs)
        self.padding = [dp(5), dp(10), dp(5), dp(5)]
        self.kwargs_ = kwargs
        self.background_color = kwargs.get('background_color', [1, 1, 1, 1])

    def add_filter(self, text, filter_):
        filter_list = sorted(list(set(filter_).difference(set(self.filter_dict[text]))))  # only add unique items
        self.filter_dict[text].extend(filter_list)
        self.update()

    def update(self):
        self.container.clear_widgets()
        for group, filter_vals in self.filter_dict.items():
            fg = FilterGroup()
            fg.name = group
            fg.add_tags(filter_vals)
            #for val in filter_vals:
            #    fgb = FilterGroupButton(text=val)
            #    fg.ids.button_container.add_widget(fgb)
            #    fgb.bind(on_release=self.delete_tag)
            self.container.add_widget(fg)
        self.height = self.minimum_height

    def apply_filter(self, data):
        lst = []
        for item, criterion in data.items():
            add_file = False
            #print('------------------------------')
            #print(criterion['name'], criterion)
            #print(self.filter_dict)
            for f_group, f in self.filter_dict.items():
                if len(set(criterion[f_group]) & set(f)) >= len(set(f)):
                    add_file = True
                else:
                    add_file = False
            #print('add file: ', add_file)
            if add_file:
                lst.append(criterion['name'])

        print(sorted(lst))
        return sorted(lst)

        #filter_cat = False
        #filter_sub = False
        #filter_type = False
        #app = App.get_running_app()
        #meta = app.METADATA[os.path.join(LOCAL_STORAGE_PATH, item[0].upper(), item)]

        #if len(self.filter_dict['category']) == 0 or \
        #        (len(set(self.filter_dict['category']) & set(meta['category'])) >= len(self.filter_dict['category'])):
        #    filter_cat = True

        #if len(self.filter_dict['subject']) == 0 or \
        #        (len(set(self.filter_dict['subject']) & set(meta['subject'])) >= len(self.filter_dict['subject'])):
        #    filter_sub = True

        #if len(self.filter_dict['type']) == 0 or \
        #        (len(set(self.filter_dict['type']) & set(meta['type'])) >= len(self.filter_dict['type'])):
        #    filter_type = True

        #return all([filter_cat, filter_sub, filter_type])