from bottle import route, run, request
import spotipy
from spotipy import oauth2
from spotipy import util

from kivyic._secret.app_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID,
                               SPOTIPY_CLIENT_SECRET,
                               SPOTIPY_REDIRECT_URI,
                               scope=SCOPE, cache_path=CACHE)
# Does token exist
token = sp_oauth.get_cached_token()


@route('/')
def auth():
    print('auth')
    url = sp_oauth.get_authorize_url()
    print('url: ', url)
    print('*** STARTING 1 ***')
    token = util.prompt_for_user_token('skxnoy', scope=SCOPE,
                                       client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=SPOTIPY_REDIRECT_URI)
    print('token:', token)



if token:
    print('cached token exists:')
    print(token)
else:
    print('no cached token')
    print('*** STARTING 1 ***')
    auth()
    url = request.url
    code = sp_oauth.parse_response_code(url)
    print('code:', code)
    run(host='localhost', port='8080')


