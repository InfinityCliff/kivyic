# https://github.com/kivy/kivy/wiki/A-draggable-scrollbar-using-a-slider


#!python
import kivy

from kivy.app import App
#from kivy.lang.builder import Builder
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation

from kivy.properties import StringProperty, ObjectProperty, NumericProperty, OptionProperty, ReferenceListProperty, \
                            ListProperty, AliasProperty, DictProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout


from kivy.uix.popup import Popup

from kivyic import path, alphabet

from functools import partial
from operator import itemgetter, attrgetter, methodcaller


from kivy.uix.recycleview import RecycleView
Builder.load_file(path + '/scrollbar.kv')

__all__ = ['AlphaScrollView']



class AlphaSBLabel(Label):
    """
    Label on the AlphaSlider

    .. versionadded:: 0.1
    """
    pass


class AlphaSlider(Slider):
    labels = ListProperty()
    '''
    List of labels along the slider

    :attr:`labels` is an :class:`~kivy.properties.ListProperty` and
    defaults to [].

    .. versionadded:: 0.1
    '''

    layout = ObjectProperty()
    '''
    Pointer to GridLayout containing labels

    :attr:`layout` is an :class:`~kivy.uix.gridlayout.GridLayout`.

    .. versionadded:: 0.1
    '''

    def __init__(self, **kwargs):
        super(AlphaSlider, self).__init__(**kwargs)

    def on_labels(self, *args):
        """
        Fired when labels is set. adds contents of labels list to layout.
        :param args:
        :return: None

        .. versionadded:: 0.1
        """
        self.layout.clear_widgets()
        for label in self.labels:
            lbl = AlphaSBLabel(text=str(label))
            self.layout.add_widget(lbl)


class AlphaScrollViewException(Exception):
    # TODO set up this AlphaScrollViewException
    """
    AlphaScrollView exception, fired when multiple content widgets are added to the
    scrollview.

    .. versionadded:: 0
    """


class AlphaScrollItem(BoxLayout):
    """
    Base class for view classes to extend that will be displayed in the
    AlphaScrollView.

    .. versionadded:: 0.1
    """
    attr_dict = DictProperty()
    '''
    Dictionary of data that will populate the view i.e. {'text': 'spam'}.
    must contain at least one item that is the sort_key set in AlphaScrollView.
    
    Attributes sent in attr_dict should be tied to values in respective class
    kv definition.
    
    :attr:`attr_dict` is an :class:`~kivy.properties.DictProperty` and
    defaults to {}.

    .. versionadded:: 0.1
    '''

    def on_attr_dict(self, obj, attrs):
        """
        Fires when data changes.  Moves through list of items in data and assigns to
        respective attributes.  Allows for classes that extend this class to have
        a dynamic number of attributes that can be sent in one dictionary.

        :param obj:
        :param attrs: new value for attr_dict
        :return:

        .. versionadded:: 0.1
        """
        for attr, val in attrs.items():
            setattr(self, attr, val)


class AlphaScrollItemLabel(AlphaScrollItem):
    """
    AlphaScrollItem view_class that has a label to display the text field.

    .. versionadded:: 0.1
    """
    text = StringProperty()
    '''
    Text field.

    :attr:`text` is an :class:`~kivy.properties.StringProperty` and
    defaults to {}.

    .. versionadded:: 0.1
    '''


class AlphaScrollItemButton(AlphaScrollItemLabel):
    # TODO (v0.2) add ability to add an action to the button
    """
    AlphaScrollItem view_class that has a Button to display the text field.

    .. versionadded:: 0.1
    """
    pass


class AlphaScrollViewSeparators(AlphaScrollItemLabel):
    # TODO look at adding GridLayouts for each letter, will simplify sorting -- only need to sort respective letter group
    # can have height go to zero or remove widget if no children
    """
    AlphaScrollItem view_class that has a Label to display the text field.

    This view class is the separator/header between each letter group

    .. versionadded:: 0.1
    """
    pass


class AlphaScrollBin(BoxLayout):
    bin_container = ObjectProperty()
    text = StringProperty('bin label')

    def clear_container(self):
        self.bin_container.clear_widgets()
# WORKING HERE develop method to sort bins, try rearanging list of children

# https://stackoverflow.com/questions/3173154/move-an-item-inside-a-list
# If you want to move an item that's already in the list to the specified position, you would have to delete it and insert it at the new position:

# l.insert(newindex, l.pop(oldindex))

