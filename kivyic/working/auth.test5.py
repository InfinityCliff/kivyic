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
                                 #cache_path=CACHE,
                                 )
    token = StringProperty()
    track_headers = ['id', 'name', 'album_id', 'artist_id']
    track_list = pd.DataFrame(columns=track_headers)
    album_headers = ['id', 'name', 'artist_id']
    album_list = pd.DataFrame(columns=album_headers)
    artist_list = pd.DataFrame(columns=['id', 'name'])

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.start_server()
        self.start_auth()
        q.join()
        token = self.spotify_oauth.get_access_token(q.get())

        self.sp = spotipy.Spotify(auth=token['access_token'])

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

# working here to work out how to download/save album trak info and if can save tracks, may not need to withspotify on pi
    def saved_albums(self):
        album_art = "./album_art/"
        sa = self.sp.current_user_saved_albums()

        while True:
            for item in sa['items']:
                album = item['album']
                self.album_list.loc[len(self.album_list)] = [album['id'], album['name'], album['artists'][0]['name']]

                name = album['id'] + '.jpeg'
                if not os.path.isfile(album_art + name):
                    url = album['images'][1]['url']
                    urllib.request.urlretrieve(url, album_art + name)
            if sa['next']:
                sa = self.sp._get(sa['next'])
            else:
                break

        self.album_list.set_index('id', inplace=True)
        print(self.album_list.head())

    def saved_tracks(self):
        st = self.sp.current_user_saved_tracks()
        print(st.keys())
        for item in st['items']:
            print(item['track'].keys())
            print()
            print(item['track']['name'])
            print(item['track']['album']['name'])
            print(item['track']['artists'][0]['name'])
            print()
            print(item['track']['album']['album_art'][1]['url'])
            print('---------------------------------------------------------')


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

