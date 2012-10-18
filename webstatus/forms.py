#coding=utf-8
from bootstrap import forms
from bootstrap.forms import BootstrapModelForm, Fieldset
from models import WebStatus

class WebStatusForm(BootstrapModelForm):
	class Meta:
		layout = (
            Fieldset(u"状态记录", "log_date", "log_time", "jsgzs", "xsgzs", "zxcs", "jhkt", "memo",),
        )
		model = WebStatus
		exclude = ('dateline','user')