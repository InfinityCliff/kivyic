# -*- coding: utf-8 -*-
import pickle

from kivyic._secret.app_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from kivyic.network import internet_online
from kivyic import material_resources as mat_rsc
from kivyic.button import ICIconButton
from kivyic.scrollbar import AlphaScrollItem

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pprint
import random
import os.path
import pandas as pd

import threading
from queue import Queue

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivy import Logger

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty, ListProperty, DictProperty, NumericProperty, BooleanProperty

from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton

from kivymd.theming import ThemeManager
from uuid import uuid4

from bottle import route, run, request, abort, Bottle
import webbrowser
import urllib.request


# -------------------------------------------------------------------------------
# BOUND METHODS
# https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance
# -------------------------------------------------------------------------------
def current_user_playback(self):
    """ Get current user playback information
        required scope -- user-read-playback-state

        https://developer.spotify.com/web-api/get-information-about-the-users-current-playback/
    """
    return self._get("me/player")


spotipy.Spotify.current_user_playback = current_user_playback

# -------------------------------------------------------------------------------
# GOOD EXPLANATION ON THREADING AND QUEUES
# https://www.slideshare.net/dabeaz/an-introduction-to-python-concurrency
# -------------------------------------------------------------------------------
threads = []
q = Queue(10)

RSC_PATH = './rsc/'
SPOTIFY_RSC_PATH = RSC_PATH + '.spotify-client-kivyic/'

app = Bottle()
# -------------------------------------------------------------------------------
# Bottle Example:
# https://stackoverflow.com/questions/25711711/spotipy-authorization-code-flow

# Flask Example
# https://gist.github.com/kemitche/9749639
# -------------------------------------------------------------------------------

@app.route('/spotify_callback/')
def spotify_callback():
    """
    stores authorization 'code' in queue and reports that it has been recieved
    :return: None
    """
    # TODO add state check in to callback
    #state = request.params['state']
    # if not is_valid_state(state):
    # Uh-oh, this request wasn't started by us!
    #    abort(403)
    url = request.url
    code = url.split("?code=")[1].split("&")[0]
    q.put(code)
    q.task_done()


def start_server():
    """
    start local server to listen on port 8080
    :return: None
    """
    run(app, host='localhost', port='8080')


Builder.load_file('music_player.kv')


class MPIconButton(ICIconButton):
    icon = StringProperty('checkbox-blank-circle')


class MPBaseButton(ToggleButton):
    pass


from spotipy import oauth2
import six
import six.moves.urllib.parse as urllibparse
import base64


class SongView(ButtonBehavior, AlphaScrollItem):
    title = StringProperty()
    artist = StringProperty()
    album = StringProperty()


class SongsScreen(BoxLayout):
    song_list = ObjectProperty()
    view_class = SongView
    content = ListProperty()
    content_dict = DictProperty()

    def on_content(self, *args):
        for item in self.content:
            item['view_class'] = self.view_class
        self.content_dict = {'sort_key': 'title', 'attributes': self.content}

        self.song_list.content = self.content_dict


class AlbumView(ButtonBehavior, AlphaScrollItem):
    title = StringProperty()
    artist = StringProperty()
    cover_art = StringProperty()

    def __init__(self, **kwargs):
        super(AlbumView, self).__init__(**kwargs)
        self.register_event_type('on_play_album')

    def on_play_album(self, *args):
        pass


class AlbumsScreen(BoxLayout):
    album_list = ObjectProperty()
    view_class = AlbumView
    content = ListProperty()
    content_dict = DictProperty()

    def on_content(self, *args):
        for item in self.content:
            item['view_class'] = self.view_class
        self.content_dict = {'sort_key': 'title', 'attributes': self.content}
        self.album_list.content = self.content_dict

    def add_album(self, album_dict):
        pass


class ArtistView(ButtonBehavior, AlphaScrollItem):
    artist = StringProperty()
    song_count = NumericProperty()
    album_count = NumericProperty()


class ArtistsScreen(BoxLayout):
    artist_list = ObjectProperty()
    view_class = ArtistView
    content = ListProperty()
    content_dict = DictProperty()

    def on_content(self, *args):
        for item in self.content:
            item['view_class'] = self.view_class
        self.content_dict = {'sort_key': 'artist', 'attributes': self.content}
        self.artist_list.content = self.content_dict


