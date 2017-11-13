# -*- coding: utf-8 -*-
'''
FileExplorer
===========

The :class:`FileExplorer` widget is an advanced file browser. You use it
similarly to FileChooser usage.

It provides a shortcut bar with links to special and system directories.
When touching next to a shortcut in the links bar, it'll expand and show
all the directories within that directory. It also facilitates specifying
custom paths to be added to the shortcuts list.

To create a FileExplorer which prints the currently selected file as well as
the current text in the filename field when 'Select' is pressed, with
a shortcut to the Documents directory added to the favorites bar::

    import os
    from kivy.app import App

    class TestApp(App):

        def build(self):
            user_path = os.path.join(get_home_directory(), 'Documents')
            fe = FileExplorer(select_string='Select',
                              favorites=[(user_path, 'Documents')])
            fe.bind(on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled,
                    on_submit=self._fbrowser_submit)

            return fe

        def _fbrowser_canceled(self, instance):
            print('cancelled, Close self.')

        def _fbrowser_success(self, instance):
            print(instance.selection)

        def _fbrowser_submit(self, instance):
            print(instance.selection)

    TestApp().run()

:Events:
    `on_canceled`:
        Fired when the `Cancel` buttons `on_release` event is called.

    `on_success`:
        Fired when the `Select` buttons `on_release` event is called.

    `on_success`:
        Fired when a file has been selected with a double-tap.

.. image:: _static/filebrowser.png
    :align: right
'''

__all__ = ('FileExplorer', )
__version__ = '0.0-dev'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeViewLabel, TreeView

try:
    from kivy.garden.filechooserthumbview import FileChooserThumbView as \
        IconView
except:
    pass
from kivy.properties import (ObjectProperty, StringProperty, OptionProperty, NumericProperty,
                             ListProperty, BooleanProperty)
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.compat import PY2
from kivy.uix.filechooser import FileChooserLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

import string

import os
from os.path import sep, dirname, expanduser, isdir, join, isfile
from os import walk
from sys import getfilesystemencoding
from functools import partial

from kivyic import path
from kivyic.menu import ICDropdown

if platform == 'win':
    from ctypes import windll, create_unicode_buffer


def get_home_directory():
    if platform == 'win':
        user_path = expanduser('~')

        if not isdir(join(user_path, 'Desktop')):
            user_path = dirname(user_path)

    else:
        user_path = expanduser('~')

    if PY2:
        user_path = user_path.decode(getfilesystemencoding())

    return user_path


def get_drives():
    drives = []
    if platform == 'win':
        bitmask = windll.kernel32.GetLogicalDrives()
        GetVolumeInformationW = windll.kernel32.GetVolumeInformationW
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                name = create_unicode_buffer(64)
                # get name of the drive
                drive = letter + u':'
                res = GetVolumeInformationW(drive + sep, name, 64, None,
                                            None, None, None, 0)
                drives.append((drive, name.value))
            bitmask >>= 1
    elif platform == 'linux':
        drives.append((sep, sep))
        drives.append((expanduser(u'~'), '~/'))
        places = (sep + u'mnt', sep + u'media')
        for place in places:
            if isdir(place):
                for directory in next(walk(place))[1]:
                    drives.append((place + sep + directory, directory))
    elif platform == 'macosx' or platform == 'ios':
        drives.append((expanduser(u'~'), '~/'))
        vol = sep + u'Volume'
        if isdir(vol):
            for drive in next(walk(vol))[1]:
                drives.append((vol + sep + drive, drive))
    return drives


Builder.load_file(path + '/filebrowser.kv')


class TreeLabel(TreeViewLabel):
    path = StringProperty('')
    '''Full path to the location this node points to.

    :class:`~kivy.properties.StringProperty`, defaults to ''
    '''

    def __init__(self, **kwargs):
        super(TreeLabel, self).__init__(**kwargs)
        self.register_event_type('on_change_path')

    def on_change_path(self, *args):
        pass


