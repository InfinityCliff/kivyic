# -*- coding: utf-8 -*-
import pickle

from kivyic._secret.app_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from kivyic.network import internet_online
from kivyic import material_resources as mat_rsc
from kivyic.label import ICIconLabel
from kivyic.button import ICIconButton

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pprint
import random

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock

from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty, ListProperty, DictProperty

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from kivy.graphics.texture import Texture

from kivymd.theming import ThemeManager
from kivymd.button import MDFlatButton, BaseFlatButton, BasePressedButton, BaseRoundButton

Builder.load_file('music_player.kv')


class MPIconButton(ICIconButton):
    icon = StringProperty('checkbox-blank-circle')


class MPBaseButton(ToggleButton):
    pass


class Library(Widget):
    music_library = None
    library_loaded = False
    play_list = ListProperty()

    def __init__(self, **kwargs):
        super(Library, self).__init__(**kwargs)
        self.library_loaded = self.load_local_library()

    def add_music_library(self, lib):
        self.music_library = lib
        self.library_loaded = True
        self.save_local_library()

    def shuffle_songs(self):
        lst = []
        for _, album in self.music_library.items():
            lst.extend(album['tracks'])
        print(lst)
        self.play_list = lst
        random.shuffle(self.play_list)

    def shuffle_albums(self):
        albums = [self.music_library[k] for k in self.music_library if k == 'album_id']
        print(albums)

    def load_local_library(self):
        try:
            with open('./rsc/local_library.p', 'rb') as filename:
                music_library = pickle.load(filename)
        except FileNotFoundError:
            print('toast: no local library File Found. Downloading...')
            return False
        print('toast: local library File Found, loading...')
        self.music_library = music_library
        return True

    def save_local_library(self):
        print('toast: saving local library...')
        filename = open('./rsc/local_library.p', 'wb')
        pickle.dump(self.music_library, filename)
        filename.close()

    def test(self):
        print('*** running test, Library ***')


from spotipy import oauth2
import six
import six.moves.urllib.parse as urllibparse
import base64

SCOPE = 'user-library-read'


class SpotifyClient(Library):

    client_credentials_manager = None
    sp = None
    username = StringProperty()
    token = None

    def __init__(self, **kwargs):
        super(SpotifyClient, self).__init__(**kwargs)

    def show_user(self):
        user = self.sp.user(self.username)
        pprint.pprint(user)

    def download_library(self):
        library = {}
        scope = 'user-library-read'
        self.token = self.get_token(scope)
        sp = spotipy.Spotify(auth=self.token)
        if self.token:
            print('toast: downloading library...')
            albums = sp.current_user_saved_albums()
            while True:
                for item in albums['items']:
                    print(item['album']['name'])
                    library[item['album']['id']] = {'name': item['album']['name'],
                                                    'artist': item['album']['artists'][0]['name'],
                                                    'tracks': [track['name'] for track in item['album']['tracks']['items']]}
                if albums['next']:
                    albums = sp._get(albums['next'])
                else:
                    break
        else:
            print("toast: Can't get token for", self.username)
        self.add_music_library(library)

    def test(self):
        sp = spotipy.Spotify(auth=self.token)
        if self.token:
            print('toast: downloading library...')
            albums = sp.current_user_saved_albums()
            while True:
                for item in albums['items']:
                    print(item['album']['name'])
                if albums['next']:
                    albums = sp._get(albums['next'])
                else:
                    break
        else:
            print("toast: Can't get token for", self.username)
        super().test()


class IpodClient:
    pass


class USBClient:
    pass


class HDClient:
    pass


# Bottle Example ------------------------------------
# https://stackoverflow.com/questions/25711711/spotipy-authorization-code-flow

# Flask Example -------------------------------------
# https://gist.github.com/kemitche/9749639


from bottle import route, run, request, abort, Bottle


STATE = StringProperty()


class BottleServerInterface(Widget):
    server_interface_oauth2 = None
    code = StringProperty()

    def __init__(self, oauth2, **kwargs):
        super(BottleServerInterface, self).__init__(**kwargs)
        self.server_interface_oauth2 = oauth2

    def bottle_server(self):
        start_bottle_server(callback=self.code_return)

    def code_return(self, code):
        print('code returned')
        self.code = code



app = Bottle()


@app.route('/')
def make_authorization_url():
    pass
    # print('make_authorization_url_1')
    # from uuid import uuid4
    # state = str(uuid4())
    # save_created_state(state)
    # params = {"client_id":     SPOTIPY_CLIENT_ID,
    #          "response_type": "code",
    #          # "state":         state,
    #          "redirect_uri":  SPOTIPY_REDIRECT_URI,
    #          "scope":         SCOPE}
    # url = 'http://accounts.spotify.com/authorize?' + urllibparse.urlencode(params)
    # return '<a href="%s">Authenticate with Spotify</a>' % url


@app.route('/spotify_callback/')
def spotify_callback():
    print('callback')
    #state = request.params['state']
    # if not is_valid_state(state):
    # Uh-oh, this request wasn't started by us!
    #    abort(403)
    url = request.url
    CODE = url.split("?code=")[1].split("&")[0]
    app.callback(CODE)