class PlayListView(ButtonBehavior, AlphaScrollItem):
    play_list_name = StringProperty
    song_count = NumericProperty()
    play_list_art = StringProperty()


class PlayListsScreen(BoxLayout):
    play_list = ObjectProperty()
    view_class = PlayListView
    content = ListProperty()
    content_dict = DictProperty()

    def on_content(self, *args):
        for item in self.content:
            item['view_class'] = self.view_class
        self.content_dict = {'sort_key': 'play_list_name', 'attributes': self.content}
        self.play_list.content = self.content_dict


class DailyMixScreen(BoxLayout):
    pass


class ContentSelector(BoxLayout):

    def __init__(self, **kwargs):
        super(ContentSelector, self).__init__(**kwargs)
        self.register_event_type('on_header_control')

    def on_header_control(self, *args):
        pass


class Controls(BoxLayout):
    controls_state = DictProperty()
    repeat_color = ListProperty()
    repeat_state = StringProperty()
    shuffle_color = ListProperty()
    shuffle_state = BooleanProperty()

    play_pause_icon = StringProperty('play-circle-outline')
    is_playing = BooleanProperty()

    def __init__(self, **kwargs):
        super(Controls, self).__init__(**kwargs)
        self.register_event_type('on_control')
        #self.shuffle_color = [1,0,0,1]
        print("sc", self.shuffle_color)

    def next_repeat_state(self):
# working here to create multistate button to sycle between repeat states
    def on_control(self, *args):
        pass

    #def on_repeat_color(self, *args):
    #    pass

    def on_controls_state(self, *args):
        print('on_controls_state')
        print(self.controls_state['shuffle_state'])
        self.repeat_state = self.controls_state['repeat_state']
        #self.shuffle_state = self.controls_state['shuffle_state']
        self.on_shuffle_state(self, self.controls_state['shuffle_state'])
        self.is_playing = self.controls_state['is_playing']
        print('::', self.shuffle_color)

    def on_is_playing(self, obj, is_playing, *args):
        self.play_pause_icon = {False: 'play-circle-outline',
                                True: 'pause-circle-outline'}[is_playing]

    def on_repeat_state(self, obj, value, *args):
        self.repeat_color = {'off': mat_rsc.SPOTIFY_LT_GREY,
                             'track': mat_rsc.SPOTIFY_BRT_GREEN,
                             'context': [1, 0, 0, 1],
                             }[value]

    def on_shuffle_state(self, obj, value, *args):
        print(':::', value)
        self.shuffle_color = {False: mat_rsc.SPOTIFY_LT_GREY,
                              True: mat_rsc.SPOTIFY_BRT_GREEN,
                              }[value]


class SecondaryControls(FloatLayout):

    def __init__(self, **kwargs):
        super(SecondaryControls, self).__init__(**kwargs)
        self.register_event_type('on_secondary_control')

    def on_secondary_control(self, *args):
        pass


class ClientBase(Widget):
    username = ''

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username')
        super(ClientBase, self).__init__(**kwargs)

    @staticmethod
    def start_server():
        """
        creates thread to start server an initiates the thread
        :return: None
        """
        server = threading.Thread(target=start_server)
        server.setDaemon(True)
        threads.append(server)
        server.start()
        Logger.info("Bottle: Server Started: {}".format(server.name))

    def get_authorize_code(self, auth_url):
        """
        opens browser at auth_url and request access code, code is returned to:
            @app.route('/spotify_callback/')
            def spotify_callback():
                ...
        :param auth_url: str: path to service authorization code
        :return: None
        """
        state = str(uuid4())
        self.save_created_state(state)
        webbrowser.open(auth_url)

    def save_created_state(self, state):
        pass

    def is_valid_state(state):
        return True

    def test(self):
        print('*** running test, Library ***')


