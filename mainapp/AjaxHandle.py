# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
import json
import datetime, time

ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

class AjaxHandle():
    """docstring for AjaxHandle"""
    def __init__(self):
        pass