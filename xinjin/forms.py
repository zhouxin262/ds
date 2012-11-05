#coding=utf-8
# from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from xinjin.models import Xinjin, XinjinDan


class XinjinForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "user",
                     "yingfa", "baoxian", "gongjijin", "leixing"),
        )
        model = Xinjin
        exclude = ("month", "year", "typer", "xinjindan", "status")


class XinjinDanForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "bianhao", "xiangmu", ),
        )
        model = XinjinDan
        exclude = ("month", "year", "typer")