# -------------------------------------------------------------------------------
# SPOTIFY ON RASPBERRY PI LINKS
# https://eltechs.com/run-spotify-on-raspberry-pi/
# https://docs.mopidy.com/en/latest/
# https://raspberrypi.stackexchange.com/questions/4473/how-to-run-spotify-on-raspberry-pi
# https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=62537
# -------------------------------------------------------------------------------
class SpotifyClient(ClientBase):

    SCOPE = 'user-library-read user-modify-playback-state playlist-read-private user-read-playback-state'
    track_list = None
    album_list = None
    artist_list = None
    play_list = None
    current_state = DictProperty()

    def __init__(self, **kwargs):
        super(SpotifyClient, self).__init__(**kwargs)
        self.register_event_type('on_change_state')
        #self.register_event_type('on_shuffle_state')

        self.CACHE = SPOTIFY_RSC_PATH + ".cache-" +  self.username
        self.spotify_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                          client_secret=SPOTIPY_CLIENT_SECRET,
                                          redirect_uri=SPOTIPY_REDIRECT_URI,
                                          scope=self.SCOPE,
                                          cache_path=self.CACHE,
                                          )

        token = self.spotify_oauth.get_cached_token()
        if not token:
            print('token not found')
            self.start_server()
            self.get_authorize_code(auth_url=self.spotify_oauth.get_authorize_url())  # TODO when set up simply add --> state=state))
            q.join()
            token = self.spotify_oauth.get_access_token(q.get())
        else:
            print('token found')

        self.sp = spotipy.Spotify(auth=token['access_token'])
#        self.update_current_state()
        self.load_data_pickle()

    def update_current_state(self, *args):
        self.current_state = self.sp.current_user_playback()

    def on_current_state(self, *args):
        self.dispatch('on_change_state', self.current_state)

    def on_change_state(self, *args):
        pass

    def control(self, control_type=None, state=None):
        from functools import partial

        {'shuffle': partial(self.sp.shuffle, state),
                   'previous': self.sp.previous_track,
                   'play': self.sp.start_playback,
                   'pause': self.sp.pause_playback,
                   'next': self.sp.next_track,
                   'repeat': self.sp.repeat
                   }[control_type]()
        #control()
        self.update_current_state()

    def load_data_pickle(self):
        data_filename = SPOTIFY_RSC_PATH + '.spotify-albums-' + self.username + '.pkl'
        if os.path.isfile(data_filename):
            self.album_list = pd.read_pickle(data_filename)
        else:
            self.download_albums()

        data_filename = SPOTIFY_RSC_PATH + '.spotify-tracks-' + self.username + '.pkl'
        if os.path.isfile(data_filename):
            self.track_list = pd.read_pickle(data_filename)
        else:
            self.download_tracks()

        data_filename = SPOTIFY_RSC_PATH + '.spotify-artists-' + self.username + '.pkl'
        if os.path.isfile(data_filename):
            self.artist_list = pd.read_pickle(data_filename)
        else:
            self.compile_artists()

        data_filename = SPOTIFY_RSC_PATH + '.spotify-play_lists-' + self.username + '.pkl'
        if os.path.isfile(data_filename):
            self.play_list = pd.read_pickle(data_filename)
        else:
            self.download_play_lists()

    def save_data_pickle(self, list_name, data_list):
        data_filename = SPOTIFY_RSC_PATH + '.spotify-' + list_name + '-' + self.username + '.pkl'
        data_list.to_pickle(data_filename)

    def download_albums(self):
        print('toast: Downloading Album list for user: ', self.username)
        album_art = SPOTIFY_RSC_PATH + "album_art/"
        sa = self.sp.current_user_saved_albums()
        self.album_list = None

        columns = ['album_id', 'title', 'artist_id', 'artist', 'cover_art']
        self.album_list = pd.DataFrame(columns=columns)
        while True:
            for item in sa['items']:
                album = item['album']
                self.album_list.loc[len(self.album_list)] = [album['id'], album['name'],
                                                             album['artists'][0]['id'],
                                                             album['artists'][0]['name'],
                                                             album_art + album['id'] + '.jpeg',
                                                             ]
                name = album['id'] + '.jpeg'
                if not os.path.isfile(album_art + name):
                    url = album['images'][1]['url']
                    urllib.request.urlretrieve(url, album_art + name)
            if sa['next']:
                sa = self.sp._get(sa['next'])
            else:
                break

        self.save_data_pickle('albums', self.album_list)

    def download_tracks(self):
        print('toast: Downloading Track list for user: ', self.username)
        st = self.sp.current_user_saved_tracks()
        self.track_list = None
        columns = ['track_id', 'title', 'album', 'artist', 'artist_id']
        self.track_list = pd.DataFrame(columns=columns)
        while True:
            for item in st['items']:
                track = item['track']
                self.track_list.loc[len(self.track_list)] = [track['id'], track['name'],
                                                             track['album']['name'],
                                                             track['artists'][0]['name'],
                                                             track['artists'][0]['id'],
                                                             ]

            if st['next']:
                st = self.sp._get(st['next'])
            else:
                break
        self.save_data_pickle('tracks', self.track_list)

    def compile_artists(self):
        print('toast: Compiling Track list for user: ', self.username)
        self.artist_list = self.album_list[['artist_id', 'artist']].copy()
        self.artist_list.drop_duplicates(subset='artist_id', inplace=True)
        self.artist_list['album_count'] = self.artist_list.artist_id.apply(
                lambda x: len(self.album_list.loc[self.album_list['artist_id'] == x]))
        self.artist_list['song_count'] = self.artist_list.artist_id.apply(
                lambda x: len(self.track_list.loc[self.track_list['artist_id'] == x]))

        self.save_data_pickle('artists', self.artist_list)

    def download_play_lists(self):
        print('toast: Downloading Playlist for user: ', self.username)
        pl = self.sp.current_user_playlists()
        self.play_list = None
        columns = ['play_list_id', 'play_list_name']
        self.play_list = pd.DataFrame(columns=columns)
        while True:
            for playlist in pl['items']:
                self.play_list.loc[len(self.play_list)] = [playlist['id'],
                                                           playlist['name'],
                                                           ]
            if pl['next']:
                pl = self.pl._get(pl['next'])
            else:
                break
        self.save_data_pickle('play_lists', self.play_list)


    def test(self):
        super().test()


