import random
import datetime
import time

from bson.objectid import ObjectId

from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi

from .decorators import check_quiz_generated


class GenerateQuiz():
    """
    This class is used to generate new quiz questions. Number of questions generated
    can change and vary for different exam types.
    """
    exam_model = None
    question_list = None

    @check_quiz_generated
    def generate_new_quiz(self, exam_type):
        """
        This function generates new set of quiz questions and saves the
        question list in the exammodel collection
        """
        exam_date = time.mktime(datetime.datetime.now().date().timetuple())
        exammodel_api = ExammodelApi()
        question_api = QuestionApi()
        exam_type = exam_type.upper()
        subjects = question_api.find_distinct_value(
            "subject",
            {"exam_type": exam_type}
        )['results']
        if exam_type == "ENGINEERING":
            exam_category = "BE-IOE"
            exam_name = "Meroanswer IOE Daily Quiz"
            subjects.remove("english")
            marks = 2

        elif exam_type == "MEDICAL":
            exam_category = "MBBS-IOM"
            exam_name = "Meroanswer IOM Daily Quiz"
            marks = 1

        latest_exam_models = exammodel_api.find_all_exammodel_descending(
            {"exam_family": "QUIZ", "exam_category": exam_category},
            fields={"quiz_number": 1, "question_list": 1},
            sort_index="quiz_number",
            limit=2
        )
        if len(latest_exam_models) > 0:
            quiz_number = int(latest_exam_models[0]['quiz_number']) + 1
        else:
            quiz_number = 1

        NUMBER_OF_QUESTIONS = len(subjects) * 2
        question_list = []
        random_list = []
        for i in range(NUMBER_OF_QUESTIONS):
            subject_questions = question_api.find_all_questions(
                {"subject": subjects[i % len(subjects)],
                 "exam_type": exam_type,
                 "marks": marks},
                fields={"_id": 1}
            )
            random_num = random.randrange(len(subject_questions))

            # generate unique random numbers to avoid repetition
            while random_num in random_list:
                random_num = random.randrange(len(subject_questions))
            random_list.append(random_num)
            question_id = subject_questions[random_num]['uid']

            while question_id in (
                latest_exam_models[0]['question_list'] or latest_exam_models[1]['question_list']
            ):
                # generate unique random numbers to avoid repetition
                while random_num in random_list:
                    random_num = random.randrange(len(subject_questions))
                random_list.append(random_num)
                question_id = subject_questions[random_num]['uid']

            question_list.append(ObjectId(question_id['id']))

        # insert the newly generated questions into exammodel collection
        # with exam code incremented by one

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

        new_exam_model = {
            "exam_name": exam_name,
            "exam_date": exam_date,
            "image": "exam.jpg",
            "exam_code": new_exam_code,
            "exam_category": exam_category,
            "exam_family": "QUIZ",
            "quiz_number": quiz_number,
            "question_list": question_list
        }
        exammodel_api.insert_new_model(new_exam_model)
        return True

    def return_quiz_questions(self, exam_category):
        """
        This function receives the exam_date and exam_category parameters and
        returns the quiz question list for that exam.
        """
        exam_category = exam_category.upper()
        exam_date = time.mktime(datetime.datetime.now().date().timetuple())
        exammodel_api = ExammodelApi()
        self.exam_model = exammodel_api.find_one_exammodel(
            {"exam_family": "QUIZ",
             "exam_date": exam_date,
             "exam_category": exam_category}
        )
        question_id_list = [
            ObjectId(i['id']) for i in self.exam_model['question_list']
        ]
        question_api = QuestionApi()
        self.question_list = question_api.find_all_questions(
            {
                '_id': {"$in": question_id_list}
            },
            fields={'answer.correct': 0, 'question_number': 0}
        )
        for count, eachQuestion in enumerate(self.question_list):
            eachQuestion['question_number'] = count + 1
        return True
