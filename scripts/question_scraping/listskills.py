"""
Question bank skill lister
ICS3U-01
Ryan
This program lists the skills from a question bank.
Apr 20, 2026
"""

import json

# Set up a set of skills. The purpose of a set is that avoids duplicate elements.
skills = set()

# Open up the question bank
with open("english.json", "r") as f:
    questions = json.load(f)

# Loop over the questions and adds the skill category.
for question in questions:
    skills.add(question["skill_cd"])

# Print the skills
print(skills)