#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)


class Gongzihao(models.Model):
    user = models.OneToOneField(User, related_name='gongzihao')
    gongzihao = models.CharField(max_length=30)
