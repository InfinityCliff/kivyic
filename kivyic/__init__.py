# -*- coding: utf-8 -*-
import os
import glob

from kivy import Logger
from kivy.properties import ListProperty

__version_info__ = (0, 1, 6)
__version__ = '0.1.dev6'


path = os.path.dirname(__file__)
#fonts_path = os.path.join(path, "fonts/")
#images_path = os.path.join(path, 'images/')
alphabet = [chr(i-1+ord('A')) for i in range(1, 27)]
numbers = [str(n) for n in (range(0, 10))]
symbols = [chr(s) for s in range(33, 47)] + [chr(95)]

alpha_num_sym = sorted(alphabet + symbols + numbers)

Logger.info("KivyIC: KivyIC version: {}".format(__version__))


def ColorProperty(rgba):
    return [x / 255 for x in rgba[:3]] + [rgba[-1]]


class ColorProperty1(ListProperty):
    color_property = ListProperty()

    def __init__(self, **kwargs):
        super(ColorProperty1, self).__init__(**kwargs)

    def on_color_property(self, rgba, *args):
        cp = [x / 255 for x in rgba[:3]] + [rgba[-1]]


def summary():
    # print a summary of each .py file in the module
    # list file name, __all__ and __version__
    import importlib
    for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
        if file.split('.')[1] == 'py' and file != '__init__.py':
            print('--------------------------')
            print(file)
            imp = file.split('.')[0]
            try:
                t = importlib.__import__('kivyic.' + imp, globals(), locals(), ['__all__'], 0)
                print('__all__:', t.__all__)
            except:
                print('__all__:', 'None')


if __name__ == '__main__':
    summary()