class AlphaScrollView(ScrollView):
    """
    ScrollView container inside of AlphaScrollPane.

    Contains a GridLayout (self._container) that holds the view_class

    .. versionadded:: 0.1
    """

    content = DictProperty()
    '''
    contains the attribute items that are used in the AlphaScrollItem display.
    
    format:
    {'sort_key': value, 'attributes': [{list of dict}, {dict contain attributes for view_class}]
    :attr:`content` is an :class:`~kivy.properties.DictProperty` and
    defaults to {}.

    .. versionadded:: 0.1
    '''

    _container = ObjectProperty()
    '''
    Pointer to the GridLayout that contains the AlphaScrollItem's

    :attr:`_container` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    .. versionadded:: 0.1
    '''

    _view_class = None
    '''
    AlphaScrollItem class that will be displayed for each item in the AlphaScrollView.

    :attr:`_view_class` defaults to None.

    .. versionadded:: 0.1
    '''

    sort_key = None
    # TODO add an exception if this item is not set
    '''
    Attribute in self._view_class that will be used to sort the items
    
    Required and must be set.
    
    :attr:`sort_key` defaults to None.

    .. versionadded:: 0.1
    '''

    separators = ListProperty()
    # TODO if bins are used this can be removed
    '''
    list of values that will be used for title of separators in AlphaScrollItemSeparators

    :attr:`separators` is an :class:`~kivy.properties.ListProperty` and
    defaults to [].

    .. versionadded:: 0.1
    '''
    alpha_bins = DictProperty()

    def __init__(self, **kwargs):
        for l in alphabet:
            self.alpha_bins[l] = AlphaScrollBin(text=l)
        super(AlphaScrollView, self).__init__(**kwargs)
        self._container.bind(minimum_height=self._container.setter('height'))
        for l in alphabet:
            self._container.add_widget(self.alpha_bins[l])

    def on_content(self, instance, new_content):
        """
        Fires when self.content is changed.
        Sets self.sort_key and calls refresh_view.

        :param instance: calling object
        :param new_content: new value for self.content

        .. versionadded:: 0.1
        """
        self.sort_key = new_content['sort_key']
        self._view_class = new_content['view_class']
        if self._container:
            self.refresh_view()

    def clear_bins(self):
        for letter in alphabet:
            self.alpha_bins[letter].clear_container()

    def on__container(self, instance, new__container):
        """
        Fires when self._container is changed.
        Sets self.sort_key and calls refresh_view.

        :param instance: calling object
        :param new__container:  new value for self._container

        .. versionadded:: 0.1
        """
        if new__container is None or self.content is None or self._view_class is None:
            return
        self.refresh_view()


    def refresh_view(self):
        """
        Clears hte scrollview and redraws the widgets in the scrollview, adds separators between each letter group

        .. versionadded:: 0.1
        """
        self.clear_bins()
        for attributes in self.content['attributes']:
            alpha_bin = attributes[self.sort_key][0]
            self.alpha_bins[alpha_bin].add_widget(self._view_class(attr_dict=attributes))

    def add_item(self, new_data_dict):
        """
        Add an item to the self.content Dictionary
        :param new_data_dict:
        :return:

        .. versionadded:: 0.1
        """
        print(self.content)
        # add item to content
        self.content['attributes'].append(new_data_dict)

        # add item to respective bin
        alpha_bin = new_data_dict[self.sort_key][0]
        self.alpha_bins[alpha_bin].add_widget(self._view_class(attr_dict=new_data_dict))

    def add_separator(self, separator, data_list):
        """
        Adds a separator to list

        :param separator: separator text to add to separator list and data list
        :param data_list: 
        :return: appended data list

        .. versionadded:: 0.1
        """
        data_list.append({'text': separator})
        self.separators.append(separator)
        return data_list

    def scroll_to(self, widget, padding=10, animate=True):
        """
        Overrides ScrollView.scroll to allow scrolling to selected letter from slider

        Scrolls the viewport to ensure that the given letter/widget is visible,
        optionally with padding and animation. If animate is True (the
        default), then the default animation parameters will be used.
        Otherwise, it should be a dict containing arguments to pass to
        :class:`~kivy.animation.Animation` constructor.

        :param widget: widget or letter to scroll to
        :param padding: int: distance from top of window to top of selected widget
        :param animate: bool: will it animate

        .. versionadded:: 0.1
        """
        if type(widget) is str:
            self.scroll_to_letter(widget)
        else:
            super().scroll_to(widget, padding=10, animate=True)

    def scroll_to_letter(self, letter, padding=10, animate=True):
        """
        Finds first instance of letter and sends the respective widget to self._scroll_to_letter

        :param letter: letter to scroll to
        :param padding: int: distance from top of window to top of selected widget
        :param animate: bool: will it animate

        .. versionadded:: 0.1
        """
        for child in reversed(self._container.children):
            if child.text[0] == letter:
                self._scroll_to_letter(child, padding=10, animate=True)
                break

    def _scroll_to_letter(self, widget, padding=10, animate=True):
        # TODO - see if can send back to super() to do scroll, do not think this is any different than scroll view
        # call to super in scroll_to_letter above

        """
        Scrolls the viewport to ensure that the given widget is visible

        :param widget:
        :param padding: int: distance from top of window to top of selected widget
        :param animate: bool: will it animate
        :return:

        .. versionadded:: 0.1
        """
        if not self.parent:
            return

        # if _viewport is layout and has pending operation, reschedule
        if hasattr(self._viewport, 'do_layout'):
            if self._viewport._trigger_layout.is_triggered:
                Clock.schedule_once(
                        lambda *dt: self.scroll_to(widget, padding, animate))
                return

        if isinstance(padding, (int, float)):
            padding = (padding, padding)

        pos = self.parent.to_widget(*widget.to_window(*widget.pos))
        cor = self.parent.to_widget(*widget.to_window(widget.right,
                                                      widget.top))

        dx = dy = 0

        if cor[1] < self.top:
            dy = self.top - pos[1] - widget.height - dp(padding[1])
        else:
            dy = self.top - cor[1] - dp(padding[1])

        if pos[0] < self.x:
            dx = self.x - pos[0] + dp(padding[0])
        elif cor[0] > self.right:
            dx = self.right - cor[0] - dp(padding[0])

        dsx, dsy = self.convert_distance_to_scroll(dx, dy)
        sxp = min(1, max(0, self.scroll_x - dsx))
        syp = min(1, max(0, self.scroll_y - dsy))

        if animate:
            if animate is True:
                animate = {'d': 0.2, 't': 'out_quad'}
            Animation.stop_all(self, 'scroll_x', 'scroll_y')
            Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp


