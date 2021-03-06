#coding=utf-8
from django.db import models
from django.contrib.auth.models import User, Group


class Wentileibie(models.Model):
    WENTILEIBIE_CHOICES = ((u"招生", u"招生"), (u"入学", u"入学"),
                           (u"学习内容", u"学习内容"), (u"平台问题", u"平台问题"), (u"平台使用", u"平台使用"),
                           (u"信息查询", u"信息查询"), (u"学籍规定", u"学籍规定"), (u"考试", u"考试"),
                           (u"统考", u"统考"), (u"学位", u"学位"), (u"毕业设计", u"毕业设计"), (u"其他", u"其他"),
                           )
    name = models.CharField(
        verbose_name=u"问题类别", max_length=30, default=u"")
    users = models.ManyToManyField(User, related_name="wentileibie", blank=True)
    groups = models.ManyToManyField(Group, related_name="wentileibie", blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'问题类别'
        verbose_name_plural = u'问题类别'


class Zixun(models.Model):
    FANGSHI_CHOICES = (("Q", u"QQ"), ("E", u"EMAIL"), ("T", u"电话"),  ("W", u"网站"),  ("L", u"来访"), ("A", u"其他"), )
    WENTILEIBIE_CHOICES = ((u"招生", u"招生"), (u"入学", u"入学"),
                           (u"学习内容", u"学习内容"), (u"平台问题", u"平台问题"), (u"平台使用", u"平台使用"),
                           (u"信息查询", u"信息查询"), (u"学籍规定", u"学籍规定"), (u"考试", u"考试"),
                           (u"统考", u"统考"), (u"学位", u"学位"), (u"毕业设计", u"毕业设计"), (u"其他", u"其他"),
                           )
    RENYUANLEIBIE_CHOICES = ((u"成人", u"成人"), (u"网络", u"网络"),
                             (u"交通", u"交通"), (u"自考", u"自考"), (u"站点", u"站点"), (u"校外", u"校外"), (u"其他", u"其他"),)
    CHULIQINGKUANG_CHOICES = ((u"已", u"已处理"), (u"处", u"处理中"), (u"待", u"待处理"),)
    fangshi = models.CharField(
        verbose_name=u"方式", max_length=30, default='Q', choices=FANGSHI_CHOICES)
    xuehao = models.CharField(
        verbose_name=u"学号", max_length=30, blank=True, default='')
    zhandian = models.CharField(
        verbose_name=u"站点名称", max_length=30, blank=True, default='')
    lianxifangshi = models.CharField(
        verbose_name=u"联系方式", max_length=30, blank=True, default='')
    wenti = models.TextField(
        verbose_name=u"问题", blank=True, default='')
    renyuanleibie = models.CharField(
        verbose_name=u"人员类别", max_length=30, default=u"成人", choices=RENYUANLEIBIE_CHOICES)
    wentileibie = models.ForeignKey('Wentileibie', verbose_name='问题类别', null=False, default=Wentileibie.objects.filter()[0])
    memo = models.TextField(
        verbose_name=u"备注", blank=True, default='')
    jiejuefangan = models.TextField(
        verbose_name=u"解决方案", blank=True, default='')
    dateline = models.DateTimeField(
        verbose_name=u"输入日期", null=True, blank=True, auto_now_add=True)
    chuliqingkuang = models.CharField(max_length=2, choices=CHULIQINGKUANG_CHOICES, default=u"待", blank=True, verbose_name="处理情况")
    typer = models.ForeignKey(User, related_name="jiaofu_zixun_typer")
    jiejue_typer = models.ForeignKey(User, related_name="Jiejue_typer", null=True, blank=True)
    jiejue_dateline = models.DateTimeField(verbose_name=u"解决日期", null=True, blank=True, auto_now=True)
