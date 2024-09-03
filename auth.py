from flask import Flask, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
import streamlit as st


client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]

st.write(f"client_id: {client_id}")
st.write(f"client_secret: {client_secret}")

app = Flask(__name__)
app.secret_key = 'random_secret_key'
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=client_id,
    client_secret=client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=None,
    client_kwargs={'scope': 'openid profile email'},
)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('index'))


@app.route('/oauth2callback')
def authorized():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    return 'Logged in as: ' + user_info['email']


@app.route('/profile')
def profile():
    user_info = google.get('userinfo').json()
    return f'Logged in as: {user_info["email"]}'


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
