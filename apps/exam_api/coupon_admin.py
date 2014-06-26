from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from django.shortcuts import render_to_response
from django.template import RequestContext


def coupon_search(request):
    mycoupon = Coupon()
    parameters = {}
    if request.method == 'POST':
        code = request.POST.get('coupon')
        coupon_obj = mycoupon.get_coupon_by_coupon_code(code)
        userprofile = UserProfile()
        coupon_user = userprofile.get_user_by_coupon(code)
        print coupon_user
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
