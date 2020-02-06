
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User,Group
import sys
sys.path.insert(1,'../PythonScripts')
from ldapConnection import LdapConnection
from Ldap.models import LdapConfig


class AuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        # Get the user information from the LDAP if he can be authenticated
        configs = LdapConfig.objects.all()
        for config in configs:
            config_dict = config.__dict__
            if not config_dict['uri'].startswith('ldap://'):
                config_dict['uri'] = 'ldap://'+config_dict['uri']
            try:
                conn = LdapConnection(config_dict)
                group_list = conn.authenticate(username, password)
                if group_list is None:
                    print('failed',config_dict['uri'])
                    continue

                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User(username=username)
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_support = True
                    user.save()
                for group in group_list:
                    django_group = Group.objects.get(name = group)
                    django_group.user_set.add(user)

                return user
            except Exception as e:
                print(e,'failed',config_dict['uri'])
        return None

            
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None