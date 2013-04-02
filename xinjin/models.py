#coding=utf-8
from django.db import models
from django.contrib.auth.models import User


class XinjinDan(models.Model):
    bianhao = models.CharField(
        verbose_name=u"编号", max_length=30, blank=True, default='', unique=True)
    xiangmu = models.CharField(
        verbose_name=u"项目", max_length=30, blank=True, default='')
    month = models.IntegerField(verbose_name=u"月份")
    year = models.IntegerField(verbose_name=u"年份")
    dateline = models.DateField(
        verbose_name=u"输入日期", null=True, blank=True, auto_now=True)
    typer = models.ForeignKey(User, related_name="xinjindan_typer")

    def __unicode__(self):
        return self.bianhao


class Xinjin(models.Model):
    STATUS_CHOICES = (('1', u'通过'), ('0', u'未通过'))
    LEIXING_CHOICES = (('1', u'劳务'), ('0', u'工资'))
    user = models.ForeignKey(User, verbose_name=u"姓名", related_name="xinjin")
    xinjindan = models.ForeignKey(
        XinjinDan, verbose_name=u"薪金单", related_name="xinjin")
    yingfa = models.DecimalField(
        verbose_name=u"应发", null=True, max_digits=11,
        decimal_places=0, blank=True, default=0)
    baoxian = models.DecimalField(
        verbose_name=u"保险", null=True, max_digits=11,
        decimal_places=0, blank=True, default=0)
    gongjijin = models.DecimalField(
        verbose_name=u"公积金", null=True, max_digits=11,
        decimal_places=0, blank=True, default=0)
    leixing = models.CharField(u"类型", max_length=1, default='0', choices=LEIXING_CHOICES)
    month = models.IntegerField(verbose_name=u"月份")
    year = models.IntegerField(verbose_name=u"年份")
    dateline = models.DateField(
        verbose_name=u"输入日期", null=True, blank=True, auto_now=True)
    typer = models.ForeignKey(User, related_name="xinjin_typer")
    status = models.CharField(max_length=1, default='0', choices=STATUS_CHOICES)


