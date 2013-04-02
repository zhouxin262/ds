#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class WebStatus(models.Model):
    STATUS_CHOICES = ((u'正常', u'正常'), (u'异常', u'异常'),)
    TIME_CHOICES = ((u'08:00', u'08:00'), (u'14:00', u'14:00'), (u'18:00', u'18:00'),)
    user = models.ForeignKey(User, related_name="webstatus")
    jsgzs = models.CharField(max_length=10, verbose_name=u"教师工作室", choices=STATUS_CHOICES, default=u"正常")
    xsgzs = models.CharField(max_length=10, verbose_name=u"学生工作室", choices=STATUS_CHOICES, default=u"正常")
    zxcs = models.CharField(max_length=10, verbose_name=u"在线测试", choices=STATUS_CHOICES, default=u"正常")
    jhkt = models.CharField(max_length=10, verbose_name=u"交互课堂", choices=STATUS_CHOICES, default=u"正常")
    memo = models.TextField(max_length=10, verbose_name=u"异常备注", blank=True, default="", help_text=u"如有异常填写备注，记录（用户名、姓名、电话、异常功能名称、详细描述）")
    log_date = models.DateField(null=True, blank=True, verbose_name="日期")
    log_time = models.CharField(max_length=10, verbose_name=u"时间", default="08:00")
    dateline = models.DateTimeField(auto_now_add=True)
