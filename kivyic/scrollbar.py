# https://github.com/kivy/kivy/wiki/A-draggable-scrollbar-using-a-slider


#!python
import kivy

from kivy.app import App
#from kivy.lang.builder import Builder
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import dp, sp
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
from kivyic.debug import dprint

from functools import partial
from operator import itemgetter, attrgetter, methodcaller

import inspect

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
        Clock.schedule_once(self._post_init)

    def _post_init(self, *args):
        self.add_labels()

    def add_labels(self, *args):
        """
        Fired when labels is set. adds contents of labels list to layout.
        :param args:
        :return: None

        .. versionadded:: 0.1
        """
        self.labels.sort()

        if self.layout:
            self.layout.clear_widgets()
            for label in self.labels:
                lbl = AlphaSBLabel(text=str(label))
                self.layout.add_widget(lbl)
        self.size_slider()

    def size_slider(self):
        l_count = len(self.labels)
        self.max = l_count
        self.value = l_count

        #print(self.parent.size)


        #print('slider height   :', self.height)
        #print('layout height   :', self.layout.height)
        #print('layout size     :', self.layout.size)
        #print('layout min size :', self.layout.minimum_height)

        #print('padding         :', self.padding)

class AlphaScrollViewException(Exception):
    """
    AlphaScrollView exception, fired when multiple content widgets are added to the
    scrollview.

    .. versionadded:: 0
    """
    pass


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

    order = NumericProperty(0)

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
    def __repr__(self):
        return '<AlphaScrollItemButton>: ' + str(self.attr_dict)


class AlphaBin(GridLayout):
    bin_container = ObjectProperty()
    bin_title = StringProperty('bin label')
    sort_key = StringProperty()

    def sort_bin(self):
        self.bin_container.children = sorted(self.bin_container.children, key=lambda k: getattr(k, self.sort_key), reverse=True)

    def clear_widgets(self):
        self.bin_container.clear_widgets()

    def add_widget(self, widget, index=0):
        if isinstance(widget, dict):
            attr_dict = dict(widget)
            del attr_dict['view_class']
            widget_ = widget['view_class'](attr_dict=attr_dict)
            self.bin_container.add_widget(widget_)
            self.sort_bin()
            return widget_
        else:
            super(AlphaBin, self).add_widget(widget, index)

    def __str__(self):
        return 'AlphaBin: ' + self.bin_title

    def __repr__(self):
        bc = [b.text for b in self.bin_container.children]
        return 'AlphaBin: ' + self.bin_title + "\n" + str(bc) + "\n"

    @property
    def not_empty(self):
        if len(self.bin_container.children) > 0:
            return True
        return False


class AlphaBinView(GridLayout):
    bins = DictProperty()
    content = ObjectProperty()
    '''
    contains the attribute items that are used in the AlphaBin display.

    format:
    {'sort_key': value, 'attributes': [{list of dict}, {dict contain attributes for view_class}]
    :attr:`content` is an :class:`~kivy.properties.DictProperty` and
    defaults to {}.

    .. versionadded:: 0.1
    '''
    sort_key = StringProperty()

    def on_item_list(self, obj, *args):
        print(obj)

    def __init__(self, **kwargs):
        super(AlphaBinView, self).__init__(**kwargs)
        #self.bin_headers = alphabet
        for l in alphabet:
            b = AlphaBin(bin_title=l)
            self.bins[l] = b
            self.add_widget(b)

    def on_content(self, obj, new_content):
        if new_content:
            self.sort_key = new_content['sort_key']
            for item in new_content['attributes']:
                self.add_widget(item)

    def add_widget(self, widget, index=0):
        if isinstance(widget, dict):
            letter = widget[self.sort_key][0]
            # create bin item and add to respective bin and append to item list
            self.bins[letter].sort_key = self.sort_key
            self.bins[letter].add_widget(widget)
        else:
            super().add_widget(widget, index)

    def clear_widgets(self, bin_name=None):
        if bin_name:
            for bin_ in bin_name:
                self.bins[bin_].clear_widgets()
        else:
            for bin_ in self.bins.values():
                bin_.clear_widgets()

    def labels(self):
        return [b for b in self.bins.keys() if self.bins[b].not_empty]


