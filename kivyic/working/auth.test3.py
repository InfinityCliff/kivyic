# https://github.com/reddit/reddit/wiki/OAuth2-Python-Example

from bottle import route, run, request, abort, Bottle
import spotipy
from spotipy import oauth2
from spotipy import util

import six
import six.moves.urllib.parse as urllibparse
import base64
from kivyic._secret.app_credentials import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

app = Bottle()


@app.route('/')
def homepage():
    print('homepage')
    text = '<a href="%s">Authenticate with Spotify</a>'
    return text % make_authorization_url()


def make_authorization_url():
    print('make_authorization_url')
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id":     SPOTIPY_CLIENT_ID,
              "response_type": "code",
              "state":         state,
              "redirect_uri":  SPOTIPY_REDIRECT_URI,
              "scope":         SCOPE}
    import urllib
    url = 'http://accounts.spotify.com/authorize?' + urllibparse.urlencode(params)
    return url


def save_created_state(state):
    pass


def is_valid_state(state):
    return True


@app.route('/spotify_callback/')
def spotify_callback():
    print('spotify_callback')
    state = request.params['state']
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    #code = request.args.get('code')
    code = request.params['code']
    print(code)
    #code = sp_oauth.parse_response_code(response)
    # We'll change this next line in just a moment
    return "got a code! %s" % code

def get_token(code):
    print('get_token')
    client_auth = request.auth.HTTPBasicAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    auth_header = base64.b64encode(six.text_type(SPOTIPY_CLIENT_ID + ':' + SPOTIPY_CLIENT_SECRET).encode('ascii'))
    auth_header = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": SPOTIPY_REDIRECT_URI}
    response = request.post('https://accounts.spotify.com/api/token',
                            data=post_data,
                            headers=auth_header,
                            auth=client_auth,
                            verify=True)
    token_json = response.json()
    return token_json["access_token"]

if __name__ == '__main__':
    run(app, host='localhost', port='8080')
