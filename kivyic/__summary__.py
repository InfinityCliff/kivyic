# -*- coding: utf-8 -*-
import os
import importlib

from kivyic import path

dic = {}
# print a summary of each .py file in the module
# list file name, __all__ and __version__
for file in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
    if file.split('.')[1] == 'py' and file != '__init__.py':
        imp = file.split('.')[0]
        try:
            t = importlib.__import__('kivyic.' + imp, globals(), locals(), ['__all__'], 0)
            dic[file] = {'all': t.__all__}
        except:
            dic[file] = {'all': 'None'}

        try:
            t = importlib.__import__('kivyic.' + imp, globals(), locals(), ['__version__'], 0)
            dic[file] = {'version': t.__version__}
        except:
            dic[file] = {'version': 'None'}

print("KivyIC: Summary of Modules")

for k in dic.keys():
    print('--------------------------')
    print(k)
    print(dic[k]['version'])
    print(dic[k]['all'])

