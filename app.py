"""
Adaptive Score - Main file
ICS3U-01
Ryan

This file is the main Flask app that will run for Adaptive Score.
Adaptive Score is a platform for students to practice using an adaptive question bank for the SAT test.
Based on the user's proficiency in certain skill domains, the interface will progressively show harder/easier questions.
The app is also able to generate practice tests.
The aim of this app is to enhance student scores.
There are platforms that do this, but they can be expensive ($100+/month) or limited (no adaptiveness)

All required libraries are in requirements.txt.

Due date: May 28, 2026.
Full log can be found in the assignment on Google Classroom and through commit history on Github.
"""

# Built-in python libraries
# Mainly json and sqlite3 to parse, os to get environment variables
import json
import os
import sqlite3

# Third party libraries
# Flask is the web server, flask_login and oauthlib handle auth, requests sends requests, dotenv loads the .env file
from flask import Flask, redirect, request, url_for, render_template, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
from dotenv import load_dotenv

# Internal imports, used for models, database, and blueprints
from db import init_db_command
from models.user import User
from scripts.question_parsing import process_question
from routes.auth import auth_blueprint
from routes.adaptive_practice import adaptive_practice_blueprint

# Load dotenv, for use in constants. load_dotenv puts it in os.environ
load_dotenv()

# Super admin email. There is currently only one and I hardcoded this in .env for ease of use.
SUPER_ADMIN_EMAIL = os.environ.get("SUPER_ADMIN_EMAIL", None)

# Setup flask app
app = Flask(__name__)

# Static key, will log people out if changed
app.secret_key = os.environ.get("SECRET_KEY", None)

# Set up user session management (taken from real python tutorial)
login_manager = LoginManager()
login_manager.init_app(app)

# Set up the database if it has not already been initialized. This is pretty naive.
try:
    init_db_command(app)

    # Also, initialize all the questions
    # Load english and math questions
    with open("scripts/question_scraping/english.json", "r") as e:
        english_bank = json.load(e)

    with open("scripts/question_scraping/math.json", "r") as m:
        math_bank = json.load(m)

    # Loop over each question in the bank and add it to the database
    for eng_question in english_bank:
        process_question(app, eng_question, "english")

    for math_question in math_bank:
        process_question(app, math_question, "math")

    print("Finished processing questions")

except sqlite3.OperationalError:
    # Assume it's already been created
    pass


# -------- Utility functions --------
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login helper to retrieve a user from the database.
    Args:
        user_id: The user id that was gotten from the OAuth2 authentication
    Returns:
        User (object): The user object from the user ID.
    """
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """
    Handles the 403 unauthorized page, essentially if the user is trying to access a page without being logged in.
    Returns:
        str: Unauthorized string
        response_code (int): 403, the web response code for unauthorized.
    """
    return "Unauthorized", 403


# Main route
@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", name=current_user.name, email=current_user.email)
    else:
        return render_template('login.html')


# BLUEPRINT REGISTRATION
app.register_blueprint(auth_blueprint)
app.register_blueprint(adaptive_practice_blueprint)

if __name__ == "__main__":
    # app.run(host='0.0.0.0') # production use
    app.run(ssl_context="adhoc", debug=True)  # testing
