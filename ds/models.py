#coding=utf-8
from django.db import models

class News(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)