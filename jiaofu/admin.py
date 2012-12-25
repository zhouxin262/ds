from django.contrib import admin
from django.forms import ModelMultipleChoiceField
from django.contrib.auth.models import User
from django.forms import ModelForm

from jiaofu.models import Wentileibie


class UserModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Return a string of the format: "firstname lastname (username)"
        return "%s" % (obj.get_full_name())


class WentileibieAdminForm(ModelForm):
    users = UserModelChoiceField(User.objects.all().order_by('first_name'))

    def __init__(self, *args, **kwargs):
        super(WentileibieAdminForm, self).__init__(*args, **kwargs)
        self.fields['users'].widget.attrs['size'] = '30'

    class Meta:
        model = Wentileibie


class WentileibieAdmin(admin.ModelAdmin):
    form = WentileibieAdminForm

admin.site.register(Wentileibie, WentileibieAdmin)
