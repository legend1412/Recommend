# -*- coding:utf-8 -*-
from django.contrib import admin
from index.models import Cate


class AdminCate(admin.ModelAdmin):
    # 将全部字段显示出来
    list_display = ('cate_id', 'cate_name')
    # 添加search bar 在指定的字段中search
    search_fields = ('cate_id', 'cate_name')
    # 页面右边会出现相应的过滤器选项
    list_filter = ('cate_id', 'cate_name')


admin.site.register(Cate, AdminCate)
