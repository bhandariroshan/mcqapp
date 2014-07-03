from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import Q


@user_passes_test(lambda u: u.is_superuser)
def coupon_search(request):
    mycoupon = Coupon()
    parameters = {}
    if request.method == 'POST':
        code = request.POST.get('coupon')
        coupon_obj = mycoupon.get_coupon_by_coupon_code(code)
        userprofile = UserProfile()
        coupon_user = userprofile.get_user_by_coupon(code)
        if coupon_user is not None:
            user_details = {
                'name': coupon_user.get('name'),
                'username': coupon_user.get('username'),
                'fb_link': 'https://facebook.com/'+ coupon_user.get('link').split('/')[-2]

            }
        else:
            user_details = ''
        parameters['coupon_user'] = user_details
        parameters['coupon'] = coupon_obj
    else:
        parameters['coupon'] = ''
    return render_to_response("coupon_admin.html", parameters, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def subscribe_user_to_exam(request):
    mycoupon = Coupon()
    parameters = {}
    if request.method == 'POST':
        query = request.POST.get('username')
        users_result = User.objects.filter(
            Q(username__contains=query) | Q(email__contains=query)
        )
        # for each in users_result:
        #     print each
        parameters['users_result'] = users_result
    return render_to_response('subscribe_to_exam.html', parameters, context_instance=RequestContext(request))
