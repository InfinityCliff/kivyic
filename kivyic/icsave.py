# -*- coding: utf-8 -*-

__all__ = []
__version__ = '0.0'

app_name = ''
location = ''
filetype = ''

def icsave(file, application_name, save_location='local'):
    app_name = application_name
    location = save_location
    filetype = file.split('.')[1]
    if filetype.upper() == 'TXT':
        save_txt()
    elif filetype.upper() == 'JSON':
        save_json()
    elif filetype.upper() == 'CSV':
        save_csv()

def save_txt():
    pass

def save_json():
    pass

def save_csv():
    pass