class AlphaScrollView(ScrollView):
    """
    ScrollView container inside of AlphaScrollPane.

    AlphaBinView is added to this widget to contain the scoll items

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

    _alpha_bins = ObjectProperty()
    '''
    Contains the bins to hold the scrollview items.

    :attr:`alpha_bins` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to AlphaBinView.

    .. versionadded:: 0.1
    '''

    def __init__(self, **kwargs):
        super(AlphaScrollView, self).__init__(**kwargs)
        self._alpha_bins = AlphaBinView(cols=1)
        self._alpha_bins.content = self.content
        self._alpha_bins.bind(minimum_height=self._alpha_bins.setter('height'))
        self.add_widget(self._alpha_bins)

    def on_content(self, obj, value, *args):
        if self._alpha_bins:
            self._alpha_bins.content = value

    def add_widget(self, widget, index=0):
        """

        :param widget: dict or widget: if dict will pass to alpha_bins, must conform to
            { dict_item: item_val, 'view_class': cls }
            dict_item (can be more than one, but one must be the sort_key)
        :param index:
        """
        if isinstance(widget, dict):
            self._alpha_bins.add_widget(widget)
            return
        try:
            super().add_widget(widget, index)
        except:
            # TODO - fix raise
            raise AlphaScrollViewException('AlphaScrollPane is a ScrollView and can accept only one widget')

    @property
    def bin_labels(self):
        return self._alpha_bins.labels()

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
            super().scroll_to(widget, padding=0, animate=True)

    def scroll_to_letter(self, letter, padding=10, animate=True):
        """
        Finds first instance of letter and sends the respective widget to self._scroll_to_letter

        :param letter: letter to scroll to
        :param padding: int: distance from top of window to top of selected widget
        :param animate: bool: will it animate

        .. versionadded:: 0.1
        """
        self._scroll_to_letter(self._alpha_bins.bins[letter])

    def _scroll_to_letter(self, widget, padding=10, animate=True):
        """
        Scrolls the viewport to ensure that the given widget is visible.  Always puts bin title at the top,
        which is why this is similar to scrollview.scroll_to

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
            # subtracts the widget.height to place at top of view
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

        self.container = GridLayout(rows=1)
        self.scrollview = AlphaScrollView(size_hint=(0.9, 0.95), content=self.content)

        self.slider = AlphaSlider(min=1, orientation='vertical', step=1, #size_hint=(0.1, 0.95),
                                  value_track=False, labels=self.scrollview.bin_labels)

        self.slider.bind(value=partial(self.scroll_change, self.scrollview))

        self.container.add_widget(self.scrollview)
        self.container.add_widget(self.slider)
        self.add_widget(self.container)

    def on_content(self, obj, value, *args):
        if self.scrollview:
            self.scrollview.content = value

    def on_letter(self, *args):
        self.find_letter()

    def add_widget(self, widget, index=0):
        if isinstance(widget, dict):
            self.scrollview.add_widget(widget)
            return
        super().add_widget(widget, index)

    def find_letter(self):
        self.scrollview.scroll_to(self.letter)

    def value_to_letter(self, value):
        if type(value) is int:
            self.letter = chr(abs(value - 26) + ord('A'))
        else:
            self.letter = value.upper()

    def scroll_change(self, scrlv, slider, value):
        if len(slider.labels) == 0:
            alphalist = alphabet
        else:
            alphalist = slider.labels
        letter = list(reversed(alphalist))[value-1]
        self.value_to_letter(letter)
        scrlv.scroll_y = slider.value_normalized

    @staticmethod
    def slider_change(s, instance, value):
        if value >= 0:
            # this to avoid 'maximum recursion depth exceeded' error
            s.value = value


class ScrollApp(App):
    asp = ObjectProperty

    def build(self):
        b = BoxLayout(padding=[dp(10)])
        content = []
        for letter in alphabet:
            for i in range(1, 6):
                content.append({'text': letter + str(i), 'view_class': AlphaScrollItemButton})
        content_dict = {'sort_key': 'text', 'attributes': content}
        self.asp = AlphaScrollPane(content=content_dict)
        self.asp.add_widget({'text': 'A7', 'view_class': AlphaScrollItemButton})
        self.asp.add_widget({'text': 'A6', 'view_class': AlphaScrollItemButton})
        self.asp.add_widget({'text': 'A6', 'view_class': AlphaScrollItemButton})

        b.add_widget(self.asp)
        return b


if __name__ == '__main__':
    ScrollApp().run()
