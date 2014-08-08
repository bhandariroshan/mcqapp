class LeaderBoard():
    """
    This class is used for leader board related operations
    """
    ioe_quiz_result = None
    ioe_total_score = None
    iom_quiz_result = None
    iom_total_score = None

    def user_quiz_result(self, request):
        """
        The function receives the user id and provides the quiz information
        of the user
        """
        from django.contrib.auth.models import User
        from .models import QuizResult

        try:
            user = User.objects.get(id=request.user.id)
        except:
            return False
        self.ioe_quiz_result = QuizResult.objects.filter(
            user_id=user.id, quiz_type="BE-IOE").order_by('-attempted_date')
        self.ioe_total_score = QuizResult.objects.filter(
            user_id=user.id, quiz_type="BE-IOE").sum('quiz_score')
        self.iom_quiz_result = QuizResult.objects.filter(
            user_id=user.id, quiz_type="MBBS-IOM").order_by('-attempted_date')
        self.iom_total_score = QuizResult.objects.filter(
            user_id=user.id, quiz_type="MBBS-IOM").sum('quiz_score')

        return True
