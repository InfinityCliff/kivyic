from distutils.core import setup

setup(
        name='kivyic',
        version='0.1.dev3',
        packages=['kivyic'],
        package_data={'': ['*.kv']},
        include_package_data=True,
        url='https://github.com/InfinityCliff/kivyic',
        license='MIT',
        author='Infinity Cliff',
        author_email='kevin.williams@InfinityCliff.com',
        description='Implementation of Kivy',
        install_requires=['kivy', 'kivymd', 'apiclient', 'oauth2client']
)
