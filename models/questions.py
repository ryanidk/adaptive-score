from db import get_db

# TODO better document, add header
class Question:
    def __init__(self, q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem, rationale):
        self.id = q_id
        self.college_board_id = college_board_id
        self.section = section
        self.type = q_type
        self.skill = skill
        self.skill_description = skill_description
        self.difficulty = difficulty
        self.stimulus = stimulus
        self.stem = stem
        self.rationale = rationale

    @staticmethod
    def get_by_id(question_id):
        # TODO change this to only have one return
        db = get_db()
        question = db.execute(
            "SELECT * FROM question WHERE id = ?", (question_id,)
        ).fetchone()
        if not question:
            return None

        question = Question(
            q_id=question[0], college_board_id=question[1], section=question[2], q_type=question[3], skill=question[4], skill_description=question[5], difficulty=question[6], stimulus=question[7], stem=question[8], rationale=question[9]
        )
        return question

    @staticmethod
    def get_by_skill_and_difficulty(skill, difficulty):
        db = get_db()
        question = db.execute(
            "SELECT * FROM question WHERE skill = ? AND difficulty = ? ORDER BY RANDOM() LIMIT 1", (skill, difficulty)
        ).fetchone()
        return question

    @staticmethod
    def create(q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem, rationale):
        db = get_db()
        db.execute(
            "INSERT INTO question (id, college_board_id, section, type, skill, skill_description, difficulty, stimulus, stem, rationale)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem, rationale),
        )
        db.commit()


class MultipleChoiceOption:
    def __init__(self, o_id, question_id, idx, content):
        self.id = o_id
        self.question_id = question_id
        self.idx = idx
        self.content = content

    @staticmethod
    def get_by_option_id(option_id):
        # TODO change this to only have one return
        db = get_db()
        option = db.execute(
            "SELECT * FROM question_option WHERE id = ?", (option_id,)
        ).fetchone()
        if not option:
            return None

        option = MultipleChoiceOption(
            o_id=option[0], question_id=option[1], idx=option[2], content=option[3]
        )
        return option

    @staticmethod
    def get_options_by_question_id(question_id):
        # TODO change this to only have one return
        db = get_db()
        db_options = db.execute(
            "SELECT * FROM question_option WHERE question_id = ?", (question_id,)
        ).fetchall()
        if len(db_options) == 0:
            return None

        options = []

        for temp_option in db_options:
            option = MultipleChoiceOption(
                o_id=temp_option[0], question_id=temp_option[1], idx=temp_option[2], content=temp_option[3]
            )
            options.append(option)

        return options

    @staticmethod
    def create(o_id, question_id, idx, content):
        db = get_db()
        db.execute(
            "INSERT INTO question_option (id, question_id, idx, content)"
            " VALUES (?, ?, ?, ?)",
            (o_id, question_id, idx, content),
        )
        db.commit()

class CorrectAnswer:
    def __init__(self, a_id, question_id, answer):
        self.id = a_id
        self.question_id = question_id
        self.answer = answer

    @staticmethod
    def get_by_question_id(question_id):
        # TODO change this to only have one return
        db = get_db()
        answer = db.execute(
            "SELECT * FROM correct_answer WHERE question_id = ?", (question_id,)
        ).fetchone()
        if not answer:
            return None

        answer = CorrectAnswer(
            a_id=answer[0], question_id=answer[1], answer=answer[2]
        )
        return answer

    @staticmethod
    def create(question_id, answer):
        db = get_db()
        db.execute(
            "INSERT INTO correct_answer (question_id, answer)"
            " VALUES (?, ?)",
            (question_id, answer),
        )
        db.commit()