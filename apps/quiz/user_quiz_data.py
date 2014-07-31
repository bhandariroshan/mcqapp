import datetime
import time
from bson.objectid import ObjectId

from .models import QuizAnswer


class SaveQuiz():
    """
    This class is used to perform save related operations of quiz
    """

    def save_user_quiz(self, request):
        """
        This function receives the user information, question id and option
        chosen by user for the question and saves the data in the database
        """

        question_id = request.POST.get('question_id')
        option = request.POST.get('option')
        exam_code = int(request.POST.get('exam_code'))
        attempted_date = time.mktime(datetime.datetime.now().date().timetuple())
        quiz_answer_obj, created = QuizAnswer.objects.get_or_create(
            question_id=ObjectId(question_id),
            user_id=request.user.id,
            attempted_date=attempted_date,
            defaults={"attempted_option": option, "exam_code": exam_code}
        )
        if not created:
            quiz_answer_obj.attempted_option = option
            quiz_answer_obj.save()
            return True

    def save_daily_quiz_score(self, request):
        """
        This function receives user information and exam code
        and returns the score of the user for daily quiz.
        """
        from apps.mainapp.classes.query_database import QuestionApi, ExammodelApi
        from .models import QuizResult

        exam_code = int(request.POST.get('exam_code'))
        quiz_answer_obj = QuizAnswer.objects(
            exam_code=exam_code,
            user_id=request.user.id
        )
        question_api = QuestionApi()
        daily_score = 0
        for quiz_objects in quiz_answer_obj:
            question = question_api.find_one_question(
                {"_id": quiz_objects.question_id},
            )
            if question['answer']['correct'] == quiz_objects.attempted_option:
                daily_score += 1
        exam_model_obj = ExammodelApi()
        current_exam_model = exam_model_obj.find_one_exammodel(
            {"exam_code": exam_code}
        )
        exam_name = current_exam_model['exam_name']
        quiz_number = current_exam_model['quiz_number']
        quiz_result_obj = QuizResult(
            quiz_code=exam_code,
            attempted_date=quiz_answer_obj[0].attempted_date,
            quiz_type=current_exam_model['exam_category']
        )
        quiz_result_obj.quiz_name = ' '.join([exam_name, str(quiz_number)])
        quiz_result_obj.user_id = request.user.id
        quiz_result_obj.quiz_score = daily_score
        quiz_result_obj.submitted = True
        quiz_result_obj.save()
        return True

    def check_quiz_submitted(self, request, exam_code):
        """
        This functions checks whether quiz is submitted by the user
        and return true if submitted else returns false
        """
        from .models import QuizResult
        return QuizResult.objects.filter(
            exam_code=exam_code, user_id=request.user.id
        ).count() > 0
