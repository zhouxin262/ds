#coding=utf-8
# from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from jiaofu.models import Zixun


class ZixunForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "fangshi",
                     "xuehao", "zhandian", "lianxifangshi", "renyuanleibie", "wentileibie", "wenti", "memo"),
        )
        model = Zixun
        exclude = ("jiejuefangan", "dateline", "typer", "jiejue_typer", "chuliqingkuang", "jiejuedateline")


class JiejueForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "chuliqingkuang", "jiejuefangan"),
        )
        model = Zixun
        exclude = ("dateline", "typer", "jiejue_typer", "jiejuedateline", "fangshi",
                   "xuehao", "zhandian", "lianxifangshi", "renyuanleibie", "wentileibie", "wenti", "memo")
