"""
Constants
ICS3U-01
Ryan
This file represents the constants for Adaptive Score
Last modified: May 11, 2026
"""

# Skill sets
ENGLISH_SKILLS = {'INF', 'TSP', 'FSS', 'BOU', 'COE', 'CID', 'WIC', 'CTC', 'TRA', 'SYN'}
MATH_SKILLS = {'P.B.', 'S.B.', 'Q.G.', 'H.E.', 'Q.D.', 'Q.F.', 'H.A.', 'H.B.', 'Q.B.', 'Q.A.', 'Q.E.', 'S.A.', 'P.A.',
               'H.C.', 'S.C.', 'Q.C.', 'H.D.', 'S.D.', 'P.C.'}

SKILL_DESCRIPTIONS = {'INF': 'Inferences', 'CID': 'Central Ideas and Details', 'COE': 'Command of Evidence',
                      'WIC': 'Words in Context', 'TSP': 'Text Structure and Purpose', 'CTC': 'Cross-Text Connections',
                      'TRA': 'Transitions', 'SYN': 'Rhetorical Synthesis', 'BOU': 'Boundaries',
                      'FSS': 'Form, Structure, and Sense', 'H.A.': 'Linear equations in one variable',
                      'H.D.': 'Systems of two linear equations in two variables', 'H.B.': 'Linear functions',
                      'H.C.': 'Linear equations in two variables',
                      'H.E.': 'Linear inequalities in one or two variables', 'P.C.': 'Nonlinear functions',
                      'P.B.': 'Nonlinear equations in one variable and systems of equations in two variables ',
                      'P.A.': 'Equivalent expressions', 'Q.A.': 'Ratios, rates, proportional relationships, and units',
                      'Q.E.': 'Probability and conditional probability',
                      'Q.F.': 'Inference from sample statistics and margin of error ', 'Q.B.': 'Percentages',
                      'Q.C.': 'One-variable data: Distributions and measures of center and spread',
                      'Q.D.': 'Two-variable data: Models and scatterplots',
                      'Q.G.': 'Evaluating statistical claims: Observational studies and experiments ',
                      'S.B.': 'Lines, angles, and triangles', 'S.A.': 'Area and volume',
                      'S.C.': 'Right triangles and trigonometry', 'S.D.': 'Circles'}

# Percentage accuracy threshold for the user to move down a difficulty
LOWER_DIFFICULTY_THRESHOLD = 0.55

# Percentage accuracy threshold for the user to move up a difficulty
UPPER_DIFFICULTY_THRESHOLD = 0.75
