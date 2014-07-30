import datetime
import time
from bson.objectid import ObjectId

from .models import QuizAnswer


class SaveQuiz():
    """
    This class is used to save answers chosen by user in the
    QuizAnswer collection
    """

    def save_user_quiz(self, request, question_id, option):
        """
        This function receives the user information, question id and option
        chosen by user for the question and saves the data in the database
        """
        attempted_date = time.mktime(datetime.datetime.now().date().timetuple())
        quiz_answer_obj, created = QuizAnswer.objects.get_or_create(
            question_id=ObjectId(question_id),
            user_id=request.user.id,
            attempted_date=attempted_date,
            defaults={"attempted_option": option}
        )
        if not created:
            quiz_answer_obj.attempted_option = option
            quiz_answer_obj.save()
