"""
Diagnostic Routes
ICS3U-01
Ryan
These routes handle diagnostics and the showing of questions.
Last Modified: May 13, 2026
"""

# Necessary imports
from flask import Blueprint, render_template, redirect, url_for, request, session
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
from models.questions import Question, MultipleChoiceOption, CorrectAnswer
from services.adaptive_testing import sanitize_option
from services.diagnostic import generate_diagnostic

# Set up blueprint
diagnostic_blueprint = Blueprint('diagnostic', __name__, template_folder='../templates')


# Diagnostic routes
@diagnostic_blueprint.route("/diagnostic", methods=['GET', 'POST'])
@login_required
def diagnostic():
    """
    Handles the diagnostic route by either generating a diagnostic to serve to the user.
    It adapts based on the type of question.
    It can also handle the POST requests and form submissions too.

    Returns:
        (render_template): The template of the webpage to serve.
    """

    # Plain response variable, placeholder is a redirect
    diagnostic_response = "Could not fetch diagnostic, please refresh the page and try again (Error 400)", 400

    # Handle GET requests to return a diagnostic question
    if request.method == "GET":
        # Check if the user already has a diagnostic in their session, have a default empty one
        next_questions = session.get("diagnostic_questions", [])

        # If it's empty generate a diagnostic and store it in the session
        if next_questions == [] or not next_questions:
            next_questions = generate_diagnostic()

            # We still add the full diagnostic question list to the session; we only clear it from the session upon submission, as the user can just refresh the page to get through the diagnostic without actually answering any questions.
            session["diagnostic_questions"] = next_questions

    # TODO finish this, add a diagnostic result route, finish the POST requests, add a way to handle the questions (probably store form data in a session)