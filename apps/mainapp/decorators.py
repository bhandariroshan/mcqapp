from django.http import HttpResponseRedirect

from .classes.Userprofile import UserProfile


def user_authenticated_and_subscribed_required(view_func):
    '''
    Condition 1: if user is not authenticated redirect to login page
    Condition 2: if user is not subscribed for the exam then redirect
                 to home page
    '''

    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/accounts/login/?next=" +
                                        request.get_full_path())
        user_profile_obj = UserProfile()
        user = user_profile_obj.get_user_by_username(request.user.username)

        if int(kwargs['exam_code']) not in user['valid_exam']:
            return HttpResponseRedirect("/")

        return view_func(request, *args, **kwargs)

    return _wrapped_view_func
