import datetime
import time
from bson.objectid import ObjectId

from .models import QuizAnswer


class SaveQuiz():
    """
    This class is used to save answers chosen by user in the
    QuizAnswer collection
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


class QuizResult():
    """
    This class is used for result related queries of of quiz
    """

    def user_quiz_result(self, request):
        """
        This function receives user information and exam code
        and returns the result of the quiz for that quiz.
        """

        exam_code = int(request.POST.get('exam_code'))
        user_quiz_answers = QuizAnswer.objects(
            exam_code=exam_code,
            user_id=request.user.id
        )
