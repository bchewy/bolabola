from flask import Flask, redirect, session, url_for, render_template
import pika
import http.client
import os
import json
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

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
    conn = http.client.HTTPConnection("kong:8000")
    headers = {
        "Content-Type": "application/json",
    }
    payload = json.dumps({
        "user_id": user_info["sub"],
        "email": user_info["email"],
        "name": user_info["name"],
    })
    conn.request("POST", "/api/v1/user/check-create", payload, headers)

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
    app.run(debug=True)