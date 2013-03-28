from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.utils import importlib
from django.utils.encoding import smart_str
from django.core.exceptions import ImproperlyConfigured


UNUSABLE_PASSWORD = '!'  # This will never be a valid encoded hash
HASHERS = None  # lazily loaded from PASSWORD_HASHERS
PREFERRED_HASHER = None  # defaults to first item in PASSWORD_HASHERS


def load_hashers(password_hashers=None):
    global HASHERS
    global PREFERRED_HASHER
    hashers = []
    if not password_hashers:
        password_hashers = settings.PASSWORD_HASHERS
    for backend in password_hashers:
        try:
            mod_path, cls_name = backend.rsplit('.', 1)
            mod = importlib.import_module(mod_path)
            hasher_cls = getattr(mod, cls_name)
        except (AttributeError, ImportError, ValueError):
            raise ImproperlyConfigured("hasher not found: %s" % backend)
        hasher = hasher_cls()
        if not getattr(hasher, 'algorithm'):
            raise ImproperlyConfigured("hasher doesn't specify an "
                                       "algorithm name: %s" % backend)
        hashers.append(hasher)
    HASHERS = dict([(hasher.algorithm, hasher) for hasher in hashers])
    PREFERRED_HASHER = hashers[0]


def get_hasher(algorithm='default'):
    """
    Returns an instance of a loaded password hasher.

    If algorithm is 'default', the default hasher will be returned.
    This function will also lazy import hashers specified in your
    settings file if needed.
    """
    if hasattr(algorithm, 'algorithm'):
        return algorithm

    elif algorithm == 'default':
        if PREFERRED_HASHER is None:
            load_hashers()
        return PREFERRED_HASHER
    else:
        if HASHERS is None:
            load_hashers()
        if algorithm not in HASHERS:
            raise ValueError("Unknown password hashing algorithm '%s'. "
                             "Did you specify it in the PASSWORD_HASHERS "
                             "setting?" % algorithm)
        return HASHERS[algorithm]


def is_password_usable(encoded):
    return (encoded is not None and encoded != UNUSABLE_PASSWORD)


def check_password(password, encoded, setter=None, preferred='default'):
    """
    Returns a boolean of whether the raw password matches the three
    part encoded digest.

    If setter is specified, it'll be called when you need to
    regenerate the password.
    """
    if not password or not is_password_usable(encoded):
        return False

    preferred = get_hasher(preferred)
    raw_password = password
    password = smart_str(password)
    encoded = smart_str(encoded)

    if len(encoded) == 32 and '$' not in encoded:
        hasher = get_hasher('unsalted_md5')
    else:
        algorithm = encoded.split('$', 1)[0]
        hasher = get_hasher(algorithm)

    must_update = hasher.algorithm != preferred.algorithm
    is_correct = hasher.verify(password, encoded)
    if setter and is_correct and must_update:
        setter(raw_password)
    return is_correct


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

            def setter(raw_password):
                user.set_password(raw_password)
                user.save()

            if user.password == password:
                return user
            else:
                try:
                    if check_password(password, user.password, setter):
                        return user
                except:
                    return User.DoesNotExist
        except User.DoesNotExist:
            try:
                user = User.objects.get(last_name=username)

                def setter1(raw_password):
                    user.set_password(raw_password)
                    user.save()

                if user.password == password:
                    return user
                else:
                    try:
                        if check_password(password, user.password, setter1):
                            return user
                    except:
                        raise User.DoesNotExist
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_group_perm_cache'):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = Permission.objects.filter(group__user=user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            user_obj._group_perm_cache = set(["%s.%s" % (ct, name) for ct, name in perms])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        if not user_obj.is_active:
            return False
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False
