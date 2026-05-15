"""
Adaptive Testing Engine
ICS3U-01
Ryan
This program contains functions for adaptive testing, such as getting a random question based on any random skill.
It also handles question submission.
Last modified: May 15, 2026
"""

# Random import to fetch random skill
import random

# Regex import to string replace
import re

# Internal model imports (variables and classes)
from constants import *

# Skill and questions classes
from models.user import Skill
from models.questions import Question, CorrectAnswer


# All functions

def check_correct_response(accepted_answers_list, response, question_type):
    """
    Utility function to check if the response given is accepted or not.

    Args:
        accepted_answers_list (list): A list with the correct answers
        response (str): The user's response
        question_type (str): The question type, either "mcq" or "spr"

    Returns:
        correct (bool): Whether the answer was correct or not
    """

    # Generic correct = False
    correct = False

    # First, just straight up check if the answer is in the list of correct answers. If so move on.
    if response in accepted_answers_list:
        correct = True
    # If it's not (and the question is a student produced response) start sanitizing it to try to find a match within 0.001
    elif question_type == "spr":
        # Check that the answer can be converted into a float in the first place.
        # Fractions do not need a normalized answer...
        floating_response = None

        try:
            floating_response = float(response)
        except ValueError:
            # It must be a fraction or invalid, so pass
            correct = False

        # Set a current index to iterate over the list
        current_index = 0

        # If there's a floating response just iterate over each of the answers to find one within the margin...
        if floating_response is not None:
            while not correct and current_index < len(accepted_answers_list):
                answer = accepted_answers_list[current_index]
                current_index += 1
                floating_answer = None

                # Try to convert to a float, otherwise just pass
                try:
                    floating_answer = float(answer)
                except ValueError:
                    # Move on with the day
                    continue

                # Check the answer float for the student produced response answer margin
                if abs(floating_answer - floating_response) <= SPR_ANSWER_MARGIN:
                    correct = True
                    # This will end the loop here

    return correct


def get_random_question_for_user(user_id):
    """
    Gets a random question for the user based on a random skill and their current difficulty.

    Args:
        user_id (str): The user's unique ID.

    Returns:
        question (Question): A question object representing the random question we should return to the user. Can be None.
    """

    # First, pick a random skill to test
    random_skill = random.choice(list(ENGLISH_SKILLS | MATH_SKILLS))

    # Get the user's difficulty in that skill
    user_skill = Skill.get_skill(user_id, random_skill)

    # Only continue with the next steps if the skill actually exists
    if user_skill is not None:
        # This can be None as well. We are just trying to avoid SQL errors passing null arguments.
        question = Question.get_by_skill_and_difficulty(random_skill, user_skill.difficulty)
    else:
        # Explicitly set the question to None anyway
        question = None

    return question


def process_response(user_id, question_id, response):
    """
    Processes a response for a particular user, also updating their skills to match that.
    It also considers whether a response is student produced or not, and normalizes the answer regardless.

    Args:
        user_id (str): The user ID who answered the question
        question_id (str): The ID of the question
        response (str): The response of the user. For multiple choice, i.e. A, B, for free response, i.e. 41.67

    Returns:
        correct (bool): True if the response was correct, False if not
        accepted_answers (list[CorrectAnswer]): The list of correct answers
        rationale (str): The rationale behind the correct answer.
    """

    # Clear whitespace from response
    response = response.strip().replace(" ", "")

    # Get the question
    question = Question.get_by_id(question_id)

    # Get the valid answers
    accepted_answers = CorrectAnswer.get_by_question_id(question_id)

    # Convert them to a list
    accepted_answers_list = [ca.answer for ca in accepted_answers]

    # Check correct response
    correct = check_correct_response(accepted_answers_list, response, question.type)

    # Now update the skill!
    Skill.update_attempts(user_id, question.skill, correct)

    # Get the skill's current attempts, update the difficulty (if applicable...)
    user_skill = Skill.get_skill(user_id, question.skill)

    # Now check if the attempts is the value set in the constants (or more). Then update the difficulty level accordingly
    # Moves down and up depending on accuracy
    if user_skill.attempts >= DIFFICULTY_UPDATE_QUESTION_THRESHOLD:
        # Placeholder difficulty stays the same.
        new_difficulty = user_skill.difficulty

        # I corrected for floating point math
        if user_skill.correct_attempts / user_skill.attempts <= LOWER_DIFFICULTY_THRESHOLD:
            # Drop the user a difficulty depending on current difficulty
            if user_skill.difficulty == "M":
                new_difficulty = "E"
            elif user_skill.difficulty == "H":
                new_difficulty = "M"
        elif user_skill.correct_attempts / user_skill.attempts >= UPPER_DIFFICULTY_THRESHOLD:
            # Bump up the difficulty depending on current
            if user_skill.difficulty == "E":
                new_difficulty = "M"
            elif user_skill.difficulty == "M":
                new_difficulty = "H"

        # Execute function to update difficulty
        Skill.update_difficulty(user_id, question.skill, new_difficulty)

    # Now just return everything
    return correct, accepted_answers_list, question.rationale
