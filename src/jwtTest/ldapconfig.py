import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

cert = "ldapcet/ca.pem"

LDAP_SERVER = 'ipa.autonet.auth'
AUTH_LDAP_SERVER_URI = 'ldap://' + LDAP_SERVER

AUTH_LDAP_BIND_DN = 'uid=admin,cn=users,cn=accounts,dc=autonet,dc=auth'
AUTH_LDAP_BIND_PASSWORD = "Nishstar48"
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,cn=users,cn=accounts,dc=autonet,dc=auth'
AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_NETWORK_TIMEOUT: 5,
                                }

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_CACERTFILE : cert,
}
AUTH_LDAP_START_TLS = True

AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail'
}

AUTH_LDAP_GROUP_BASE = "cn=groups,cn=accounts,dc=autonet,dc=auth"
AUTH_LDAP_GROUP_FILTER = "(objectClass=groupOfNames)"
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_GROUP_BASE,
                                    ldap.SCOPE_SUBTREE, AUTH_LDAP_GROUP_FILTER)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_staff': 'cn=ipausers,' + AUTH_LDAP_GROUP_BASE,
    'is_support': 'cn=ipausers,' + AUTH_LDAP_GROUP_BASE,
    'is_superuser': 'cn=ipausers,' + AUTH_LDAP_GROUP_BASE,
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
}

class ConfigChanger:
	def __init__(self):
		self.isnext = True
	def change(self):
		print("changing path")
		global cert 
		cert = "ldapcert/ca.pem"
		self.isnext = False
		print("path changed")
