from django.db import models
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import Group
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




class LdapConfig(models.Model):
	uri = models.CharField(max_length = 255)
	port = models.CharField(max_length = 20)
	ldaps = models.BooleanField()
	cert_content = models.TextField(null = True, blank = True)
	bind_dn = models.CharField(max_length = 255)
	bind_password = models.CharField(max_length = 255)
	access_groups = models.TextField()

def add_groups(sender, instance, **kwargs):
	group_list = instance.access_groups.split(',')
	for group in group_list:
		new_group, created = Group.objects.get_or_create(name=group)
	f = open(os.path.join(BASE_DIR,"ldapcert",instance.bind_dn+".pem"),"w+")
	f.write(instance.cert_content)
	f.close()

def delete_groups(sender, instance, **kwargs):
	group_list = instance.access_groups.split(',')
	for group in group_list:
		try:
			Group.objects.filter(name = group).delete()
		except Exception as e:
			print(e)
	if os.path.exists(os.path.join(BASE_DIR,"ldapcert",instance.bind_dn+".pem")):
		os.remove(os.path.join(BASE_DIR,"ldapcert",instance.bind_dn+".pem"))
			

post_save.connect(add_groups, sender = LdapConfig)
post_delete.connect(delete_groups, sender = LdapConfig)

# Create your models here.
