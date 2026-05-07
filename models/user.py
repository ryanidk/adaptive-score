"""
User classes: User and Skill
ICS3U-01
Ryan
This file represents the User and Skill classes used in the app
Last modified: Apr 29, 2026
"""

# Flask login for authentication, and db to access the database
from flask_login import UserMixin
from db import get_db

# A list of all possible skills:
english_skills = {'INF', 'TSP', 'FSS', 'BOU', 'COE', 'CID', 'WIC', 'CTC', 'TRA', 'SYN'}
math_skills = {'P.B.', 'S.B.', 'Q.G.', 'H.E.', 'Q.D.', 'Q.F.', 'H.A.', 'H.B.', 'Q.B.', 'Q.A.', 'Q.E.', 'S.A.', 'P.A.',
               'H.C.', 'S.C.', 'Q.C.', 'H.D.', 'S.D.', 'P.C.'}


class User(UserMixin):
    """
    This class represents a User object that is authenticated with Google.

    Attributes:
        id (str): The unique user ID from Google
        name (str): The user's name from Google
        email (str): The user's image
        profile_pic (str): A url of the user's profile picture on Google
    """

    def __init__(self, id_, name, email, profile_pic):
        """
        Initializes the User object

        Args:
            id_ (str): The unique user ID from Google
            name (str): The user's name from Google
            email (str): The user's image
            profile_pic (str): A url of the user's profile picture on Google
        """

        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        """
        Static method: Gets a user by ID and returns a User object

        Args:
            user_id (str): The ID of the user

        Returns:
            user (User): The user object representing the user
        """

        # Load the database
        db = get_db()

        # Fetch the user
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

        # Ensure that a user actually exists
        if user:
            user = User(
                id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
            )
        else:
            # Explicitly set the user to none
            # Ms. Edwards I know you hate multiple returns so I am just explicitly doing this
            user = None

        return user

    @staticmethod
    def get_all_users():
        """
        Static method: Gets all the user in the database and returns them as a list

        Returns:
            items (dict[name, email]): A dictionary of all users' names and emails
        """

        # Load database
        db = get_db()

        # Get name and email columns (all of them)
        items = db.execute('SELECT name, email FROM user').fetchall()

        return items

    @staticmethod
    def create(id_, name, email, profile_pic):
        """
        Static method: Creates a user

        Args:
            id_ (str): The unique user ID from Google
            name (str): The user's name from Google
            email (str): The user's image
            profile_pic (str): A url of the user's profile picture on Google
        """

        # Load the database
        db = get_db()

        # Insert the user's details
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )

        # Commit to the database
        db.commit()


class Skill:
    """
    This class represents the Skills from a user.
    There are many skills, and every user will have multiple rows to represent each and every skill.

    Attributes:
        user_id (str): The user ID (from Google)
        skill (str): An ID representing the skill, i.e., INF, TSP, etc.
        attempts (int): The number of attempts at questions in this category by the user.
        correct_attempts (int): How many correct attempts at questions in this category by the user.
        difficulty (str): Either E, M, or H, representing the user's current skill level.
    """

    def __init__(self, user_id, skill, attempts, correct_attempts, difficulty):
        """
        Initializes a Skill object.

        Args:
            user_id (str): The user ID (from Google)
            skill (str): An ID representing the skill, i.e., INF, TSP, etc.
            attempts (int): The number of attempts at questions in this category by the user.
            correct_attempts (int): How many correct attempts at questions in this category by the user.
            difficulty (str): Either E, M, or H, representing the user's current skill level.
        """

        self.user_id = user_id
        self.skill = skill
        self.attempts = attempts
        self.correct_attempts = correct_attempts
        self.difficulty = difficulty

    @staticmethod
    def get_skills(user_id):
        """
        Static method: Gets a list of all Skill objects for a user.

        Args:
            user_id (str): The user ID to fetch the skills from

        Returns:
            skills (list[Skill]): A list with many Skill objects representing the individual skills. Can be empty.
        """

        # Get the database
        db = get_db()

        # Fetch the skills
        db_skills = db.execute(
            "SELECT * FROM skills WHERE user_id = ?", (user_id,)
        ).fetchall()

        # Initialize list of skills, note that this can be empty
        skills = []

        # Loop over all skills to create objects to be added to the list above
        for temp_skill in db_skills:
            skill = Skill(
                user_id=temp_skill[0], skill=temp_skill[1], attempts=temp_skill[2], correct_attempts=temp_skill[3],
                difficulty=temp_skill[4]
            )
            skills.append(skill)

        return skills

    @staticmethod
    def get_skill(user_id, skill):
        """
        Static method: Gets an individual Skill object for a user.

        Args:
            user_id (str): The user ID to fetch the skills from
            skill (str): The skill ID to fetch

        Returns:
            return_skill (Skill): A skill object representing the user skill. Can be none if it doesn't exist.
        """

        # Get the database
        db = get_db()

        # Fetch the skills
        db_skill = db.execute(
            "SELECT * FROM skills WHERE user_id = ? AND skill = ?", (user_id, skill,)
        ).fetchone()

        # Only create the skill object if it actually exists. Otherwise, just make it explicitly none.

        if db_skill:
            return_skill = Skill(
                user_id=db_skill[0], skill=db_skill[1], attempts=db_skill[2], correct_attempts=db_skill[3],
                difficulty=db_skill[4]
            )
        else:
            return_skill = None

        return return_skill

    @staticmethod
    def update_attempts(user_id, skill, correct_answer):
        """
        Static method: Update the attempts of a skill for the user whether they got the answer correct or not.

        Args:
            user_id (str): The unique user ID of the user
            skill (str): The skill ID, i.e., INF, TSP, etc.
            correct_answer (bool): Whether the correct answer was selected, either True or False
        """

        # Set the correct answer increment amount. 1 if it was correct, 0 if not.
        correct_increment = 1 if correct_answer else 0

        # Fetch the database
        db = get_db()

        # Update the skill
        db.execute(
            "UPDATE skills SET attempts = attempts + 1, correct_attempts = correct_attempts + ? WHERE user_id = ? AND skill = ?",
            (correct_increment, user_id, skill))

        # Commit to the database
        db.commit()

    @staticmethod
    def update_difficulty(user_id, skill, difficulty):
        """
        Static method: Updates the difficulty of a specified skill to a new difficulty and resets attempts.

        Args:
            user_id (str): The user ID to update the skills for/
            skill (str): The ID representing the skill to update, i.e., INF
            difficulty (str): The difficulty to update the user to, either E, M, or H.
        """

        # Fetch database
        db = get_db()

        # Update skills table
        db.execute(
            "UPDATE skills SET difficulty = ?, attempts = 0, correct_attempts = 0 WHERE user_id = ? AND skill = ?",
            (difficulty, user_id, skill))

        # Commit to database
        db.commit()

    @staticmethod
    def create_skills(user_id):
        """
        Static method: Creates skills for a user ID

        Args:
            user_id (str): The user ID to create skills for.
        """

        # Fetch database
        db = get_db()

        # For each skill in the combined skill list, insert a row into the table
        for skill in (english_skills | math_skills):
            db.execute(
                "INSERT INTO skills (user_id, skill)"
                " VALUES (?, ?)",
                (user_id, skill),
            )

        # Commit to the database
        db.commit()
