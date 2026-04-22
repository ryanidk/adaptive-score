"""
College board SAT Question Bank Scraper
ICS3U-01
Ryan
This program scrapes the official SAT question bank and puts it in a JSON.
Apr 22, 2026
"""

# Expect this to take like an hour to scrape all the questions.
# Note to self when parsing: remember to remove unnecessary newlines, especially in the math questions. They cause mathjax issues.

# Requests - needed to scrape
import requests

# Json - needed to parse json and export to the file
import json

# Initialize english question bank and math question bank
english_question_bank = []
math_question_bank = []


# Scrape all english questions
# Begin by making the web request
english_json_data = {
    'asmtEventId': 99,
    'test': 1,
    'domain': 'INI,CAS,EOI,SEC',
}

# Make the request itself, this will turn it into a list since we are parsing the json
temp_english_questions = requests.post(
    'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions',
    json=english_json_data,
).json()

# Loop over each question and scrape it individually
for question in temp_english_questions:
    # The json data we send is the "external id" of the question
    question_json_data = {
        'external_id': question['external_id'],
    }

    question_response = requests.post(
        'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
        json=question_json_data,
    ).json()

    all_question_info = question | question_response

    # Append the question info to the question bank
    english_question_bank.append(all_question_info)

    # Debug
    print("Succesfully parsed Id " + all_question_info["questionId"])


# Scrape all math questions
# Begin by making the web request
math_json_data = {
    'asmtEventId': 99,
    'test': 2,
    'domain': 'H,P,Q,S',
}

# Make the request itself, this will turn it into a list since we are parsing the json
temp_math_questions = requests.post(
    'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions',
    json=math_json_data,
).json()

# Loop over each question and scrape it individually
for question in temp_math_questions:
    # There's a chance that the question is old, so only parse the question if it actually has an external ID.
    if question['external_id'] is not None:
        # The json data we send is the "external id" of the question
        question_json_data = {
            'external_id': question['external_id'],
        }

        question_response = requests.post(
            'https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question',
            json=question_json_data,
        ).json()

        all_question_info = question | question_response

        # Note to self: sometimes the math questions will not have an answerOptions key. This is a free response.
        # In all cases, correct_answers are stored in the correct_answer key. For multiple choice, it's A, B, C, or D.

        # Append the question info to the question bank
        math_question_bank.append(all_question_info)

        # Debug
        print("Succesfully parsed Id " + all_question_info["questionId"])
    else:
        # Debug
        print("Question OLD " + question["questionId"])


# Quick count the banks
print(f"Math questions: {len(math_question_bank)}")
print(f"English questions: {len(english_question_bank)}")

# Dump the question banks to their files
with open("math.json", "w") as f:
    json.dump(math_question_bank, f)

with open("english.json", "w") as f:
    json.dump(english_question_bank, f)