import base64
import os
import os.path
import simplejson as json
import urllib
import urllib2
import time

from flask import Flask, session, request, redirect, render_template
from flaskext.sqlalchemy import SQLAlchemy

from models import app, db

FBAPI_APP_ID = os.environ.get('FACEBOOK_APP_ID')
Flask.secret_key = 'pm1yfQmmbZUiAP8Ll/JG9XJWNiebOVyyz1T0nlVED3uE4lpv'

def oauth_login_url(next_url=None):
    fb_login_uri = ("https://www.facebook.com/dialog/oauth"
                    "?client_id=%s&redirect_uri=%s" %
                    (app.config['FBAPI_APP_ID'],
                     next_url if next_url else get_home()))

    if app.config['FBAPI_SCOPE']:
        fb_login_uri += "&scope=%s" % ",".join(app.config['FBAPI_SCOPE'])
    return fb_login_uri

class ensure_fb_auth:
    def __init__(self, func):
        '''
        Ensure that that user has a valid Facebook presence. If not, redirect
        the user to the Facebook authentication page, while attempting to have
        them link back to the current page.
        '''
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
    def __call__(self, *args):
        access_token,expires = None, None
        if 'access_token' in session and 'expires' in session:
            access_token = session['access_token']
            expires = session['expires']
        elif request.args.get('code', None):
            auth_response = fbapi_auth(request.args.get('code'))
            session['access_token'], session['expires'] = \
                access_token, expires = auth_response

        if not access_token or expires <= time.time():
            print 'QWERTYUIOP'
            return redirect(oauth_login_url(
                    get_permalink_path(request.path)))
        else:
            print 'asdfghjkl'
            return self.func(*args)

def get_permalink_path(path):
    '''
    Deal with the mixed environment of AJAXified partials and full paths.
    '''
    if 'ajax' in path or 'task' in path:
        path = get_fully_qualified_path('/permalink' + path)
    else:
        path = get_fully_qualified_path(path)
    if not path:
        path = get_fully_qualified_path('/')
    return path

def simple_dict_serialisation(params):
    return "&".join(map(lambda k: "%s=%s" % (k, params[k]), params.keys()))

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip('=')

def fbapi_get_string(path, domain=u'graph', params=None, access_token=None,
                     encode_func=urllib.urlencode):
    """Make an API call"""
    if not params:
        params = {}
    params[u'method'] = u'GET'
    if access_token:
        params[u'access_token'] = access_token

    for k, v in params.iteritems():
        if hasattr(v, 'encode'):
            params[k] = v.encode('utf-8')

    url = u'https://' + domain + u'.facebook.com' + path
    params_encoded = encode_func(params)
    url = url + params_encoded
    result = urllib2.urlopen(url).read()

    return result

def fbapi_auth(code):
    params = {'client_id': app.config['FBAPI_APP_ID'],
              'redirect_uri': get_home(),
              'client_secret': app.config['FBAPI_APP_SECRET'],
              'code': code}

    result = fbapi_get_string(path=u"/oauth/access_token?", params=params,
                              encode_func=simple_dict_serialisation)
    pairs = result.split("&", 1)
    result_dict = {}
    for pair in pairs:
        (key, value) = pair.split("=")
        result_dict[key] = value
    return (result_dict["access_token"], result_dict["expires"])

def fbapi_get_application_access_token(id):
    token = fbapi_get_string(
        path=u"/oauth/access_token",
        params=dict(grant_type=u'client_credentials', client_id=id,
                    client_secret=app.config['FB_APP_SECRET']),
        domain=u'graph')

    token = token.split('=')[-1]
    if not str(id) in token:
        print 'Token mismatch: %s not in %s' % (id, token)
    return token

def fql(fql, token, args=None):
    if not args:
        args = {}

    args["query"], args["format"], args["access_token"] = fql, "json", token
    return json.loads(
        urllib2.urlopen("https://api.facebook.com/method/fql.query?" +
                        urllib.urlencode(args)).read())

def fb_call(call, args=None):
    return json.loads(urllib2.urlopen("https://graph.facebook.com/" + call +
                                      '?' + urllib.urlencode(args)).read())

app.config.from_object(__name__)
app.config.from_object('conf.Config')

def get_home():
    return get_fully_qualified_path('/')

def get_fully_qualified_path(short_path):
    if request.host.find('localhost') != -1:
        return 'http://' + request.host + short_path
    else:
        return 'https://' + request.host + short_path


@app.route('/close/', methods=['GET', 'POST'])
def close():
    return render_template('close.html')

@app.route('/', methods=['GET', 'POST'])
@ensure_fb_auth
def root(content=None):
    access_token = session['access_token']
    if access_token:
        if not content:
            content = home()
        me = fb_call('me', args={'access_token': access_token})
        app_friends = fql(
            "SELECT uid, name, is_app_user, pic_square "
            "FROM user "
            "WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) AND "
            "  is_app_user = 1", access_token)

        return render_template(
            'index.html',
            app=app,
            me=me,
            appId=FBAPI_APP_ID,
            token=access_token,
            content=content)
    else:
        print oauth_login_url(next_url=get_home())
        return redirect(oauth_login_url(next_url=get_home()))

@app.route('/task/create/', methods=['GET', 'POST'])
@ensure_fb_auth
def create_task():
    return render_template('create_task.html')

@app.route('/task/<id>/', methods=['GET'])
@ensure_fb_auth
def view_task():
    print request.path
    return render_template('view_task.html')

@app.route('/ajax/home/', methods=['GET'])
@ensure_fb_auth
def home():
    access_token = session['access_token']
    me = fb_call('me', args={'access_token': access_token})
    app = fb_call(FBAPI_APP_ID, args={'access_token': access_token})
    likes = fb_call('me/likes',
                    args={'access_token': access_token, 'limit': 4})
    friends = fb_call('me/friends',
                      args={'access_token': access_token, 'limit': 4})
    photos = fb_call('me/photos',
                     args={'access_token': access_token, 'limit': 16})

    return render_template('home.html', me=me, app=app, likes=likes,
                           friends=friends, photos=photos)

@app.route('/permalink/<path:ajax_path>')
def permalink(ajax_path):
    return root(render_template('permalink_load.html', ajax_path=ajax_path))

@app.route('/experiment/piglatin/', methods=['GET', 'POST'])
def pig():
    def piglatin(inp):
        if len(inp) < 3:
            return inp+"ay"
        else:
            return inp[1:]+inp[0]+"ay"
    inp = request.args.get('inp', None)
    return render_template('experiment.html', out=piglatin(inp));


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    if app.config.get('FBAPI_APP_ID') and app.config.get('FBAPI_APP_SECRET'):
        app.run(host='0.0.0.0', port=port)
    else:
        print 'Cannot start application without Facebook App Id and Secret set'
