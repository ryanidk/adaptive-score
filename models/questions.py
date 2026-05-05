"""
Questions classes: Question, Multiple choice answer, Correct answer
ICS3U-01
Ryan
This file represents the question, multiple choice answer, and correct answer classes that are referred to in the app.
Last modified: May 5, 2026
"""

# Import database class
from db import get_db


# The classes themselves
class Question:
    """
    This class represents a Question object. Each question is its individual object.

    Attributes:
        id (str): The ID of the question
        college_board_id (str): The college board ID, or external id, of the question
        section (str): The section, either "english" or "math"
        type (str): Either "mcq" (multiple-choice) or "spr" (student-produced response)
        skill (str): Short-handed skill, i.e. "WIC"
        skill_description (str): Skill description, i.e. "Words in Context"
        difficulty (str): The difficulty, either "E", "M", or "H"
        stimulus (str): CAN BE NONE. Stimulus for english questions - usually the passage
        stem (str): Usually the question itself
        rationale (str): The rationale for the answer.
    """

    def __init__(self, q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem,
                 rationale):
        """
        Initializes attributes for the Question class.

        Args:
            q_id (str): The ID of the question
            college_board_id (str): The college board ID, or external id, of the question
            section (str): The section, either "english" or "math"
            q_type (str): Either "mcq" (multiple-choice) or "spr" (student-produced response)
            skill (str): Short-handed skill, i.e. "WIC"
            skill_description (str): Skill description, i.e. "Words in Context"
            difficulty (str): The difficulty, either "E", "M", or "H"
            stimulus (str): CAN BE NONE. Stimulus for english questions - usually the passage
            stem (str): Usually the question itself
            rationale (str): The rationale for the answer.
        """

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
        """
        Static method: Gets a question by question ID.

        Args:
            question_id (str): The question ID to fetch

        Returns:
            question (Question): The question object, can be None.
        """

        # Get the database
        db = get_db()

        # Fetch the question from the database by ID
        question = db.execute(
            "SELECT * FROM question WHERE id = ?", (question_id,)
        ).fetchone()

        # Only create the question object if the question exists. If not, it will just be none.
        if question:
            question = Question(
                q_id=question[0], college_board_id=question[1], section=question[2], q_type=question[3],
                skill=question[4], skill_description=question[5], difficulty=question[6], stimulus=question[7],
                stem=question[8], rationale=question[9]
            )
        else:
            # We are explicitly saying that it is None just in case.
            question = None

        return question

    @staticmethod
    def get_by_skill_and_difficulty(skill, difficulty):
        """
        Static method: Gets a question by skill and difficulty.

        Args:
            skill (str): The skill category, i.e. "WIC"
            difficulty (str): The difficulty, either "E", "M", or "H"

        Returns:
            question (Question): The question object found, can be None.
        """

        # Get the database
        db = get_db()

        # Fetch the question from the database by skill and difficulty
        question = db.execute(
            "SELECT * FROM question WHERE skill = ? AND difficulty = ? ORDER BY RANDOM() LIMIT 1", (skill, difficulty)
        ).fetchone()

        # Only create the question object if the question exists. If not, it will just be none.
        if question:
            question = Question(
                q_id=question[0], college_board_id=question[1], section=question[2], q_type=question[3],
                skill=question[4], skill_description=question[5], difficulty=question[6], stimulus=question[7],
                stem=question[8], rationale=question[9]
            )
        else:
            # Try again with a different difficulty
            new_question = db.execute(
                "SELECT * FROM question WHERE skill = ? ORDER BY RANDOM() LIMIT 1",
                (skill,)
            ).fetchone()

            # If there's a new question try with the new difficulty
            if new_question:
                question = Question(
                    q_id=new_question[0], college_board_id=new_question[1], section=new_question[2],
                    q_type=new_question[3],
                    skill=new_question[4], skill_description=new_question[5], difficulty=new_question[6],
                    stimulus=new_question[7],
                    stem=new_question[8], rationale=new_question[9]
                )
            else:
                # We are explicitly saying that it is None just in case.
                question = None

        return question

    @staticmethod
    def create(q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem,
               rationale):
        """
        Static method: Creates a question to be inserted into the database.

        Args:
            q_id (str): The ID of the question
            college_board_id (str): The college board ID, or external id, of the question
            section (str): The section, either "english" or "math"
            q_type (str): Either "mcq" (multiple-choice) or "spr" (student-produced response)
            skill (str): Short-handed skill, i.e. "WIC"
            skill_description (str): Skill description, i.e. "Words in Context"
            difficulty (str): The difficulty, either "E", "M", or "H"
            stimulus (str): CAN BE NONE. Stimulus for english questions - usually the passage
            stem (str): Usually the question itself
            rationale (str): The rationale for the answer.
        """

        # Load the database
        db = get_db()

        # Add the value
        db.execute(
            "INSERT INTO question (id, college_board_id, section, type, skill, skill_description, difficulty, stimulus, stem, rationale)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (q_id, college_board_id, section, q_type, skill, skill_description, difficulty, stimulus, stem, rationale),
        )

        # Commit to the database
        db.commit()


