# coding:utf-8
from django.shortcuts import render, HttpResponse, redirect
import requests
from models import *
import random
import json
import re
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from datetime import datetime
# Create your views here.

# http://s.music.163.com/search/get/?type=1&limit=10&s=%E5%95%8A%E5%93%88%E5%93%88
# 获取歌曲详情 http://music.163.com/api/song/detail/?id=30953009&ids=%5B30953009%5D

@csrf_exempt
def city(request):
	if request.method == 'GET':
		s = request.GET.get('s', False)
		if not s:
			s = u'英文'
		payload = {
			'type': 1,
			'limit': 25,
			's': s
		}
		response = requests.post(url='http://music.163.com/api/search/get/', params=payload)
		data = response.json()
		for i in data['result']['songs']:
			print i
			print '-'*100

		data = {
			'songs': data['result']['songs'],
			'find_str': s
		}
		return render(request, 'city.html', data)
	elif request.method == 'POST':
		s = request.POST.get('s', False)
		if not s:
			s = u'英文'
		payload = {
			'type': 1,
			'limit': 100,
			's': s
		}
		response = requests.post(url='http://music.163.com/api/search/get/', params=payload)
		data = response.json()

		id_lst = []
		for i in data['result']['songs']:
			id_lst.append(i['id'])

		msg = {
			'id': random.choice(id_lst)
		}
		return HttpResponse(json.dumps(msg), content_type='application/json')


@csrf_exempt
def index(request):
	if request.method == 'POST':
		p_type = request.POST.get('to', False)
		if not p_type:
			return HttpResponse('error')
		username = request.POST.get('user', False)
		pw = request.POST.get('passwd', False)
		# pw2 = request.POST.get('passwd2', False)
		if p_type == 'reg':
			user = User.objects.create_user(username=username, password=pw)

		elif p_type == 'log':
			user = authenticate(username=username, password=pw)
			print '0'*20
			if not user:
				return redirect('/index')
		else:
			return redirect('/index')

		login(request, user)
		return redirect('/city')

	return render(request, 'index.html')


def sign_out(request):
	logout(request)
	return redirect('/city')


@csrf_exempt
@login_required(login_url='/index')
def operate(request):
	if request.method == 'POST':
		op_type = request.POST.get('type', False)
		m_id = request.POST.get('mid', False)
		msg = {
			'msg': '',
			'type': 'success'
		}
		if op_type == 'like':
			msg['msg'] = u'音乐已添加到<我喜爱的>列表'
		elif op_type == 'dislike':
			msg['msg'] = u'音乐已添加到垃圾桶，以后不会再被推荐'
		else:
			msg['msg'] = u'error!!!'
			msg['type'] = 'danger'
			return HttpResponse(json.dumps(msg), content_type='application/json')

		f_type = True if op_type == 'like' else False
		if not request.user.is_authenticated:
			msg['msg'] = u'登录后才能添加到列表'
			msg['type'] = 'danger'
		elif not op_type or not m_id:
			msg['msg'] = u'音乐源异常'
			msg['type'] = 'danger'
		music = Music.objects.filter(user=request.user, music_id=m_id)
		if music:
			music[0].type = f_type
			music[0].save()
		else:
			Music.objects.create(user=request.user, music_id=m_id, type=f_type)

		return HttpResponse(json.dumps(msg), content_type='application/json')


def list(request):
	like = Music.objects.filter(user=request.user, type=True)
	dislike = Music.objects.filter(user=request.user, type=False)
	data = {
		'like': like,
		'dislike': dislike
	}
	return render(request, 'list.html', data)