"""
College board SAT Question Bank Parser
ICS3U-01
Ryan
From the scraped SAT question bank JSONs, this program parses it into the database.
Apr 22, 2026
"""

# Json library import - to import json
import json

# Internal class import - questions, multiple choice options, correct answers
from models.questions import Question, MultipleChoiceOption, CorrectAnswer

# Load english and math questions
with open("question_scraping/english.json", "r") as e:
    english_bank = json.load(e)

with open("question_scraping/math.json", "r") as m:
    math_bank = json.load(m)


# Utility function to process questions
def process_question(question, section):
    """
    Processes questions and adds them to the database.
    It fills out all fields (depending on the question type).
    It considers things like if there is no stimulus (i.e. for math questions) and whether the question is multiple choice or not.

    Arguments:
        - question (dict): The dictionary object with the question.
        - section (str): The question section, whether "math" or "english"
    """

    # Consider if the question has a stimulus or not. If not just set it to none
    if "stimulus" in question.keys():
        stimulus = question["stimulus"]
    else:
        stimulus = None

    # Insert question into the database
    Question.create(question["questionId"], question["external_id"], section, question["type"], question["skill_cd"], question["skill_desc"], question["difficulty"], stimulus, question["stem"], question["rationale"])

    # Insert all the answers into the database of correct answers.
    for answer in question["correct_answer"]:
        CorrectAnswer.create(question["questionId"], answer)

    # If it's a multiple choice question, add it to the options database
    if question["type"].lower() == "mcq":
        for idx, option in enumerate(question["answerOptions"]):
            MultipleChoiceOption.create(option["id"], question["questionId"], idx, option["content"])


# Loop over each question in the bank and add it to the database
for eng_question in english_bank:
    process_question(eng_question, "english")

for math_question in math_bank:
    process_question(math_question, "math")
