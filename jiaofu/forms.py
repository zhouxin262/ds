#coding=utf-8
# from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from jiaofu.models import Zixun


class ZixunForm(BootstrapModelForm):
    class Meta:
        layout = (
            Fieldset(u"", "fangshi",
                     "xuehao",  "renyuanleibie", "wentileibie","wenti", "memo"),
        )
        model = Zixun
        exclude = ("jiejuefangan", "dateline", "typer",)
