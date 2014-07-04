from apps.mainapp.classes.Coupon import Coupon
from apps.mainapp.classes.Userprofile import UserProfile
from apps.mainapp.classes.Exams import Exam
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
    return render_to_response('superuser/subscribe_to_exam.html', parameters, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def paying_users(request):
    profiles = UserProfile()
    mycoupon = Coupon()
    myexam = Exam()
    parameters = {}
    paying_users = []
    if request.method == 'POST':
        query = request.POST.get('username')
        users_result = profiles.search_user(query)
        
    else:
        users_result = profiles.get_all_users()
    for each_user in users_result:
        user_details = {
            'username': each_user.get('username'),
            'email': each_user.get('email'),
            'first_name': each_user.get('first_name'),
            'last_name': each_user.get('last_name'),
            'subscription_type': ' , '.join(each_user.get('subscription_type')),
            'total_coupons': len(each_user.get('coupons'))
        }
        coupon_count = {}
        price = 0
        if 'BE-IOE' in each_user.get('subscription_type'):
            if len(each_user.get('subscription_type')) == 1:
                coupon_count['BE-IOE'] = 1
            else:
                if 'MBBS-IOM' in each_user.get('subscription_type'):
                    coupon_count['MBBS-IOM'] = 1

        elif 'MBBS-IOM' in each_user.get('subscription_type'):
            if len(each_user.get('subscription_type')) == 1:
                coupon_count['MBBS-IOM'] = 1
            else:
                if 'BE-IOE' in each_user.get('subscription_type'):
                    coupon_count['BE-IOE'] = 1
        else:
            if len(each_user.get('subscription_type')) != 0:
                valid_exams = each_user.get('valid_exam')
                if len(valid_exams) !=0:
                    for each_exam in valid_exams:
                        print each_exam
                        try:
                            exam_det = myexam.get_exam_detail(int(each_exam))
                            print ('exam_det: {0}').format(exam_det)
                            exam_family = exam_det.get('exam_family')
                            exam_category = exam_det.get('exam_category')
                            new_type = exam_family + "-" + exam_category
                            coupon_count[new_type] = coupon_count.get(new_type, 1) + 1
                        except:
                            pass
        user_details['coupon_count'] = coupon_count
        # for each_coupon in each_user.get('coupons'):
        #     one_coupon = mycoupon.get_coupon_by_coupon_code(each_coupon)
        #     subscription_type = one_coupon.get('subscription_type')
        #     coupon_count[subscription_type] = coupon_count.get(subscription_type, 0) + 1

        print ('coupon_count for {0}: {1}').format(each_user.get('username'), coupon_count)
        paying_users.append(user_details)
    parameters['users_result'] = paying_users
    return render_to_response('superuser/paying_users.html', parameters, context_instance=RequestContext(request))
