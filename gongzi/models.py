#coding=utf-8
from django.db import models

from django.contrib.auth.models import User

class Remuneration(models.Model):
    user = models.ForeignKey(User)
    realname = models.CharField(max_length=150, blank=True)
    idcard = models.CharField(max_length=150, blank=True)
    amount = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    insurance = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    provident = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    taxable = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    taxrate = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    taxes = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    dues = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    paid = models.DecimalField(null=True, max_digits=11, decimal_places=0, blank=True)
    type = models.CharField(max_length=150)
    month = models.CharField(max_length=150)
    dateline = models.DateField(null=True, blank=True)