class AlphaScrollPane(RelativeLayout):
    letter = StringProperty()
    '''
    Letter from slider to send to AlphaScrollView for scrolling to

    :attr:`letter` is an :class:`~kivy.properties.StringProperty` and
    defaults to ''.

    .. versionadded:: 0.1
    '''

    scrollview = ObjectProperty()
    '''
    Pointer to AlphaScrollView.  Created and added in __init__.

    :attr:`scrollview` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to AlphaScrollView().

    .. versionadded:: 0.1
    '''

    slider = ObjectProperty()
    '''
    Pointer to AlphaSlider.  Created and added in __init__.

    :attr:`slider` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to AlphaSlider().

    .. versionadded:: 0.1
    '''

    content = DictProperty()
    '''
    Passed to AlphaScrollView, see AlphaScrollView.content for more information.
    
    .. versionadded:: 0.1
    '''

    container = ObjectProperty()
    '''
    Pointer to GridLayout that contains the slider and scroll view

    :attr:`container` is an :class:`~kivy.properties.StringProperty` and
    defaults to ''.

    .. versionadded:: 0.1
    '''

    def __init__(self, **kwargs):

        super(AlphaScrollPane, self).__init__(**kwargs)

        self.container = StackLayout(orientation='lr-bt')

        self.scrollview = AlphaScrollView(size_hint=(0.9, 0.95), content=self.content)

        self.slider = AlphaSlider(min=1, max=26, value=26, orientation='vertical', step=1, size_hint=(0.1, 0.95), value_track=False)
        self.slider.labels = alphabet
        self.slider.bind(value=partial(self.scroll_change, self.scrollview))

        self.container.add_widget(self.scrollview)
        self.container.add_widget(self.slider)
        self.add_widget(self.container)

    def on_letter(self, *args):
        self.find_letter()

    def add_item(self, data):
        self.scrollview.add_item(data)

    def find_letter(self):
        self.scrollview.scroll_to(self.letter)

    def value_to_letter(self, value):
        self.letter = chr(abs(value - 26) + ord('A'))

    def scroll_change(self, scrlv, slider, value):
        self.value_to_letter(value)
        scrlv.scroll_y = slider.value_normalized

    def slider_change(self, s, instance, value):
        if value >= 0:
            #this to avoid 'maximum recursion depth exceeded' error
            s.value = value


class ScrollApp(App):

    def build(self):
        b = BoxLayout(padding=[dp(10)])
        content = []
        for letter in alphabet:
            for i in range(1, 6):
                content.append({'text': letter + str(i)})
        content_dict = {'sort_key': 'text', 'attributes': content, 'view_class': AlphaScrollItemButton}
        asp = AlphaScrollPane(content=content_dict)
        asp.add_item({'text': 'A7'})
        asp.add_item({'text': 'A6'})
        asp.add_item({'text': 'A6'})

        b.add_widget(asp)
        return b


if __name__ == '__main__':
    ScrollApp().run()
