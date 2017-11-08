from kivy.app import App
from kivy.lang import Builder
import time
from kivymd.theming import ThemeManager
from kivyic.filebrowser import FileExplorer, get_home_directory
from kivy.uix.modalview import ModalView

from kivyic.dialog import FileExplorerDialog, ICDialog
from kivyic import path
from kivy.garden.filebrowser import LinkTree

#Builder.load_file(path + '/filebrowser.kv')

main_kv = '''
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar

#:import OneLineTextInputItem kivyic.textfields.OneLineTextInputItem
#:import ICFilterPanel kivyic.filteric.ICFilterPanel
#:import FileExplorer kivyic.filebrowser.FileExplorer
#:import get_home_directory kivyic.filebrowser.get_home_directory

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
            text: "Filter"
            on_release: app.root.ids.scr_mngr.current = 'filter'
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "Dialogs"
            on_release: app.root.ids.scr_mngr.current = 'dialogs'    
        NavigationDrawerIconButton:
            icon: 'checkbox-blank-circle'
            text: "File Explorer"
            on_release: app.root.ids.scr_mngr.current = 'fileexplorer'                    
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
                name: 'filter'
                GridLayout:
                    cols: 1
                    ICFilterPanel:
                        id: filter            
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
                name: 'dialogs'
                GridLayout:
                    id: dialogs_grid
                    rows: 1
                    Button:
                        size_hint: None, None
                        height: '48dp'
                        width: '100dp'
                        pos_hint: {'center_x': 0.5}
                        text: 'File Explorer'
                        on_release: app.open_file_dialog() 
            Screen:
                name: 'fileexplorer'
                GridLayout:
                    rows: 1
                    Button: 
                        text: 'File Explorer'
                        on_release: app.open_file_dialog()
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
        self.build_sample_filter(main_widget)
        return main_widget

    def open_file_dialog(self):
        #user_path = get_home_directory()
        mv = ModalView(size_hint=(.8,.8))
        #fe = FileExplorer(select_string='Select',
        #                  favorites=[(user_path, 'Documents')])
        fe = FileExplorer()
        #fe.bind(on_success=self._fbrowser_success,
        #        on_canceled=self._fbrowser_canceled,
        #        on_submit=self._fbrowser_submit)
        mv.add_widget(fe)
        mv.open()

    def build_sample_filter(self, widget):
        widget.ids.filter.add_filter('Cat:', ['Work Work Work', 'Home'])
        widget.ids.filter.add_filter('Sub:', ['Homework', 'Lawn care'])
        widget.ids.filter.add_filter('Type:', ['pdf', 'txt'])
        widget.ids.filter.add_filter('Cat:', ['Workshop', 'Home'])

if __name__ == '__main__':
    Sampler().run()
