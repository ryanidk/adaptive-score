"""
Adaptive Practice Routes
ICS3U-01
Ryan
These routes handle adaptive practice (just questions, no vocab, diagnostic, or full-length test)
Last Modified: May 1, 2026
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
from models.questions import Question, MultipleChoiceOption, CorrectAnswer
from services.adaptive_testing import get_random_question_for_user, process_response

# Set up blueprint
adaptive_practice_blueprint = Blueprint('adaptive_practice', __name__, template_folder='../templates')