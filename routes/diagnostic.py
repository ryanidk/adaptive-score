"""
Diagnostic Routes
ICS3U-01
Ryan
These routes handle diagnostics and the showing of questions.
Last Modified: May 15, 2026
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
from services.diagnostic import generate_diagnostic, process_diagnostic_responses

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

            # We will also clear the responses data to ensure it doesn't accidentally continue on
            session["diagnostic_responses"] = []

        next_question_id = next_questions[0].get("id", "")
        next_question_number = next_questions[0].get("number", 1)

        # Retrieve the question
        question = Question.get_by_id(next_question_id)

        # Only if there's a question do we try to process it
        if question is not None:
            # Different render template for different types of questions
            if question.section.lower() == "english":
                # English questions are ALWAYS multiple choice, so get the options
                options = MultipleChoiceOption.get_options_by_question_id(question.id)

                # List out options (just in case)
                # Also remove the beginning and end paragraph symbols

                option_A = sanitize_option(options[0].content)
                option_B = sanitize_option(options[1].content)
                option_C = sanitize_option(options[2].content)
                option_D = sanitize_option(options[3].content)

                diagnostic_response = render_template("english_mcq.html", name=current_user.name,
                                                    email=current_user.email,
                                                    question_id=question.id, stimulus=question.stimulus,
                                                    skill=question.skill_description,
                                                    difficulty=question.difficulty, stem=question.stem,
                                                    option_A=option_A, option_B=option_B, option_C=option_C,
                                                    option_D=option_D, question_number=next_question_number)

            elif question.section.lower() == "math" and question.type.lower() == "mcq":
                # Math multiple choice question
                options = MultipleChoiceOption.get_options_by_question_id(question.id)

                # List out options (just in case)
                # Also remove the beginning and end paragraph symbols
                option_A = sanitize_option(options[0].content)
                option_B = sanitize_option(options[1].content)
                option_C = sanitize_option(options[2].content)
                option_D = sanitize_option(options[3].content)

                diagnostic_response = render_template("math_mcq.html", name=current_user.name, email=current_user.email,
                                                    question_id=question.id,
                                                    skill=question.skill_description,
                                                    difficulty=question.difficulty, stem=question.stem,
                                                    option_A=option_A, option_B=option_B, option_C=option_C,
                                                    option_D=option_D, question_number=next_question_number)

            elif question.section.lower() == "math" and question.type.lower() == "spr":
                # Just render the template
                diagnostic_response = render_template("math_spr.html", name=current_user.name, email=current_user.email,
                                                    question_id=question.id,
                                                    skill=question.skill_description,
                                                    difficulty=question.difficulty, stem=question.stem,
                                                    question_number=next_question_number)

    # Handle POST requests (form submission), essentially just add the form elements to the session
    elif request.method == "POST":
        # Retrieve form
        form_data = request.form

        # Make sure the question ID and the answer actually exist so we don't end up creating errors.
        # Also, ideally we will not be vulnerable to attacks in this case.

        question = Question.get_by_id(form_data["question_id"].strip())
        answer_exists = form_data["answer"].strip() != "" and form_data["answer"] is not None

        if question is not None and answer_exists:
            # Add it to the list of answers in the session
            # Check if the user already has a diagnostic responses in their session, have a default empty one
            responses_so_far = session.get("diagnostic_responses", [])

            # If we have no responses or it doesn't exist create the first entry
            if responses_so_far == [] or not responses_so_far:
                session["diagnostic_responses"] = [{"question_id": question.id, "response": form_data["answer"].strip()}]
            else:
                # Just append it
                session["diagnostic_responses"].append({"question_id": question.id, "response": form_data["answer"].strip()})

            # Now pop from the diagnostic questions
            # First we need to ensure the list is not empty before we do this, no blindly assuming!
            if session["diagnostic_questions"] != [] and session["diagnostic_questions"] is not None:
                last_question = session["diagnostic_questions"].pop(0)

            # Now check again if it's empty. If so redirect to the responses, if not just keep on going with the questions.
            if session["diagnostic_questions"] == [] or not session["diagnostic_questions"]:
                # We're done!
                diagnostic_response = redirect(url_for("diagnostic.diagnostic_complete"), 303)
            else:
                # Continue redirecting to diagnostic response
                diagnostic_response = redirect(url_for("diagnostic.diagnostic"), 303)

    return diagnostic_response

@diagnostic_blueprint.route("/diagnostic_complete")
@login_required
def diagnostic_complete():
    """
    Handles the diagnostic complete route.
    It fetches the diagnostic data from the request session and either renders a template or redirects back to the home page...

    Returns:
        (render_template): The template of the webpage to serve. CAN ALSO BE A REDIRECT
    """

    # Plain response, placeholder is a redirect
    complete_response = redirect(url_for("index"))

    # Retrieve current user id
    cur_user_id = current_user.id

    # Retrieve diagnostic questions data
    diagnostic_responses = session.pop("diagnostic_responses", [])

    # Only fetch if the list ain't empty and all the keys we need are there
    if diagnostic_responses != [] and diagnostic_responses and all("question_id" and "response" in r.keys() for r in diagnostic_responses):
        # It is safe to therefore assume that the values are safe and will not error out, as we have checked them previously
        # If the user edits the session, it will just be reset, as it is signed with a secret key.
        # This is a quite naive security implementation, but if I do end up releasing it, I will change it.

        # Process the diagnostic responses
        results = process_diagnostic_responses(cur_user_id, diagnostic_responses)

        # Set a render template
        complete_response = render_template("diagnostic_complete.html", name=current_user.name, email=current_user.email, results=results)

    # Return the complete response
    return complete_response


