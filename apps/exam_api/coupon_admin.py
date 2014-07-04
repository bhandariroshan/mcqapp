from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
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
                'fb_link': 'https://facebook.com/' +
                coupon_user.get('link').split('/')[-2]

            }
        else:
            user_details = ''
        parameters['coupon_user'] = user_details
        parameters['coupon'] = coupon_obj
    else:
        parameters['coupon'] = ''
    return render_to_response(
        "coupon_admin.html",
        parameters,
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def subscribe_user_to_exam(request):
    parameters = {}
    if request.method == 'POST':
        query = request.POST.get('username')
        users_result = User.objects.filter(
            Q(username__contains=query) | Q(email__contains=query)
        )

        parameters['users_result'] = users_result
    return render_to_response(
        'superuser/subscribe_to_exam.html',
        parameters,
        context_instance=RequestContext(request)
    )


@user_passes_test(lambda u: u.is_superuser)
def paying_users(request):
    profiles = UserProfile()
    mycoupon = Coupon()
    parameters = {}
    paying_users = []
    if request.method == 'POST':
        query = request.POST.get('username')
        users_result = profiles.search_user(query)

    else:
        users_result = profiles.get_all_users(limit=1000)
    for each_user in users_result:
        user_details = {
            'username': each_user.get('username'),
            'email': each_user.get('email'),
            'first_name': each_user.get('first_name'),
            'last_name': each_user.get('last_name'),
        }
        coupon_count = {}
        subscription_type = 'IDP'
        if 'BE-IOE' in each_user.get('subscription_type'):
            if len(each_user.get('subscription_type')) == 1:
                subscription_type = 'BE-IOE'
            else:
                if 'MBBS-IOM' in each_user.get('subscription_type'):
                    subscription_type = 'both'

        elif 'MBBS-IOM' in each_user.get('subscription_type'):
            if len(each_user.get('subscription_type')) == 1:
                subscription_type = 'MBBS-IOM'
            else:
                if 'BE-IOE' in each_user.get('subscription_type'):
                    subscription_type = 'both'

        if len(each_user.get('subscription_type')) != 0:
            #coupons
            for each_coupon in each_user.get('coupons'):
                try:
                    one_coupon = mycoupon.get_coupon_by_coupon_code(
                        each_coupon)
                    exam_type = one_coupon.get('subscription_type')
                    if exam_type == 'BE-IOE' and one_coupon.get('serial_no') \
                            is not None:
                        exam_type = exam_type + '(discount)'
                    new_type = subscription_type + "/" + exam_type
                    coupon_count[new_type] = coupon_count.get(new_type, 0) + 1
                except:
                    pass

        user_details['coupon_count'] = ' ; '.join(
            [key + ' - ' + str(value)
                for key, value in coupon_count.iteritems()]
        )
        total_coupons = 0
        coupon_price = {
            'BE-IOE/DPS': 30,
            'BE-IOE/CPS': 30,
            'BE-IOE/BE-IOE': 500,
            'BE-IOE/BE-IOE(discount)': 250,
            'MBBS-IOM/DPS': 20,
            'MBBS-IOM/CPS': 20,
            'MBBS-IOM/MBBS-IOM': 300
        }
        price = 0
        for key, value in coupon_count.iteritems():
            total_coupons += value
            price += coupon_price[key] * value

        user_details['total_coupons'] = total_coupons
        user_details['price'] = price
        if price != 0 or request.method == 'POST':
            paying_users.append(user_details)
    parameters['users_result'] = paying_users
    parameters['users_result'] = sorted(paying_users, key=getKey, reverse=True)
    return render_to_response(
        'superuser/paying_users.html',
        parameters,
        context_instance=RequestContext(request)
    )


def getKey(item):
    return item['price']
