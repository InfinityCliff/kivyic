# https://github.com/plamere/spotipy
# https://spotipy.readthedocs.io/en/latest/

# REDIRECT uri
# https://teamtreehouse.com/community/what-is-redirect-uri
# https://stackoverflow.com/questions/25711711/spotipy-authorization-code-flow
# https://www.reddit.com/r/learnpython/comments/5bic6d/anyone_have_experience_using_spotipy_and/

import pickle

from kivyic._secret.app_credentials import SpotipyCreds

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import pprint
import random

from kivy.properties import StringProperty, ObjectProperty, ListProperty, DictProperty
from kivy.uix.widget import Widget


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
            print('no local library File Found. Downloading...')
            return False
        print('local library File Found, loading...')
        self.music_library = music_library
        return True

    def save_local_library(self):
        print('saving local library...')
        filename = open('./rsc/local_library.p', 'wb')
        pickle.dump(self.music_library, filename)
        filename.close()


class MusicPlayer(Widget):
    source = StringProperty()
    player = ObjectProperty()

    def on_source(self, obj, value, *args):
        self.player = {'Spotify': SpotifyClient(), 'Ipod': IpodClient(),
                       'USB': USBClient(), 'HD': HDClient()}[value]

    def shuffle_songs(self):
        self.player.shuffle_songs()


# TODO - Widget is not the right thing here, but used so username can be passed
class SpotifyClient(Library):

    client_credentials_manager = None
    sp = None
    username = StringProperty()
    client_id = StringProperty()
    client_secret = StringProperty()
    redirect_uri = StringProperty()
    #library = None

    def __init__(self, **kwargs):
        super(SpotifyClient, self).__init__(**kwargs)
        self.client_id = SpotipyCreds.SPOTIPY_CLIENT_ID
        self.client_secret = SpotipyCreds.SPOTIPY_CLIENT_SECRET
        self.redirect_uri = SpotipyCreds.SPOTIPY_REDIRECT_URI
        self.auth()
        #self.library = Library()
        if not self.library_loaded:
            self.download_library()

    def auth(self):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def show_user(self):
        user = self.sp.user(self.username)
        pprint.pprint(user)

    def get_token(self, scope=None):
        if scope:
            token = util.prompt_for_user_token(self.username, scope=scope,
                                               client_id=self.client_id,
                                               client_secret=self.client_secret,)
                                               #redirect_uri=self.redirect_uri)
        else:
            token = None
        return token

    def download_library(self):
        library = {}
        scope = 'user-library-read'
        token = self.get_token(scope)
        sp = spotipy.Spotify(auth=token)
        if token:
            print('downloading library...')
            self.album_list = []
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
            print("Can't get token for", self.username)
        self.add_music_library(library)


class IpodClient:
    pass


class USBClient:
    pass


class HDClient:
    pass

if __name__ == '__main__':
    client = SpotifyClient(username='skxnoy')
    client.shuffle_songs()


# https://github.com/jupyter/notebook/issues/2836

