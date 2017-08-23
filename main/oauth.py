import oauth2 as oauth
import requests
import json
import re

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .models import User

request_token_url = 'https://github.com/login/oauth/authorize'
access_token_url = 'https://github.com/login/oauth/access_token'
authenticate_url = 'https://api.github.com/user'

def github_login(request):
    
    url = "%s?client_id=%s" % (request_token_url, settings.CLIENT_ID)

    return HttpResponseRedirect(url)

def github_callback(request):
    data = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': request.GET['code']
    }
    back = requests.post(access_token_url, data=data).text

    access_token = re.match('^access_token=(\w+)&', back).group(1)
    userinfo = requests.get(authenticate_url+'?access_token='+access_token).text
    userinfo = json.loads(str(userinfo))
    github_name = userinfo['login']

    user = request.user.username
    qu = User.objects.filter(student_id=user).update(github=github_name)

    return HttpResponseRedirect('/home/myinfo/')