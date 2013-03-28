#coding=utf-8
from django.db import models

from django.contrib.auth.models import User


class Gongzi(models.Model):
    """
    ALTER TABLE `gongzi_gongzi`
    CHANGE COLUMN `yingfa` `yingfa` DECIMAL(11,2) NULL DEFAULT NULL AFTER `idcard`,
    CHANGE COLUMN `baoxian` `baoxian` DECIMAL(11,2) NULL DEFAULT NULL AFTER `yingfa`,
    CHANGE COLUMN `gongjijin` `gongjijin` DECIMAL(11,2) NULL DEFAULT NULL AFTER `baoxian`,
    CHANGE COLUMN `shuijin` `shuijin` DECIMAL(11,2) NULL DEFAULT NULL AFTER `gongjijin`,
    CHANGE COLUMN `shifa` `shifa` DECIMAL(11,2) NULL DEFAULT NULL AFTER `shuijin`;

    ALTER TABLE `gongzi_gongzi`
    ADD COLUMN `memo` VARCHAR(255) NULL DEFAULT NULL AFTER `year`;

    ALTER TABLE `gongzi_gongzi`
    ADD COLUMN `guilei` VARCHAR(255) NULL AFTER `memo`;
    """
    user = models.ForeignKey(User, related_name="gongzi")
    realname = models.CharField(max_length=150, blank=True)
    idcard = models.CharField(max_length=150, blank=True)
    yingfa = models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True, default=0)
    baoxian = models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True, default=0)
    gongjijin = models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True, default=0)
    shuijin = models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True, default=0)
    shifa = models.DecimalField(null=True, max_digits=15, decimal_places=6, blank=True, default=0)
    xiangmu = models.CharField(max_length=30, blank=True, default='')
    month = models.IntegerField()
    year = models.IntegerField()
    memo = models.CharField(max_length=255, blank=True, null=True, default='')
    guilei = models.CharField(max_length=255, blank=True, null=True, default='')
    dateline = models.DateField(null=True, blank=True, auto_now=True)
