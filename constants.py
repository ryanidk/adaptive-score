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

# Percentage accuracy threshold for the user to move down a difficulty
LOWER_DIFFICULTY_THRESHOLD = 0.55

# Percentage accuracy threshold for the user to move up a difficulty
UPPER_DIFFICULTY_THRESHOLD = 0.75