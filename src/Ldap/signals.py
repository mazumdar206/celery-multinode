from Ldap.models import LdapConfig

def add_groups(sender, instance, **kwargs):
	print(instance.access_groups)

def delete_group(sender, instance, **kwargs):
	print(instance.access_groups)

