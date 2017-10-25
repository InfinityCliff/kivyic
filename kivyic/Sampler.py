from kivy.app import App
from kivy.lang import Builder
from kivymd.theming import ThemeManager

main_kv = '''
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar

#:import OneLineTextInputItem kivyic.textfields.OneLineTextInputItem

NavigationLayout:
    id: nav_layout
    MDNavigationDrawer:
        id: nav_drawer
        NavigationDrawerToolbar:
            title: "Navigation Drawer"
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Text Fields"
            on_release: app.root.ids.scr_mngr.current = 'textfields'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "blank"
            on_release: app.root.ids.scr_mngr.current = 'blank'
    BoxLayout:
        orientation: 'vertical'
        Toolbar:
            id: toolbar
            title: 'KivyIC Text Fields'
            md_bg_color: app.theme_cls.primary_color
            background_palette: 'Primary'
            background_hue: '500'
            left_action_items: [['menu', lambda x: app.root.toggle_nav_drawer()]]
            right_action_items: [['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]
        ScreenManager:
            id: scr_mngr
            Screen:
                name: 'textfields'
                GridLayout:
                    cols: 1
                    ScrollView:
                        do_scroll_x: False
                        MDList:
                            ICSearchInput:
                            OneLineListItem:
                                text: 'OneLineListItem KivyMD'
                            OneLineTextInputItem:
                                text: 'OneLineTextInputItem KivyIC'

                            TwoLineListItem:
                                text: 'TwoLineListItem KivyMD'
                                secondary_text: 'This is a song, and these are the words'
                            TwoLineTextInputItem:
                                text: 'TwoLineTextInputItem KivIC'
                                secondary_text: 'This is a song, and these are the words'

                            ThreeLineListItem:
                                text: 'ThreeLineListItem KivyMD'
                                secondary_text: 'This is a song, \\nand these are the words'
                            ThreeLineTextInputItem:
                                text: 'ThreeLineListItem KivyMD'
                                secondary_text: 'This is a song, \\nand these are the words'

                            OneLineIconListItem:
                                text: "Single-line item with left icon KivyMD"
                                IconLeftSampleWidget:
                                    id: li_icon_1
                                    icon: 'checkbox-blank-outline'
                            OneLineIconTextInputItem:
                                text: "Single-line item with left icon KivyIC"
                                IconLeftSampleWidget:
                                    id: li_icon_1
                                    icon: 'checkbox-blank-outline'

                            TwoLineIconListItem:
                                text: "Two-line item... KivyMD"
                                secondary_text: "...with left icon"
                                IconLeftSampleWidget:
                                    id: li_icon_2
                                    icon: 'checkbox-blank-outline'
                            TwoLineIconTextInputItem:
                                text: "Two-line item... KivyIC"
                                secondary_text: "...with left icon"
                                IconLeftSampleWidget:
                                    id: li_icon_2
                                    icon: 'checkbox-blank-outline'

                            ThreeLineIconListItem:
                                text: "Three-line item... KivyMD"
                                secondary_text: "...with left icon..." + '\\n' + "and third line!"
                                IconLeftSampleWidget:
                                    id: li_icon_3
                                    icon: 'checkbox-blank-outline'
                            ThreeLineIconTextInputItem:
                                text: "Three-line item... KivyIC"
                                secondary_text: "...with left icon..." + '\\n' + "and third line!"
                                IconLeftSampleWidget:
                                    id: li_icon_3
                                    icon: 'checkbox-blank-outline'
            Screen:
                name: 'blank'
                GridLayout:
                    cols: 1
                    
'''


class Sampler(App):
    title = 'KivyIC Sampler'
    theme_cls = ThemeManager()

    def build(self):
        main_widget = Builder.load_string(main_kv)
        return main_widget

if __name__ == '__main__':
    Sampler().run()
