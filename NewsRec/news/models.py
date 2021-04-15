# -*- coding:utf-8 -*-
from django.db import models


# 新闻类别表
class Cate(models.Model):
    id = models.AutoField(primary_key=True)
    cate_id = models.CharField(blank=False, max_length=64, verbose_name='ID', unique=True)
    cate_name = models.CharField(blank=False, max_length=64, verbose_name='名字')

    def __str__(self):
        return self.cate_name

    class Meta:
        db_table = 'cate'
        verbose_name_plural = '新闻类别表'


# 新闻与新闻相似表
class Newsim(models.Model):
    id = models.AutoField(primary_key=True)
    new_id_base = models.CharField(blank=False, max_length=64, verbose_name='ID_base', unique=False)
    new_id_sim = models.CharField(blank=False, max_length=64, verbose_name='ID_sim', unique=False)
    new_correlation = models.CharField(verbose_name='新闻相关度', max_length=100, blank=False)

    # python2.7中使用的是:__unicode__
    def __str__(self):
        return self.new_id_base

    class Meta:
        db_table = 'newsim'
        verbose_name_plural = '新闻相似度表'


# 新闻表
class News(models.Model):
    id = models.AutoField(primary_key=True)
    new_id = models.CharField(blank=False, max_length=64, verbose_name='ID', unique=True)
    new_cate = models.ForeignKey(Cate, related_name='类别', on_delete=models.CASCADE)
    new_time = models.DateTimeField(blank=False, verbose_name='发表时间')
    new_seenum = models.IntegerField(verbose_name='浏览次数', blank=False)  # True表示可不填
    new_disnum = models.IntegerField(verbose_name='跟帖次数', blank=False)  # True表示可不填
    # related_name定义主表对象查询子表时使用的方法名称
    new_title = models.CharField(blank=False, max_length=100, verbose_name='标题')
    new_content = models.TextField(blank=False, verbose_name='新闻内容')

    # python2.7中使用的是:__unicode__
    def __str__(self):
        return self.new_title

    class Meta:
        db_table = 'new'
        verbose_name_plural = '新闻信息表'


# 新闻热度表
class Newhot(models.Model):
    id = models.AutoField(primary_key=True)
    new_id = models.CharField(blank=False, max_length=64, verbose_name='ID', unique=True)
    new_cate = models.ForeignKey(Cate, related_name='类别名', on_delete=models.CASCADE)
    new_hot = models.FloatField(verbose_name='热度值', blank=False)

    # python2.7中使用的是:__unicode__
    def __str__(self):
        return self.new_id

    class Meta:
        db_table = 'newhot'
        verbose_name_plural = '新闻热度表'


# 新闻标签对应表
class Newtag(models.Model):
    id = models.AutoField(primary_key=True)
    new_tag = models.CharField(blank=False, max_length=64, verbose_name='标签', unique=False)
    new_id = models.CharField(blank=False, max_length=64, verbose_name='ID', unique=False)
    new_hot = models.FloatField(verbose_name='热度值', blank=False)

    # python2.7中使用的是:__unicode__
    def __str__(self):
        return self.new_tag

    class Meta:
        db_table = 'newtag'
        verbose_name_plural = '新闻标签表'


# 用户点击表
class Newbrowse(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(blank=False, max_length=64, verbose_name='用户名', unique=False)
    new_id = models.CharField(blank=False, max_length=64, verbose_name='ID', unique=False)
    new_browse_time = models.DateTimeField(blank=False, verbose_name='浏览时间')

    # python2.7中使用的是:__unicode__
    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'newbrowse'
        verbose_name_plural = '用户点击表'
