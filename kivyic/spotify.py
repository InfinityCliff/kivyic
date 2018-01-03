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

from kivy.properties import StringProperty
from kivy.uix.widget import Widget

def auth_callback():
    print('auth callback success')

# TODO - Widget is not the right thing here, but used so username can be passed
class SpotifyClient(Widget):

    client_credentials_manager = None
    sp = None
    username = StringProperty()
    client_id = StringProperty()
    client_secret = StringProperty()
    redirect_uri = StringProperty()
    library = {}

    def __init__(self, **kwargs):
        super(SpotifyClient, self).__init__(**kwargs)
        self.client_id = SpotipyCreds.SPOTIPY_CLIENT_ID
        self.client_secret = SpotipyCreds.SPOTIPY_CLIENT_SECRET
        self.redirect_uri = SpotipyCreds.SPOTIPY_REDIRECT_URI
        self.auth()
        self.load_local_library()

    def auth(self):
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id,
                                                                   client_secret=self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def load_local_library(self):
        try:
            self.library = pickle.load(open('/rsc/local_library.p', 'r'))
        except FileNotFoundError:
            self.refresh_library()
            self.save_local_library()

    def save_local_library(self):
        pickle.dump(self.library, open('/rsc/local_library.p', 'w'))

    def test(self):
        scope = 'user-library-read'
        token = util.prompt_for_user_token(self.username, scope=scope,
                                           client_id=self.client_id, client_secret=self.client_secret)
        if token:
            print('token')
            sp = spotipy.Spotify(auth=token, client_credentials_manager=self.client_credentials_manager)
            results = sp.current_user_saved_tracks()
            for item in results['items']:
                track = item['track']
                print(track['name'] + ' - ' + track['artists'][0]['name'])
        else:
            print("Can't get token for", self.username)

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

    def get_artists(self):
        scope = 'user-library-read'
        token = self.get_token(scope)
        sp = spotipy.Spotify(auth=token)
        if token:
            results = sp.artists()
            print(results.keys())
            #for item in results['items']:
            #    track = item['track']
            #    print(track['name'] + ' - ' + track['artists'][0]['name'])
        else:
            print("Can't get token for", self.username)

    def refresh_library(self):
        library = {}
        scope = 'user-library-read'
        token = self.get_token(scope)
        sp = spotipy.Spotify(auth=token)
        if token:
            results = sp.current_user_saved_tracks()
            while True:
                for item in results['items']:
                    #print(item['track'])
                    track = item['track']

                    #print(track['name'] + ' - ' + track['artists'][0]['name'])
                    library[item['track']['id']] = {'song': track['name'], 'artist': track['artists'][0]['name'], 'album':track['album']['name']}
                if results['next']:
                    results = sp._get(results['next'])
                else:
                    break
        else:
            print("Can't get token for", self.username)
        self.library = library

if __name__ == '__main__':
    client = SpotifyClient(username='skxnoy')
    lib = client.get_library()
    print(lib)



# https://github.com/jupyter/notebook/issues/2836