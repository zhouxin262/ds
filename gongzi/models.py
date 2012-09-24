#coding=utf-8
from django.db import models

from django.contrib.auth.models import User

class Gongzi(models.Model):
    user = models.ForeignKey(User)
    realname = models.CharField(max_length=150, blank=True)
    idcard = models.CharField(max_length=150, blank=True)
    yingfa = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    baoxian = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    gongjijin = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    shuijin = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    shifa = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    xiangmu = models.CharField(max_length=30, blank=True)
    month = models.IntegerField()
    year = models.IntegerField()
    dateline = models.DateField(null=True, blank=True)