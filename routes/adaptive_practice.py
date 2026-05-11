"""
Adaptive Practice Routes
ICS3U-01
Ryan
These routes handle adaptive practice (just questions, no vocab, diagnostic, or full-length test)
Last Modified: May 11, 2026
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
from services.adaptive_testing import get_random_question_for_user, process_response, sanitize_option

# Set up blueprint
adaptive_practice_blueprint = Blueprint('adaptive_practice', __name__, template_folder='../templates')


# Adaptive practice routes
@adaptive_practice_blueprint.route("/practice", methods=['GET', 'POST'])
@login_required
def practice():
    """
    Handles the practice route by generating random questions to give to the user.
    It adapts based on the type of question.
    It can also handle the POST requests and form submissions too.

    Returns:
        (render_template): The template of the webpage to serve.
    """

    # Plain response variable, placeholder is an error
    practice_response = "Could not fetch practice, please refresh the page and try again (Error 400)", 400

    # Handle GET requests to return a random question
    if request.method == "GET":
        # Retrieve current user id
        cur_user_id = current_user.id

        # Retrieve a random question
        user_question = get_random_question_for_user(cur_user_id)

        # Only if there's a question do we try to process it
        if user_question is not None:
            # Different render template for different types of questions
            if user_question.section.lower() == "english":
                # English questions are ALWAYS multiple choice, so get the options
                options = MultipleChoiceOption.get_options_by_question_id(user_question.id)

                # List out options (just in case)
                # Also remove the beginning and end paragraph symbols

                option_A = sanitize_option(options[0].content)
                option_B = sanitize_option(options[1].content)
                option_C = sanitize_option(options[2].content)
                option_D = sanitize_option(options[3].content)

                practice_response = render_template("englishmcq.html", name=current_user.name, email=current_user.email,
                                                    question_id=user_question.id, stimulus=user_question.stimulus,
                                                    skill=user_question.skill_description,
                                                    difficulty=user_question.difficulty, stem=user_question.stem,
                                                    option_A=option_A, option_B=option_B, option_C=option_C,
                                                    option_D=option_D)

            elif user_question.section.lower() == "math" and user_question.type.lower() == "mcq":
                # Math multiple choice question
                options = MultipleChoiceOption.get_options_by_question_id(user_question.id)

                # List out options (just in case)
                # Also remove the beginning and end paragraph symbols
                option_A = sanitize_option(options[0].content)
                option_B = sanitize_option(options[1].content)
                option_C = sanitize_option(options[2].content)
                option_D = sanitize_option(options[3].content)

                practice_response = render_template("mathmcq.html", name=current_user.name, email=current_user.email,
                                                    question_id=user_question.id,
                                                    skill=user_question.skill_description,
                                                    difficulty=user_question.difficulty, stem=user_question.stem,
                                                    option_A=option_A, option_B=option_B, option_C=option_C,
                                                    option_D=option_D)

            elif user_question.section.lower() == "math" and user_question.type.lower() == "spr":
                # Just render the template
                practice_response = render_template("mathspr.html", name=current_user.name, email=current_user.email,
                                                    question_id=user_question.id,
                                                    skill=user_question.skill_description,
                                                    difficulty=user_question.difficulty, stem=user_question.stem)

    # Handle POST requests to respond to a question
    elif request.method == "POST":
        # Retrieve current user id
        cur_user_id = current_user.id

        # Only fetch if all the fields we need are in the keys
        if "question_id" in request.form.keys() and "answer" in request.form.keys():
            # Make sure the question ID and the answer actually exist so we don't end up creating errors.
            # Also, ideally we will not be vulnerable to attacks in this case.

            question = Question.get_by_id(request.form["question_id"].strip())
            answer_exists = request.form["answer"].strip() != "" and request.form["answer"] is not None

            if question is not None and answer_exists:
                # Actually respond to it if the question actually exists.
                correct, accepted_answers, rationale = process_response(cur_user_id, question.id,
                                                                        request.form["answer"].strip())


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

                    # Option states: 0 = neutral, 1 = incorrect and selected, 2 = correct
                    option_A_state = 0
                    option_B_state = 0
                    option_C_state = 0
                    option_D_state = 0

                    # Make sure to highlight the correct one in green
                    match accepted_answers[0]:
                        case "A":
                            option_A_state = 2
                        case "B":
                            option_B_state = 2
                        case "C":
                            option_C_state = 2
                        case "D":
                            option_D_state = 2

                    # If the user selected the wrong answer mark it in red
                    if not correct:
                        match request.form["answer"].strip():
                            case "A":
                                option_A_state = 1
                            case "B":
                                option_B_state = 1
                            case "C":
                                option_C_state = 1
                            case "D":
                                option_D_state = 1

                    practice_response = render_template("englishmcqresponse.html", name=current_user.name,
                                                        email=current_user.email,
                                                        question_id=question.id, stimulus=question.stimulus,
                                                        skill=question.skill_description,
                                                        difficulty=question.difficulty, stem=question.stem,
                                                        option_A=option_A, option_B=option_B, option_C=option_C,
                                                        option_D=option_D, option_A_state=option_A_state,
                                                        option_B_state=option_B_state, option_C_state=option_C_state,
                                                        option_D_state=option_D_state, rationale=rationale)

                elif question.section.lower() == "math" and question.type.lower() == "mcq":
                    # English questions are ALWAYS multiple choice, so get the options
                    options = MultipleChoiceOption.get_options_by_question_id(question.id)

                    # List out options (just in case)
                    # Also remove the beginning and end paragraph symbols

                    option_A = sanitize_option(options[0].content)
                    option_B = sanitize_option(options[1].content)
                    option_C = sanitize_option(options[2].content)
                    option_D = sanitize_option(options[3].content)

                    # Option states: 0 = neutral, 1 = incorrect and selected, 2 = correct
                    option_A_state = 0
                    option_B_state = 0
                    option_C_state = 0
                    option_D_state = 0

                    # Make sure to highlight the correct one in green
                    match accepted_answers[0]:
                        case "A":
                            option_A_state = 2
                        case "B":
                            option_B_state = 2
                        case "C":
                            option_C_state = 2
                        case "D":
                            option_D_state = 2

                    # If the user selected the wrong answer mark it in red
                    if not correct:
                        match request.form["answer"].strip():
                            case "A":
                                option_A_state = 1
                            case "B":
                                option_B_state = 1
                            case "C":
                                option_C_state = 1
                            case "D":
                                option_D_state = 1

                    practice_response = render_template("mathmcqresponse.html", name=current_user.name,
                                                        email=current_user.email,
                                                        question_id=question.id,
                                                        skill=question.skill_description,
                                                        difficulty=question.difficulty, stem=question.stem,
                                                        option_A=option_A, option_B=option_B, option_C=option_C,
                                                        option_D=option_D, option_A_state=option_A_state,
                                                        option_B_state=option_B_state, option_C_state=option_C_state,
                                                        option_D_state=option_D_state, rationale=rationale)

                elif question.section.lower() == "math" and question.type.lower() == "spr":
                    # Just render the template
                    practice_response = render_template("mathsprresponse.html", name=current_user.name,
                                                        email=current_user.email,
                                                        question_id=question.id,
                                                        skill=question.skill_description,
                                                        difficulty=question.difficulty, stem=question.stem,
                                                        correct=correct, accepted_answers=accepted_answers,
                                                        rationale=rationale, user_answer=request.form["answer"].strip())

    # Return practice response
    return practice_response
