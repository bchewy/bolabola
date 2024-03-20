from flask import Flask, redirect, session, url_for, render_template
import pika
import requests
import os
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=os.environ.get('AUTH0_CLIENT_ID'),
    client_secret=os.environ.get('AUTH0_CLIENT_SECRET'),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

@app.route('/')
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()
    # store the user information in the session
    session["user"] = token

    # get the user info from the token
    user_info = oauth.auth0.parse_id_token(token)
    
    # call the user service to check if user exists and create user in the database
    response = requests.post("http://kong:8000/api/v1/user", json=user_info)
    if response.code != 201 or response.code != 200:
        return "Failed to create user", 500

    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + os.environ.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9010)