class LinkTree(TreeView):
    _favs = ObjectProperty(None)
    _computer_node = None
    _libs = ObjectProperty()


    def fill_tree(self, fav_list):
        user_path = get_home_directory()
        self._favs = self.add_node(TreeLabel(text='Favorites', is_open=True,
                                             no_selection=True))
        self.reload_favs(fav_list)

        self._libs = self.add_node(TreeLabel(text='Libraries', is_open=True,
                                       no_selection=True))
        places = ('Documents', 'Music', 'Pictures', 'Videos')
        for place in places:
            if isdir(join(user_path, place)):
                tl = TreeLabel(text=place, path=join(user_path, place))
                #tl.bind(on_change_path=app.root.update_path)
                self.add_node(tl, self._libs)
        self._computer_node = self.add_node(TreeLabel(text='Computer', is_open=True, no_selection=True))
        self._computer_node.bind(on_touch_down=self._drives_touch)
        self.reload_drives()

    def _drives_touch(self, obj, touch):
        if obj.collide_point(*touch.pos):
            self.reload_drives()

    def reload_drives(self):
        nodes = [(node, node.text + node.path) for node in \
                 self._computer_node.nodes if isinstance(node, TreeLabel)]
        sigs = [s[1] for s in nodes]
        nodes_new = []
        sig_new = []
        for path, name in get_drives():
            if platform == 'win':
                text = u'{}({})'.format((name + ' ') if name else '', path)
            else:
                text = name
            nodes_new.append((text, path))
            sig_new.append(text + path + sep)
        for node, sig in nodes:
            if sig not in sig_new:
                self.remove_node(node)
        for text, path in nodes_new:
            if text + path + sep not in sigs:
                tl = TreeLabel(text=text, path=path + sep)
                self.add_node(tl, self._computer_node)

    def reload_favs(self, fav_list):
        user_path = get_home_directory()
        favs = self._favs
        remove = []
        for node in self.iterate_all_nodes(favs):
            if node != favs:
                remove.append(node)
        for node in remove:
            self.remove_node(node)
        places = ('Desktop', 'Downloads')
        for place in places:
            if isdir(join(user_path, place)):
                tl = TreeLabel(text=place, path=join(user_path, place))
                self.add_node(tl, favs)
        for path, name in fav_list:
            if isdir(path):
                tl = TreeLabel(text=name, path=path)
                self.add_node(tl, favs)

    def trigger_populate(self, node):
        print('repopulating')
        app = App.get_running_app()
        if not node.path or node.nodes:
            return
        parent = node.path
        _next = next(walk(parent))
        if _next:
            for path in _next[1]:
                tl = TreeLabel(text=path, path=parent + sep + path)
                tl.bind(on_change_path=app.root.update_path)
                self.add_node(tl, node)


class FileLayout(FileChooserLayout):
    VIEWNAME = 'fileview'
    _ENTRY_TEMPLATE = 'FileView'

    def __init__(self, **kwargs):
        super(FileLayout, self).__init__(**kwargs)
        self.fbind('on_entries_cleared', self.scroll_to_top)

    def scroll_to_top(self, *args):
        self.ids.scrollview.scroll_y = 1.0

    def is_dir(self, directory, filename):
        return isdir(join(directory, filename))

    def is_file(self, directory, filename):
        return isfile(join(directory, filename))

    def on_entry_added(self, node, parent=None):
        pass

    def on_entries_cleared(self):
        pass

    def on_subentry_to_entry(self, subentry, entry):
        pass

    def on_remove_subentry(self, subentry, entry):
        pass

    def on_submit(self, selected, touch=None):
        pass


