from django.shortcuts import render
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy



class QuizView(View):   
    template_name = 'exam_main.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuizView, self).get_context_data(**kwargs)
        return context

    # @method_decorator(login_required(login_url=reverse_lazy('home_page')))
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class SingleQuizView(View):   
    template_name = 'exam_main.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuizView, self).get_context_data(**kwargs)
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
