from flask_login import UserMixin

from db import get_db

# TODO better document, add header

# All possible skills:
english_skills = {'INF', 'TSP', 'FSS', 'BOU', 'COE', 'CID', 'WIC', 'CTC', 'TRA', 'SYN'}
math_skills = {'P.B.', 'S.B.', 'Q.G.', 'H.E.', 'Q.D.', 'Q.F.', 'H.A.', 'H.B.', 'Q.B.', 'Q.A.', 'Q.E.', 'S.A.', 'P.A.', 'H.C.', 'S.C.', 'Q.C.', 'H.D.', 'S.D.', 'P.C.'}

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user


    @staticmethod
    def getAllUsers():
        db = get_db()
        items = db.execute('SELECT name,email FROM user').fetchall()
        return items


    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()


class Skill:
    def __init__(self, user_id, skill, attempts, correct_attempts):
        self.user_id = user_id
        self.skill = skill
        self.attempts = attempts
        self.correct_attempts = correct_attempts

    @staticmethod
    def get_skills(user_id):
        # TODO change this to only have one return
        db = get_db()
        db_skills = db.execute(
            "SELECT * FROM skills WHERE user_id = ?", (user_id,)
        ).fetchall()
        if len(db_skills) == 0:
            return None

        skills = []

        for temp_skill in db_skills:
            skill = Skill(
                user_id=temp_skill[0], skill=temp_skill[1], attempts=temp_skill[2], correct_attempts=temp_skill[3]
            )
            skills.append(skill)

        return skills

    @staticmethod
    def update_skill(user_id, skill, correct_answer):
        """
        TODO fix docstring
        correct_answer is either true or false
        """

        correct_increment = 1 if correct_answer else 0

        db = get_db()
        db.execute(
            "UPDATE skills SET attempts = attempts + 1, correct_attempts = correct_attempts + ? WHERE user_id = ? AND skill = ?", (correct_increment, user_id, skill))
        db.commit()


    @staticmethod
    def create_skills(user_id):
        db = get_db()
        for skill in (english_skills | math_skills):
            db.execute(
                "INSERT INTO skills (user_id, skill)"
                " VALUES (?, ?)",
                (user_id, skill),
            )
        db.commit()