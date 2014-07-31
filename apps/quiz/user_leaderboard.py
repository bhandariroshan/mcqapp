class LeaderBoard():
    """
    This class is used for leader board related operations
    """

    def user_quiz_result(self, request):
        """
        The function receives the user id and provides the quiz information
        of the user
        """
        from django.contrib.auth.models import User
        from .models import QuizResult

        parameters = {}
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return False
        parameters['user'] = user
        parameters['quiz_result'] = QuizResult.objects.filter(
            user_id=user.id).order_by('exam_date')
        parameters['total_score'] = QuizResult.objects.filter(
            user_id=user.id).sum('exam_score')
        return parameters
