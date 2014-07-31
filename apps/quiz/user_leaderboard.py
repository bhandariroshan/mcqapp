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
        parameters['ioe_quiz_result'] = QuizResult.objects.filter(
            user_id=user.id, quiz_type="BE-IOE").order_by('attempted_date')
        parameters['ioe_total_score'] = QuizResult.objects.filter(
            user_id=user.id, quiz_type="BE-IOE").sum('quiz_score')
        parameters['iom_quiz_result'] = QuizResult.objects.filter(
            user_id=user.id, quiz_type="MBBS-IOM").order_by('attempted_date')
        parameters['ioe_total_score'] = QuizResult.objects.filter(
            user_id=user.id, quiz_type="MBBS-IOM").sum('quiz_score')
        return parameters
