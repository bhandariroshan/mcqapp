# from braces.views import SuperuserRequiredMixin, LoginRequiredMixin
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test, login_required

# class LatestUser(LoginRequiredMixin, SuperuserRequiredMixin, View):
@login_required(login_url='/')
@user_passes_test(lambda u: u.is_superuser)
def latest_users(request):
    parameters = {}
    count = request.GET.get('count', '100')
    all_users = User.objects.all().order_by('-date_joined')
    parameters['count'] = len(all_users)
    latest_users = []
    for each in all_users:
        try:
            social_obj = SocialAccount.objects.get(
                user=each
            )
            
            if each.first_name!= '':
                first_name = each.first_name
            elif social_obj.extra_data.get('first_name') is not None:
                first_name = social_obj.extra_data.get('first_name')
            else:
                first_name = ''

            if each.last_name!= '':
                last_name = each.last_name
            elif social_obj.extra_data.get('last_name') is not None:
                last_name = social_obj.extra_data.get('last_name')
            else:
                last_name = ''
            
            each_user = {
                'username': each.username,
                'first_name': first_name,
                'last_name': last_name,
                'email': each.email,
                'fb_url': social_obj.extra_data.get('link') if social_obj.extra_data.get('link') is not None else '',
                'date_joined': each.date_joined,
                'last_login': each.last_login
            }
            # each['fb_link'] = social_obj.extra_data['link']
            latest_users.append(each_user)
        except:
            pass
    parameters['latest_users'] = latest_users[:int(count)]
    return render_to_response(
        'latest_users.html',
        parameters, context_instance=RequestContext(request)
    )