class IpodClient:
    pass


class USBClient:
    pass


class HDClient:
    pass


class MusicPlayer(BoxLayout):
    controls = ObjectProperty()
    secondary_controls = ObjectProperty()
    content_selector = ObjectProperty()
    client = StringProperty()
    player = ObjectProperty()
    username = StringProperty()
    server_interface = None
    spotify_oauth = None
    back_content_color = ListProperty()

    screen_manager = ScreenManager()
    '''
    Manager screen shown when content button is selected in the Music Player.

    :attr:`content` is an :class:`~kivy.uix.screenmanager.ScreenManager` and
    defaults to ''.

    .. versionadded:: 0.1
    '''

    def __init__(self, **kwargs):
        self.username = kwargs.pop('username')
        super(MusicPlayer, self).__init__(**kwargs)
        self.back_content_color = mat_rsc.SPOTIFY_SONGS

    def on_client(self, obj, value, *args):
        player_cls = {'Spotify': SpotifyClient,
                      'Ipod': IpodClient,
                      'USB': USBClient,
                      'HD': HDClient}[value]
        print(':', self.username)
        self.player = player_cls(username=self.username)

        Clock.schedule_once(self.set_bindings)
        Clock.schedule_once(self.player.update_current_state)

    def set_bindings(self, *args):
        self.controls.bind(on_control=self.control)
        self.content_selector.bind(on_header_control=self.header_control)
        self.secondary_controls.bind(on_secondary_control=self.secondary_control)
        self.player.bind(on_change_state=self.change_state)

    def change_state(self, obj, value, *args):
        self.controls.controls_state = value

    def header_control(self, obj, con_type, color, *args):
        self.back_content_color = color
        self.screen_manager.current = con_type

    def secondary_control(self, obj, value, *args):
        if value == 'Shuffle Play':
            self.player.shuffle(self.screen_manager.current),
        if value == 'download':
            print(value, ':', self.screen_manager.current),
        if value == 'de-download':
            print(value, ':', self.screen_manager.current)

    def control(self, obj, con_type, state, *args):
        print(con_type)
        self.player.control(con_type, state)

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
