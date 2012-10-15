from django.conf import settings
from django.contrib.auth.models import User

class MingwenBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """
    
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(last_name=username)
                if user.password == password:
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None