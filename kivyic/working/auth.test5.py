from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder
from kivy import Logger
from kivy.properties import StringProperty, ObjectProperty

from kivyic._secret.app_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from bottle import route, run, request, abort, Bottle

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd
from tables import *
import webbrowser
import threading

from uuid import uuid4


from queue import Queue
import urllib.request
import os.path

threads = []
app = Bottle()
q = Queue(10)


@app.route('/spotify_callback/')
def spotify_callback():
    #state = request.params['state']
    # if not is_valid_state(state):
    # Uh-oh, this request wasn't started by us!
    #    abort(403)
    url = request.url
    code = url.split("?code=")[1].split("&")[0]
    q.put(code)
    q.task_done()


def start_server():
    run(app, host='localhost', port='8080')


Builder.load_string("""  
<MainWidget>:
    GridLayout:
        cols: 4
        Button:
            text: 'Authorize'
            on_release: root.start_auth()
        Button:
            text: 'Play'
            on_release: root.sp.start_playback()
        Button:
            text: 'Pause'
            on_release: root.sp.pause_playback()
        Button:
            text: 'next'
            on_release: root.sp.next_track()
        Button:
            text: 'prev'
            on_release: root.sp.previous_track()       
        Button:
            text: 'saved tracks'
            on_release: root.saved_tracks()     
        Button:
            text: 'saved albums'
            on_release: root.saved_albums()              
""")


class MainWidget(BoxLayout):
    username = 'skxnoy'
    SCOPE = 'user-library-read user-modify-playback-state'
    CACHE = ".cache-" + username
    sp = None
    spotify_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                 client_secret=SPOTIPY_CLIENT_SECRET,
                                 redirect_uri=SPOTIPY_REDIRECT_URI,
                                 scope=SCOPE,
                                 cache_path=CACHE,
                                 )
    token = StringProperty()
    track_headers = ['id', 'name', 'album_id', 'artist_id']
    track_list = pd.DataFrame(columns=track_headers)
    album_headers = ['id', 'name', 'artist_id', 'artist_name']
    album_list = pd.DataFrame(columns=album_headers)
    artist_headers = ['id', 'name']
    artist_list = pd.DataFrame(columns=['id', 'name'])

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        token = self.spotify_oauth.get_cached_token()
        if not token:
            print('token not found')
            self.start_server()
            self.start_auth()
            q.join()
            token = self.spotify_oauth.get_access_token(q.get())
        else:
            print('token found')
        self.sp = spotipy.Spotify(auth=token['access_token'])
        print('going to check if data store exists')
        self.load_data_pickle()

    # TODO - make this a thread as it is slow to load
    def load_data_pickle(self):
        for item in ['albums', 'tracks', 'artists']:
            print('does', item, 'data file exist?')
            datafilename = '.spotify-album-' + item + '-' + self.username + '.pkl'
            if os.path.isfile(datafilename):  # yes, load data pickle
                print('yes, load', item, 'pickle')
                {'albums': self.album_list,
                 'tracks': self.track_list,
                 'artists': self.artist_list
                 }[item] = pd.read_pickle(datafilename)
            else:  # no, create data store
                print('no')
                self.download_data_from_internet(item)

    def save_data_pickle(self, data):
        datafilename = '.spotify-album-' + data + '-' + self.username + '.pkl'

        if data == 'albums' and len(self.album_list) > 0:
            self.album_list.to_pickle(datafilename)

        if data == 'tracks' and len(self.track_list) > 0:
            self.track_list.to_pickle(datafilename)

        if data == 'artists' and len(self.artist_list) > 0:
            self.artist_list.to_pickle(datafilename)

    def download_data_from_internet(self, data):
        if type(data) is str:
            data = [data]
        print(data)
        for d in data:
            print(d)
            if d == 'albums':
                self.download_albums()
            if d == 'tracks':
                self.download_tracks()
            if d == 'artists':
                self.compile_artists()

# working here to work out how to download/save album trak info and if can save tracks, may not need to withspotify on pi
    def download_albums(self):
        print('toast: Downloading Album list for user: ', self.username)
        album_art = "./album_art/"
        sa = self.sp.current_user_saved_albums()
        self.album_list = None
        self.album_list = pd.DataFrame(columns=self.album_headers)
        while True:
            for item in sa['items']:
                album = item['album']
                self.album_list.loc[len(self.album_list)] = [album['id'], album['name'],
                                                             album['artists'][0]['id'],
                                                             album['artists'][0]['name']]

                name = album['id'] + '.jpeg'
                if not os.path.isfile(album_art + name):
                    url = album['images'][1]['url']
                    urllib.request.urlretrieve(url, album_art + name)
            if sa['next']:
                sa = self.sp._get(sa['next'])
            else:
                break

        self.album_list.set_index('id', inplace=True)
        self.save_data_pickle('albums')

    def download_tracks(self):
        print('toast: Downloading Track list for user: ', self.username)
        st = self.sp.current_user_saved_tracks()
        self.track_list = None
        self.track_list = pd.DataFrame(columns=self.track_headers)
        while True:
            for item in st['items']:
                track = item['track']
                self.track_list.loc[len(self.track_list)] = [track['id'], track['name'],
                                                             track['album']['id'],
                                                             track['artists'][0]['id']]

            if st['next']:
                st = self.sp._get(st['next'])
            else:
                break
        self.track_list.set_index('id', inplace=True)
        self.save_data_pickle('artists')

    def compile_artists(self):
        print('toast: Compiling artist list for user: ', self.username)
        # working here  - to build artist list from album list, need to remove index from album list
        self.artist_list = self.album_list[['artist_id', 'artist_name']]
        print(self.artist_list.head())

    @staticmethod
    def start_server():
        server = threading.Thread(target=start_server)
        server.setDaemon(True)
        threads.append(server)
        server.start()
        Logger.info("Bottle: Server Started: {}".format(server.name))

    def start_auth(self):
        state = str(uuid4())
        self.save_created_state(state)
        auth_url = self.spotify_oauth.get_authorize_url()  # TODO when set up simply add --> state=state)
        webbrowser.open(auth_url)

    def save_created_state(self, state):
        pass

    def is_valid_state(state):
        return True

class TestApp(App):
    title = 'auth/threading/queue Test App'

    def build(self):
        return MainWidget()


def start_kivy_app():
    TestApp().run()


if __name__ == '__main__':
    t = threading.Thread(target=start_kivy_app)
    threads.append(t)
    t.start()