class MultipleChoiceOption:
    """
    This class represents a MultipleChoiceOption object. Each option is its individual object, so there are 4 per question.

    Attributes:
        id (str): The ID of the option
        question_id (str): The ID of the question
        idx (int): The index of the answer. 0=A, 1=B, 2=C, 3=D
        content (str): The content of the answer
    """

    def __init__(self, o_id, question_id, idx, content):
        """
        Initializes attributes for the MultipleChoiceOption class.

        Args:
            o_id (str): The ID of the option
            question_id (str): The ID of the question
            idx (int): The index of the answer. 0=A, 1=B, 2=C, 3=D
            content (str): The content of the answer
        """

        self.id = o_id
        self.question_id = question_id
        self.idx = idx
        self.content = content

    @staticmethod
    def get_by_option_id(option_id):
        """
        Static method: Gets an option by option ID.

        Args:
            option_id (str): The option ID to fetch

        Returns:
            option (MultipleChoiceOption): The object of the multiple choice option.
        """

        # Fetch the database
        db = get_db()

        # Fetch the question based on option ID
        option = db.execute(
            "SELECT * FROM question_option WHERE id = ?", (option_id,)
        ).fetchone()

        # Only create the option object if the question exists. If not, it will just be none.
        if option:
            option = MultipleChoiceOption(
                o_id=option[0], question_id=option[1], idx=option[2], content=option[3]
            )
        else:
            # We are explicitly saying that it is None just in case.
            option = None

        return option

    @staticmethod
    def get_options_by_question_id(question_id):
        """
        Static method: Gets a list of multiple choice options based on question IDs.

        Args:
            question_id (str): The question ID to fetch the options for

        Returns:
            options (list[MultipleChoiceOption]): A list of options for the question. Can be an empty list.
        """

        # Fetch the database
        db = get_db()

        # Fetch the multiple options from the database that match the question ID.
        db_options = db.execute(
            "SELECT * FROM question_option WHERE question_id = ?", (question_id,)
        ).fetchall()

        options = []

        # Iterate over the options in the database and create a new MultipleChoiceOption for each one.
        for temp_option in db_options:
            option = MultipleChoiceOption(
                o_id=temp_option[0], question_id=temp_option[1], idx=temp_option[2], content=temp_option[3]
            )

            options.append(option)

        return options

    @staticmethod
    def create(o_id, question_id, idx, content):
        """
        Static method: Creates a multiple choice option.

        Args:
            o_id (str): The ID of the option
            question_id (str): The ID of the question
            idx (int): The index of the answer. 0=A, 1=B, 2=C, 3=D
            content (str): The content of the answer
        """

        # Fetch the database
        db = get_db()

        # Add a question option to the database
        db.execute(
            "INSERT INTO question_option (id, question_id, idx, content)"
            " VALUES (?, ?, ?, ?)",
            (o_id, question_id, idx, content),
        )

        # Commit it to the database
        db.commit()


class CorrectAnswer:
    """
    This class represents a CorrectAnswer object. Each question is associated with an object.

    Attributes:
        id (int): The ID of the correct answer; it automatically increments
        question_id (str): The ID of the question
        answer (str): The correct answer. i.e., 6.5, A, C, 5/3
    """

    def __init__(self, a_id, question_id, answer):
        """
        Initializes a correct answer object.

        Args:
            a_id (int): The ID of the correct answer; it automatically increments
            question_id (str): The ID of the question
            answer (str): The correct answer. i.e., 6.5, A, C, 5/3
        """

        self.id = a_id
        self.question_id = question_id
        self.answer = answer

    @staticmethod
    def get_by_question_id(question_id):
        """
        Static method: Gets a list of correct answer objects based on question id.

        Args:
            question_id (str): The question ID

        Returns:
            answers (list[CorrectAnswer]): A list of correct answer objects. Can be empty.
        """

        # Fetch the database
        db = get_db()

        # Fetch all the correct answers from the answers database
        answers_db = db.execute(
            "SELECT * FROM correct_answer WHERE question_id = ?", (question_id,)
        ).fetchall()

        answers = []

        # Iterate over each answer and create an object to be appended to the list of answers.
        for temp_answer in answers_db:
            answer = CorrectAnswer(
                a_id=temp_answer[0], question_id=temp_answer[1], answer=temp_answer[2]
            )
            answers.append(answer)

        return answers

    @staticmethod
    def create(question_id, answer):
        """
        Static method: Creates an answer in the database.

        Args:
            question_id (str): The question ID
            answer (str): The answer. Can be i.e., A, 0.5, 1/2, C, etc.
        """

        # Fetch the database
        db = get_db()

        # Add the answer to the database
        db.execute(
            "INSERT INTO correct_answer (question_id, answer)"
            " VALUES (?, ?)",
            (question_id, answer),
        )

        # Commit to the database
        db.commit()