def start_bottle_server(callback):
    print('toast: Starting http server...')
    app.callback = callback
    run(app, host='localhost', port='8080')

    return


class SongView(BoxLayout):
    title = StringProperty()
    artist = StringProperty()


class SongsContent(BoxLayout):
    song_list = ObjectProperty()
    view_class = 'SongView'
    def add_song(self, song_dict):



class ContentSelector(BoxLayout):

    def __init__(self, **kwargs):
        super(ContentSelector, self).__init__(**kwargs)
        self.register_event_type('on_header')

    def on_header(self, *args):
        pass


class Controls(BoxLayout):

    def __init__(self, **kwargs):
        super(Controls, self).__init__(**kwargs)
        self.register_event_type('on_control')

    def on_control(self, *args):
        pass


import threading


class MusicPlayer(BoxLayout):
    controls = ObjectProperty()
    content_selector = ObjectProperty()
    client = StringProperty()
    player = ObjectProperty()
    username = StringProperty()
    server_interface = None
    server = None
    spotify_oauth = None
    authorized = False
    textures = DictProperty()
    threads = []
    back_content_color = ListProperty()

    content = ObjectProperty(None)
    '''
    Container widget for what will be displayed in the Music Player.

    :attr:`content` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.

    .. versionadded:: 0.1
    '''
    _container = ObjectProperty()

    def __init__(self, **kwargs):
        super(MusicPlayer, self).__init__(**kwargs)
        self.back_content_color = mat_rsc.SPOTIFY_SONGS

    def on_client(self, obj, value, *args):
        self.player = {'Spotify': SpotifyClient(), 'Ipod': IpodClient(),
                       'USB': USBClient(), 'HD': HDClient()}[value]
        self.player.username = self.username
        Clock.schedule_once(self.set_bindings)
        if internet_online():
            self.spotify_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                              client_secret=SPOTIPY_CLIENT_SECRET,
                                              redirect_uri=SPOTIPY_REDIRECT_URI,
                                              scope=SCOPE)
            self.server_interface = BottleServerInterface(oauth2=self.spotify_oauth)
            self.server_interface.bind(code=self.push_code)

            self.server = threading.Thread(target=self.start_server)
            self.threads.append(self.server)
            self.server.start()
            print('toast: authorizing....')
            self.prompt_for_user_token()
            while True:
                if self.authorized:
                    break

    def on_content(self, instance, value):
        if self._container:
            self._container.clear_widgets()
            self._container.add_widget(value)

    def on__container(self, instance, value):
        if value is None or self.content is None:
            return
        self._container.clear_widgets()
        self._container.add_widget(self.content)

    def set_bindings(self, *args):
        if internet_online():
            self.server_interface.bind(on_code=self._new_code)
        self.controls.bind(on_control=self.button_pressed)
        self.content_selector.bind(on_header=self.button_pressed)
        # WORKING HERE - set calls to respective function based on button presses on content currently selected

    def button_pressed(self, obj, con_type, *args):
        if len(args) > 0:
            self.back_content_color = args[0]

    def online(self):
        return False

    def _new_code(self, obj, value, *args):
        print('getting token')
        token = self.spotify_oauth.get_access_token(value)
        print(token)
        # WORKING HERE - testing to see if code is returned and token recieved

    def prompt_for_user_token(self, cache_path=None):
        ''' prompts the user to login if necessary and returns
            the user token suitable for use with the spotipy.Spotify
            constructor

            Parameters:

             - username - the Spotify username
             - scope - the desired scope of the request
             - client_id - the client id of your app
             - client_secret - the client secret of your app
             - redirect_uri - the redirect URI of your app
             - cache_path - path to location to save tokens

        '''

        if not SPOTIPY_CLIENT_ID:
            print('''
                You need to set your Spotify API credentials. 

                Get your credentials at     
                    https://developer.spotify.com/my-applications
            ''')
            raise spotipy.SpotifyException(550, -1, 'no credentials set')

        self.spotify_oauth.cache_path = cache_path or ".cache-" + self.username

        # try to get a valid token for this user, from the cache,
        # if not in the cache, the create a new (this will send
        # the user to a web page where they can authorize this app)

        token_info = self.spotify_oauth.get_cached_token()

        if not token_info:
            print('''toast:

                Click 'Okay' to allow app access to Spotify user data.
                Click 'Cancel' to refuse - app will not be able to read
                    user data - including playlist's and music library.

            ''')
            auth_url = self.spotify_oauth.get_authorize_url()
            try:
                import webbrowser
                webbrowser.open(auth_url)
            except:
                print("Please navigate here: %s" % auth_url)

    def start_server(self):
        self.server_interface.bottle_server()

    def push_code(self, obj, value, *args):
        self.player.token = self.spotify_oauth.get_access_token(value)

    def shuffle_songs(self):
        self.player.shuffle_songs()

    def test(self):
        self.player.test()


class TestApp(App):
    title = 'Music Player Test App'
    theme_cls = ThemeManager()
    music_player = ObjectProperty()

    def build(self):
        b = BoxLayout()
        self.music_player = MusicPlayer(username='skxnoy', client='Spotify')
        b.add_widget(self.music_player)
        return b


if __name__ == '__main__':
    TestApp().run()
