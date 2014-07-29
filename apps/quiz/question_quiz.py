import random
import datetime

from bson.objectid import ObjectId

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi


class GenerateQuiz():

    """
    This class is used to generate new quiz questions. Number of questions generated
    can change and vary for different exam types.
    """

    def generate_new_quiz(self, exam_type):
        """
        This function generates new set of quiz questions and saves the
        question list in the exammodel collection
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

            # generate unique random numbers to avoid repetition
            while random_num in random_list:
                random_num = random.randrange(len(subject_questions))
            random_list.append(random_num)
            question_list.append(ObjectId(subject_questions[random_num]['uid']['id']))

        # insert the newly generated questions into exammodel collection
        # with exam code incremented by one
        exammodel_api = ExammodelApi()
        last_exam_code = exammodel_api.find_all_exammodel_descending(
            {},
            fields={"exam_code": 1},
            sort_index="exam_code",
            limit=1
        )
        if len(last_exam_code) > 0:
            new_exam_code = int(last_exam_code[0]['exam_code']) + 1
        else:
            new_exam_code = 1001
        if exam_type == "ENGINEERING":
            exam_category = "BE-IOE"
        elif exam_type == "MEDICAL":
            exam_category = "MBBS-IOM"

        new_exam_model = {
            "exam_name": "Meroanswer Daily Quiz",
            "exam_date": str(datetime.datetime.utcnow().date()),
            "image": "exam.jpg",
            "exam_code": new_exam_code,
            "exam_category": exam_category,
            "exam_family": "QUIZ",
            "question_list": question_list
        }
        exammodel_api.insert_new_model(new_exam_model)
        return new_exam_model

    def return_quiz_questions(self, exam_category):
        """
        This function receives the exam_date and exam_category parameters and
        returns the quiz question list for that exam.
        """
        exam_category = exam_category.upper()
        exam_date = str(datetime.datetime.utcnow().date())
        exammodel_api = ExammodelApi()
        exam_model = exammodel_api.find_one_exammodel(
            {"exam_family": "QUIZ",
             "exam_date": exam_date,
             "exam_category": exam_category}
        )
        question_id_list = [
            ObjectId(i['id']) for i in exam_model['question_list']
        ]
        question_api = QuestionApi()
        question_list = question_api.find_all_questions(
            {
                '_id': {"$in": question_id_list}
            },
            fields={'answer.correct': 0}
        )
        sorted_questions = sorted(
            question_list, key=lambda k: k['question_number'])
        return sorted_questions
