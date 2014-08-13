#!/usr/bin/env python
# encoding: utf-8
from allauth.socialaccount.models import SocialAccount
from apps.mainapp.classes.Userprofile import UserProfile


def user_info(request):
    if request.user.is_authenticated():
        parameters = {}
        try:
            social_obj = SocialAccount.objects.filter(
                user__id=request.user.id
            )
            user_profile_obj = UserProfile()
            user = user_profile_obj.get_user_by_username(request.user.username)
            parameters.update(
                {
                    "profile_img_url": social_obj[0].get_avatar_url(),
                    'user': user
                }
            )
            return parameters
        except:
            return {}
    else:
        return {}
