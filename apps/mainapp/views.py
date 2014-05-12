from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


def dashboard(request):
    return render_to_response('dashboard.html',
                              context_instance=RequestContext(request))


def attempt_question(request):
    return render_to_response('qone-one.html',context_instance=RequestContext(request))


def landing(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/test/')
    return render_to_response('landing.html', context_instance=RequestContext(request))

def exam_sample(request):
    return render_to_response('exam.html', context_instance=RequestContext(request))
