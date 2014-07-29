import random

from apps.mainapp.classes.query_database import QuestionApi


class GenerateQuiz():

    """
    This class is used to generate new quiz questions. Number of questions generated
    can change and vary for different exam types.
    """

    def generate_new_quiz(self, exam_type):
        """
        This function generates new set of quiz questions
        """
        question_api = QuestionApi()
        exam_type = exam_type.upper()
        subjects = question_api.find_distinct_value(
            "subject",
            {"exam_type": exam_type}
        )['results']
        NUMBER_OF_QUESTIONS = len(subjects) * 2
        question_list = []
        random_list = []
        for i in range(NUMBER_OF_QUESTIONS):
            subject_questions = question_api.find_all_questions(
                {"subject": subjects[i % len(subjects)],
                 "exam_type": exam_type},
                fields={"_id": 1}
            )
            random_num = random.randrange(len(subject_questions))
            while random_num in random_list:
                random_num = random.randrange(len(subject_questions))
            random_list.append(random_num)
            question_list.append(subject_questions[random_num])
        return question_list
