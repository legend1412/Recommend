# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from index.models import Cate
from user.models import User,UserBrowse
from song.models import Song
from sing.models import Sing
from playlist.models import PlayList



# Create your views here.
