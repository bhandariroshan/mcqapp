from django.views.decorators.csrf import csrf_exempt

from apps.mainapp.classes.AjaxHandle import AjaxHandle


@csrf_exempt
def ajax_request(request, func_name):
    ajax_handle = AjaxHandle()
    return_msg = getattr(ajax_handle, func_name)(request)
    return return_msg
