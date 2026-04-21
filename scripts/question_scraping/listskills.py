"""
Question bank skill lister
ICS3U-01
Ryan
This program lists the skills from a question bank.
Apr 20, 2026
"""

import json
skills = set()

with open("english.json", "r") as f:
    questions = json.load(f)

for question in questions:
    skills.add(question["skill_cd"])

print(skills)