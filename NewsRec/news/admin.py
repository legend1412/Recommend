# -*- coding:utf-8 -*-
from django.contrib import admin
from news.models import News, Cate, Newsim, Newhot, Newtag, Newbrowse


class AdminNews(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('new_title', 'new_id', 'new_seenum', 'new_time', 'new_cate')
    # 添加search bar，在指定的字段中search
    search_fields = ('new_title', 'new_time', 'new_cate')
    # 页面右边会出现对应的过滤器选项
    list_filter = ('new_time', 'new_cate')
    # 排序
    ordering = ('-new_time',)


admin.site.register(News, AdminNews)


class AdminCate(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('cate_id', 'cate_name')
    # 添加search bar，在指定的字段中search
    search_fields = ('cate_id', 'cate_name')
    # 页面右边会出现相应的过滤器选项
    list_filter = ('cate_name',)


admin.site.register(Cate, AdminCate)


class AdminNewSim(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('new_id_base', 'new_id_sim', 'new_correlation')
    # 添加search bar，在指定字段中search
    search_fields = ('new_id_base', 'new_id_sim', 'new_correlation')
    # 页面右边出现相应的过滤器选项
    # list_filter = ('cate_name',)


admin.site.register(Newsim, AdminNewSim)


class AdminNewHot(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('new_id', 'new_cate', 'new_hot')
    # 添加search bar，在指定字段中search
    search_fields = ('new_id', 'new_cate', 'new_hot')


admin.site.register(Newhot, AdminNewHot)


class AdminNewTag(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('new_tag', 'new_id', 'new_hot')
    # 添加search bar，在指定字段中search
    search_fields = ('new_tag', 'new_id', 'new_hot')


admin.site.register(Newtag, AdminNewTag)


class AdminNewBrowse(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ('user_name', 'new_id', 'new_browse_time')
    # 添加search bar，在指定字段中search
    search_fields = ('user_name', 'new_id', 'new_browse_time')
    # 页面右边会出现相应的过滤器选项
    list_filter = ('user_name',)


admin.site.register(Newbrowse, AdminNewBrowse)
