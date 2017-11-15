from distutils.core import setup

setup(
        name='kivyic',
        version='0.0',
        packages=['kivyic'],
        url='https://github.com/InfinityCliff/kivyic',
        license='MIT',
        author='Infinity Cliff',
        author_email='kevin.williams@InfinityCliff.com',
        description='Implementation of Kivy',
        install_requires=['kivy', 'kivymd', 'apiclient', 'oauth2client']
)
