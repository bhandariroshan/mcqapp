from apps.mainapp.classes.AjaxHandle import AjaxHandle
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

@csrf_exempt
def ajax_request(request, func_name):
    ajax_handle = AjaxHandle()
    return_msg = getattr(ajax_handle,func_name)(request)
    return return_msg

    