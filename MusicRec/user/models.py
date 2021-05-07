# -*- coding:utf-8 -*-
from django.db import models

# 用户信息：用户id，昵称，生日，性别，省份，城市，类型，标签，头像链接，用户状态，账号状态，djstatus，vipstatus，签名


class User(models.Model):
    id = models.AutoField(primary_key=True)
    u_id = models.CharField(blank=False, max_length=64, verbose_name='用户ID', unique=True)
    u_name = models.CharField(blank=False, max_length=150, verbose_name='用户昵称')
    u_birthday = models.CharField(blank=True,max_length=64, verbose_name='生日')
    u_gender = models.IntegerField(blank=True, verbose_name='用户性别')
    u_province = models.CharField(blank=True, max_length=20, verbose_name='用户省份')
    u_city = models.CharField(blank=True, max_length=20, verbose_name='用户城市')
    u_type = models.CharField(blank=True, max_length=10, verbose_name='用户类型')
    u_tags = models.CharField(blank=True, max_length=1000, verbose_name='用户标签')
    u_img_url = models.CharField(blank=True, max_length=1000, verbose_name='头像链接')
    u_auth_status = models.CharField(blank=True, max_length=10, verbose_name='用户状态')
    u_account_status = models.CharField(blank=True, max_length=10, verbose_name='账号状态')
    u_dj_status = models.CharField(blank=True, max_length=10, verbose_name='DJ状态')
    u_vip_type = models.CharField(blank=True, max_length=10, verbose_name='VIP状态')
    u_sign = models.TextField(blank=True, verbose_name='用户签名')

    # python2.7中使用的是__unicode__
    def __str__(self):
        return self.u_name

    class Meta:
        db_table = 'user'
        verbose_name_plural = '用户信息'


# 用户标签表
class UserTag(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(blank=False, max_length=64, verbose_name='用户ID')
    tag = models.CharField(blank=True, max_length=64, verbose_name='用户标签')

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'usertag'
        verbose_name_plural = '用户标签'


# 用户点击表
class UserBrowse(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(blank=False, max_length=64, verbose_name='用户名')
    click_id = models.CharField(blank=True, max_length=64, verbose_name='ID')
    click_cate = models.CharField(blank=True, max_length=64, verbose_name='类别')
    user_click_time = models.DateTimeField(blank=True, verbose_name='浏览时间')
    desc = models.CharField(blank=True, max_length=1000, verbose_name='备注', default='Are you readly!')

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'userbrowse'
        verbose_name_plural = '用户行为信息'


# 用户相似表
class UserSim(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    sim_user_id = models.CharField(blank=True, max_length=64, verbose_name='相似用户ID')
    sim = models.FloatField(blank=True, verbose_name='用户相似度')

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'usersim'
        verbose_name_plural = '用户相似'


# 用户歌单推荐表
class UserPlayListRec(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    related = models.CharField(blank=True, max_length=64, verbose_name='歌单ID')
    sim = models.FloatField(blank=True, verbose_name='相似度')

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'userplaylistrec'
        verbose_name_plural = '用户歌单推荐'


# 用户歌曲推荐
class UserSongRec(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    related = models.CharField(blank=True, max_length=64, verbose_name='曲ID')
    sim = models.FloatField(blank=True, verbose_name='相似度')

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'usersongrec'
        verbose_name_plural = '用户歌曲推荐'


# 用户歌手推荐
class UserSingRec(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    related = models.CharField(blank=True, max_length=64, verbose_name='歌手ID')
    sim = models.FloatField(blank=True, verbose_name='相似度')

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'usersimgrec'
        verbose_name_plural = '用户歌手推荐'


# 用户用户推荐表
class UserUserRec(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    related = models.CharField(blank=True, max_length=64, verbose_name='用户ID')
    sim = models.FloatField(blank=True, verbose_name='相似度')

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'useruserrec'
        verbose_name_plural = '用户用户推荐'
