"""
Diagnostic Engine
ICS3U-01
Ryan
This program contains functions for the diagnostic, which generates diagnostic tests with 16 questions in total.
It generates 8 questions per subject (one medium and one hard for the general category for each one).
It also handles diagnostic submission.
Last modified: May 15, 2026
"""

# Random import to fetch random skill
import random

# Constants import
from constants import *
from db import get_db

# Skill and questions classes
from models.user import Skill
from models.questions import Question, CorrectAnswer

# Util functions from adaptive testing
from services.adaptive_testing import check_correct_response


# All functions

def generate_diagnostic():
    """
    Helper function to generate a diagnostic test. The test consists of 16 questions in a list.

    Returns:
        questions (list[dict[str id, int number]]): The list with a dictionary of questions consisting of the question ID and the number of the question.
    """

    questions = []

    cur_number = 1

    # Loop over the skill categories and then find a random skill to test for that one
    for category in SKILL_CATEGORIES.keys():
        # Find two random categories to test with two different difficulties: Medium and hard
        skill_1 = random.choice(SKILL_CATEGORIES[category])

        # Get a random question in this skill in the medium
        question_1 = Question.get_by_skill_and_difficulty(skill_1, "M")

        # There is a possibility that it will be None, given not all skills have a medium difficulty question (they all have hard questions though). Let's while loop to prevent that.
        if question_1 is None:
            # Find two random categories to test with two different difficulties: Medium and hard
            skill_1 = random.choice(SKILL_CATEGORIES[category])

            # Get a random question in this skill in the medium
            question_1 = Question.get_by_skill_and_difficulty(skill_1, "M")

        # Parse it into a dictionary with the id and the number, then increment it
        question_1_dict = {"id": question_1.id, "number": cur_number}

        cur_number += 1

        # Second question
        skill_2 = random.choice(SKILL_CATEGORIES[category])

        # Get a random question in this skill in the hard
        question_2 = Question.get_by_skill_and_difficulty(skill_2, "H")

        # Parse it into a dictionary with the id and the number, then increment it
        question_2_dict = {"id": question_2.id, "number": cur_number}

        # Put both of them into the dictionary and increment the number
        questions.extend((question_1_dict, question_2_dict))

        cur_number += 1

    return questions


def process_diagnostic_responses(user_id, responses):
    """
    Processes the diagnostic responses for a particular user, and updates their skills in the category.

    Args:
        user_id (str): The user ID who answered the diagnostic
        responses (list[dict[str question_id, response]]): A list containing the questions and responses that was stored in the session.

    Returns:
        results (dict[str category]: dict[str difficulty, int correct_responses]): The new skill sets.
    """

    # Initialize empty results dictionary for now
    results = {}

    # Fill it in via the broad categories:
    for category in SKILL_CATEGORIES.keys():
        results[category] = {"difficulty": "E", "correct_responses": 0}

    # Go through the questions answered, check if they are correct, and update the number of correct responses accordingly
    for response in responses:
        # Fetch the response but strip it of whitespace
        response_text = response["response"].strip().replace(" ", "")

        # Fetch the question and the ID
        question = Question.get_by_id(response["question_id"])

        # Get the broad category for the skill
        category = next((k for k, v in SKILL_CATEGORIES.items() if question.skill in v), None)

        # Get accepted answers and convert them to a list
        accepted_answers = CorrectAnswer.get_by_question_id(question.id)
        accepted_answers_list = [ca.answer for ca in accepted_answers]

        # Check if it's a correct response and if it is update the dict
        correct = check_correct_response(accepted_answers_list, response_text, question.type)

        # Update the dictionary if applicable
        if correct:
            results[category]["correct_responses"] += 1

            # Check if it's reached 1 or 2 to update the difficulty accordingly
            if results[category]["correct_responses"] >= 2:
                results[category]["difficulty"] = "H"
            elif results[category]["correct_responses"] >= 1:
                results[category]["difficulty"] = "M"

    # Now update the user's skill difficulties
    for category, details in results.items():
        for skill in SKILL_CATEGORIES[category]:
            Skill.update_difficulty_without_commit(user_id, skill, details["difficulty"])

    # Commit to the DB now
    get_db().commit()

    # Return the results
    return results
