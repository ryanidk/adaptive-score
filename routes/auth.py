"""
Authentication Routes
ICS3U-01
Ryan
These routes handle authentication through Google OAuth2 for the program.
The Google auth system source: https://realpython.com/flask-google-login/
Apr 20, 2026
"""

# Necessary imports
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import os
import json
from dotenv import load_dotenv
from models.user import User, Skill


# Load dotenv, for use in constants. load_dotenv puts it in os.environ
load_dotenv()

# Configuration constants for authentication - based on environment variables
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# Set up blueprint
auth_blueprint = Blueprint('auth', __name__, template_folder='../templates')

# Set up the OAuth2 client which will be used for authentication.
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Utility functions
def get_google_provider_cfg():
    """
    Returns the json for the Google OAuth2 config. This was taken from the Real Python tutorial.

    Returns:
        - (dict) The OpenID configuration as a dictionary
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()



# Routes
@auth_blueprint.route("/login")
def login():
    """
    Handles the login route, where the user can log in with their Google account to then be redirected back to the home page.

    Returns:
        - (redirect): Redirects to the Google authorization endpoint
    """

    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth_blueprint.route("/login/callback")
def callback():
    """
    Handles the callback route. This is executed when the user authenticates with Google successfully.
    We also authenticate the request to make sure they're not spoofing an email.

    Returns:
        - (redirect): Redirects to the index page
    """

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Initialize skills if it does not exist
    if not Skill.get_skills(unique_id):
        Skill.create_skills(unique_id)

    # Begin user session by logging the user in
    login_user(user, remember=True)

    # Send user back to homepage
    return redirect(url_for("index"))




@auth_blueprint.route("/logout")
@login_required
def logout():
    """
    Handles the logout route, where the user can immediately log out.
    This redirects to the index page, but as seen in the main routes, there is a different page the user sees
    whether they are logged in or not.

    Returns:
        - (redirect): Redirects to the unauthenticated index page.
    """

    logout_user()
    return redirect(url_for("index"))