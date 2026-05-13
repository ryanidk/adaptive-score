"""
Diagnostic Engine
ICS3U-01
Ryan
This program contains functions for the diagnostic, which generates diagnostic tests with 16 questions in total.
It generates 8 questions per subject (one medium and one hard for the general category for each one).
It also handles diagnostic submission.
Last modified: May 13, 2026
"""

# Random import to fetch random skill
import random

# Constants import
from constants import *

# Skill and questions classes
from models.user import Skill
from models.questions import Question, CorrectAnswer


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
        while question_1 is None:
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
