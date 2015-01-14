from django.views.generic import View
from django.shortcuts import render
import datetime,time
from apps.mainapp.classes.Userprofile import UserProfile
# from apps.quiz.user_leaderboard import LeaderBoard
import datetime

class AnalyticsView(View):
    template_name = 'analytics.html'

    def get(self, request, *args, **kwargs):
        parameters = {}

        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)
        parameters['user'] = user

        leader_board = LeaderBoard()
        leader_board.user_quiz_result(request)

        if user['student_category'] == 'BE-IOE':
            parameters['ioe_user'] = True
        else:
            parameters['iom_user'] = True
        parameters['user'] = user
        parameters['IOE_score'] = "#".join([str(i.quiz_score) for i in leader_board.ioe_quiz_result])
        
        parameters['x_axis'] = "#".join([datetime.datetime.utcfromtimestamp(i.attempted_date).strftime('%m-%d-%Y') for i in leader_board.ioe_quiz_result])
        # print parameters['IOE_score']
        # print parameters['x-axis']
        # parameters['user_leaderboard'] = leader_board
        return render(request, self.template_name, parameters)