class FileExplorer(BoxLayout):
    file_layout_controller = ObjectProperty()
    file_layout = ObjectProperty()
    filter_button = ObjectProperty()
    file_selection_container = ObjectProperty()
    dropdown = ObjectProperty()

    __events__ = ('on_canceled', 'on_success', 'on_submit')

    select_state = OptionProperty('normal', options=('normal', 'down'))
    '''State of the 'select' button, must be one of 'normal' or 'down'.
    The state is 'down' only when the button is currently touched/clicked,
    otherwise 'normal'. This button functions as the typical Ok/Select/Save
    button.

    :data:`select_state` is an :class:`~kivy.properties.OptionProperty`.
    '''
    cancel_state = OptionProperty('normal', options=('normal', 'down'))
    '''State of the 'cancel' button, must be one of 'normal' or 'down'.
    The state is 'down' only when the button is currently touched/clicked,
    otherwise 'normal'. This button functions as the typical cancel button.

    :data:`cancel_state` is an :class:`~kivy.properties.OptionProperty`.
    '''

    select_string = StringProperty('Ok')
    '''Label of the 'select' button.

    :data:`select_string` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'Ok'.
    '''

    cancel_string = StringProperty('Cancel')
    '''Label of the 'cancel' button.

    :data:`cancel_string` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'Cancel'.
    '''

    filename = StringProperty('')
    '''The current text in the filename field. Read only. When multiselect is
    True, the list of selected filenames is shortened. If shortened, filename
    will contain an ellipsis.

    :data:`filename` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.

    .. versionchanged:: 1.1
    '''

    selection = ListProperty([])
    '''Read-only :class:`~kivy.properties.ListProperty`.
    Contains the list of files that are currently selected in the current tab.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.selection`.

    .. versionchanged:: 1.1
    '''

    path = StringProperty(u'/')
    '''
    :class:`~kivy.properties.StringProperty`, defaults to the current working
    directory as a unicode string. It specifies the path on the filesystem that
    browser should refer to.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.path`.

    .. versionadded:: 1.1
    '''

    filters = ListProperty([])
    ''':class:`~kivy.properties.ListProperty`, defaults to [], equal to '\*'.
    Specifies the filters to be applied to the files in the directory.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.filters`.

    Filering keywords that the user types into the filter field as a comma
    separated list will be reflected here.

    .. versionadded:: 1.1
    '''

    filter_dirs = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Indicates whether filters should also apply to directories.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.filter_dirs`.

    .. versionadded:: 1.1
    '''

    show_hidden = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether hidden files and folders should be shown.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.show_hidden`.

    .. versionadded:: 1.1
    '''

    multiselect = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether the user is able to select multiple files or not.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.multiselect`.

    .. versionadded:: 1.1
    '''

    dirselect = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether directories are valid selections or not.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.dirselect`.

    .. versionadded:: 1.1
    '''

    rootpath = StringProperty(None, allownone=True)
    '''
    Root path to use instead of the system root path. If set, it will not show
    a ".." directory to go up to the root path. For example, if you set
    rootpath to /users/foo, the user will be unable to go to /users or to any
    other directory not starting with /users/foo.
    :class:`~kivy.properties.StringProperty`, defaults to None.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.rootpath`.

    .. versionadded:: 1.1
    '''

    favorites = ListProperty([])
    '''A list of the paths added to the favorites link bar. Each element
    is a tuple where the first element is a string containing the full path
    to the location, while the second element is a string with the name of
    path to be displayed.

    :data:`favorites` is an :class:`~kivy.properties.ListProperty`,
    defaults to '[]'.
    '''

    file_type_filters = [
        {'viewclass': 'ICFilterMenuItem',
         'text': ('All Files', '*.*')},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('PDF Files', '*.pdf')},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('Text Files', '*.txt')},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('Example', 'item',)},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('Example', 'item')},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('Example', 'item')},
        {'viewclass': 'ICFilterMenuItem',
         'text': ('Example', 'item')}]

    def on_success(self):
        pass

    def on_canceled(self):
        pass

    def on_submit(self):
        pass

    def __init__(self, **kwargs):
        super(FileExplorer, self).__init__(**kwargs)
        self.file_layout_controller.bind(on_submit=self.update_file)
        Clock.schedule_once(self._post_init)

    def _post_init(self, *largs):
        self.ids.path_ti.text = self.file_layout_controller.path
        self.file_layout_controller.bind(selection=partial(self._attr_callback, 'selection'),
                                         path=partial(self._attr_callback, 'path'),
                                         filters=partial(self._attr_callback, 'filters'),
                                         filter_dirs=partial(self._attr_callback, 'filter_dirs'),
                                         show_hidden=partial(self._attr_callback, 'show_hidden'),
                                         multiselect=partial(self._attr_callback, 'multiselect'),
                                         dirselect=partial(self._attr_callback, 'dirselect'),
                                         rootpath=partial(self._attr_callback, 'rootpath'))
        for node in self.ids.link_tree.iterate_all_nodes():

            if isinstance(node, TreeLabel):
                node.bind(on_change_path=self.update_path)

    def _attr_callback(self, attr, obj, value):
        setattr(self, attr, getattr(obj, attr))

    def update_path(self, instance, new_path):
        new_path = os.path.abspath(new_path)
        self.file_layout_controller.path = new_path
        self.ids.path_ti.text = new_path

    def update_file(self, instance, paths, *args):
        self.ids.selected_file.text = os.path.normpath(paths[0])

    def update_filter(self, value):
        self.filters = [value[1]]


if __name__ == '__main__':
    from kivy.app import App

    class TestApp(App):

        def build(self):
            user_path = os.path.join(get_home_directory(), 'Documents')
            fe = FileExplorer(select_string='Select',
                              favorites=[(user_path, 'Documents')])
            fe.bind(on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled,
                    on_submit=self._fbrowser_submit)

            return fe

        def _fbrowser_canceled(self, instance):
            print('cancelled, Close self.')

        def _fbrowser_success(self, instance):
            print(instance.selection)
            print('path', instance.path)

        def _fbrowser_submit(self, instance):
            print(instance.selection)

    TestApp().run()
