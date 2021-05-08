# -*- coding:utf-8 -*-
from django.http import JsonResponse
from BookRec.settings import USER
from indexbook.models import Cate, History, Book
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import time
import joblib
import numpy as np

"""
返回 用户和类别
"""


@csrf_exempt
def login(request):
    if request.method == 'GET':
        users = USER
        tags = Cate.objects.all()
        return JsonResponse({'code': 1, 'data': {'users': users, 'tags': [tag.name for tag in tags]}})
    else:
        # 将用户信息写入session
        request.session['username'] = request.POST.get('username')
        request.session['tags'] = request.POST.get('tags')
        write_to_mysql(name=request.POST.get('username'), time=format_local_time(), action='登录', object='系统', tag='')
        return JsonResponse({'code': 1, 'data': {'username': request.POST.get('username'), 'tags': request.POST.get('tags')}})


# 行为信息写入表
def write_to_mysql(name='', time='', action='', object='', tag=''):
    History(name=name, time=time, action=action, object=object, tag=tag).save()
    print('{}在{}{}{},{},写入数据库！'.format(name, time, action, object, tag))


# 获取当前格式化的系统时间
def format_local_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
