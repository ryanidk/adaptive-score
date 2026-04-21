-- Users
-- Contains a unique id, their name, email and profile picture (from Google)
CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT
);

-- Questions
-- This is the same format as the CollegeBoard json.
-- Section, type, skill, skill description, and difficulty are self-explanatory.
-- Stimulus is either a passage (mainly for english) or the problem. SOMETIMES, it will be empty for math questions.
-- Stem is the main topic of the problem, i.e. Which choice most logically completes the text?
-- Rationale is self-explanatory, the reason behind the answer.
CREATE TABLE question (
  id TEXT PRIMARY KEY,
  college_board_id TEXT,
  section TEXT, -- either math or english
  type TEXT, -- either mcq (multiple choice) or spr (student-produced response)
  skill TEXT,
  skill_description TEXT,
  difficulty TEXT, -- either E, M, or H
  stimulus TEXT, -- it can be null
  stem TEXT,
  rationale TEXT
);

-- Multiple choice questions
-- Most of these fields are pretty self-explanatory.
CREATE TABLE question_option (
    id TEXT PRIMARY KEY,
    question_id TEXT,
    idx INTEGER, -- 0=A, 1=B, 2=C, 3=D, indexes of the answer
    content TEXT,
    FOREIGN KEY(question_id) REFERENCES question(id)
);

-- Correct answers
-- Also pretty self-explanatory.
CREATE TABLE correct_answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT,
    answer TEXT, -- can be B, lots of possibilities
    FOREIGN KEY(question_id) REFERENCES question(id)
)

-- Skill tracking
-- Pretty self-explanatory.
CREATE TABLE skills (
    user_id TEXT,
    skill TEXT,
    attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    PRIMARY KEY(user_id, skill)
);

-- TODO add a db of attempts to avoid duplicates