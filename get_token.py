from flask import Flask, request, redirect, session, url_for
import requests
import base64
import secrets
import json

secret_k = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_k # Replace with your secret key
# Spotify API credentials
CLIENT_ID = '08e2f604ed0f49baabd07bccf43cc9b3' # Replace with your Spotify client ID
CLIENT_SECRET = 'e4e6da6c6d224792b4b2dc1d86ada943' # Replace with your Spotify client secret
REDIRECT_URI = 'http://localhost:8080/callback' # Replace with your Redirect URI

# Spotify API endpoints
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
# Scopes define the permissions your app needs
SCOPES = ['user-read-recently-played']
@app.route('/')
def home():
# Redirect the user to Spotify's authorization page
    auth_query_parameters = {
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'client_id': CLIENT_ID
    }
    auth_url = f"{SPOTIFY_AUTH_URL}/?{requests.compat.urlencode(auth_query_parameters)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Handle the callback from Spotify
    code = request.args.get('code')
    # Exchange the authorization code for an access token
    token_data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
    }
    headers = {
    'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    response = requests.post(SPOTIFY_TOKEN_URL, data=token_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        # Store the access token securely (e.g., in a database)
        session['access_token'] = access_token
        # File path where you want to save the access token
        file_path = "access_token.txt"
# Write the access token to the text file
        with open(file_path, "w") as file:
            file.write(access_token)
        print(f"Access token saved to {file_path}")
        return "Access token obtained successfully and stored."
    else:
        return "Failed to obtain an access token."
if __name__ == '__main__':
    app.run(debug=True, port=8080)