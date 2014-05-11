from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
import pprint
from apps.mainapp.classes.Questions import Questions
from django.conf import settings

def dashboard(request):
    return render_to_response('dashboard.html', context_instance=RequestContext(request))

def attempt_question(request):
    return render_to_response('qone-one.html',context_instance=RequestContext(request))

def landing(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/test/')
    return render_to_response('landing.html', context_instance=RequestContext(request))

def exam_sample(request):
    return render_to_response('exam.html', context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def add_question(request):
    parameters = {}
    parameters.update(csrf(request))
    if request.method == 'POST':
        data = {
        'subject':str(request.POST['subject']),
        'chapter':str(request.POST['chapter']),
        'question':str(request.POST['question']),
        'options':{
                'a':str(request.POST['opta']),
                'b':str(request.POST['optb']),
                'c':str(request.POST['optc']),
                'd':str(request.POST['optd'])
            },
        'ans':str(request.POST['correct']),
        'description':str(request.POST['description']),
        'difficulty':str(request.POST['difficulty']),
        'level':str(request.POST['level']), 
        'user':str(request.user.username)
        }
        #pprint.pprint(data)
        question_obj = Questions()
        question_obj.save_question(data)
        return HttpResponseRedirect('/')
    return render_to_response('questions-entry.html', context_instance=RequestContext(request))