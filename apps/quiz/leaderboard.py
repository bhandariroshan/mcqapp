from django.views.generic import View
from django.shortcuts import render
from .models import QuizResult
from apps.mainapp.classes.Userprofile import UserProfile
import datetime,time


class LeaderBoardView(View):
    """
    This class is used for leader board related operations
    """
    ioe_quiz_result = None
    ioe_total_score = None
    iom_quiz_result = None
    iom_total_score = None

    template_name = 'quiz/leaderboard.html'

    def get(self, request, *args, **kwargs):
        parameters = {}
        filter_type = request.GET.get('filter', 'week')
        if filter_type == 'all':
            parameters['ioe_result'], parameters['iom_result'] = self.user_quiz_result()
        else:
            parameters['ioe_result'], parameters['iom_result'] = self.week_quiz_result()
        return render(request, self.template_name, parameters)

    def week_quiz_result(self):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        # print type(start_week)
        # print start_week.strftime("%s")
        start_week_timestamp = int(time.mktime(start_week.timetuple()))
        end_week_timestamp = int(time.mktime(end_week.timetuple()))

        user_prof = UserProfile()
        all_users = QuizResult.objects.distinct('user_id')
        final_ioe_result = []
        final_iom_result = []
        for each_user in all_users:
            if int(each_user) in range(2, 8):
                continue
            else:
                quiz_user = user_prof.get_user_by_userid(int(each_user))
                quiz_types = QuizResult.objects.filter(
                    user_id=each_user).distinct('quiz_type')
                for each in quiz_types:
                    try:
                        data = {
                            'user_id': quiz_user.get('useruid'),
                            'name': quiz_user.get('name'),
                            'profile_img': "http://graph.facebook.com/" + quiz_user.get('id') + "/picture"
                        }
                    except:
                        continue
                    score = QuizResult.objects.filter(
                        user_id=each_user, quiz_type=each,
                        attempted_date__gte=start_week_timestamp
                    ).filter(
                        attempted_date__lte=end_week_timestamp
                    ).sum('quiz_score')
                    total_quiz = len(QuizResult.objects.filter(
                        user_id=each_user, quiz_type=each,
                        attempted_date__gte=start_week_timestamp
                    ).filter(
                        attempted_date__lte=end_week_timestamp
                    ))
                    data['total_score'] = format(score/float(total_quiz), '.2f')
                    data['total_quiz'] = int(total_quiz)
                    if each == 'MBBS-IOM':
                        final_iom_result.append(data)
                    if each == 'BE-IOE':
                        final_ioe_result.append(data)
        new_ioe_list = sorted(final_ioe_result, key=lambda k: k['total_score'], reverse=True)
        new_iom_list = sorted(final_iom_result, key=lambda k: k['total_score'], reverse=True)

        return new_ioe_list, new_iom_list

    def user_quiz_result(self):
        """
        The function receives the user id and provides the quiz information
        of the user
        """
        user_prof = UserProfile()
        all_users = QuizResult.objects.distinct('user_id')
        final_ioe_result = []
        final_iom_result = []
        for each_user in all_users:
            if int(each_user) in range(2, 8):
                continue
            else:
                quiz_user = user_prof.get_user_by_userid(int(each_user))
                quiz_types = QuizResult.objects.filter(
                    user_id=each_user).distinct('quiz_type')
                for each in quiz_types:
                    data = {
                        'user_id': quiz_user.get('useruid'),
                        'name': quiz_user.get('name'),
                        'profile_img': "http://graph.facebook.com/" + quiz_user.get('id') + "/picture"
                    }

                    score = QuizResult.objects.filter(
                        user_id=each_user, quiz_type=each).sum('quiz_score')
                    total_quiz = len(QuizResult.objects.filter(
                        user_id=each_user, quiz_type=each))
                    data['total_score'] = format(score/float(total_quiz), '.2f')
                    data['total_quiz'] = int(total_quiz)
                    if each == 'MBBS-IOM':
                        final_iom_result.append(data)
                    if each == 'BE-IOE':
                        final_ioe_result.append(data)
        new_ioe_list = sorted(final_ioe_result, key=lambda k: k['total_score'], reverse=True)
        new_iom_list = sorted(final_iom_result, key=lambda k: k['total_score'], reverse=True)

        return new_ioe_list, new_iom_list
