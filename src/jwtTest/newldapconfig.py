from django_auth_ldap.backend import LDAPBackend
from jwtTest.ldapconfig import ConfigChanger

class LDAPBackend1(LDAPBackend):
	settings_prefix = "AUTH_LDAP_"

	def authenticate_ldap_user(self,ldap_user,password):
		changer = ConfigChanger()
		changer.change()
		user = ldap_user.authenticate(password)
		if user == None:
			print("1fail",changer.isnext)
		while user == None and changer.isnext:
			print("entering")
			changer.change()
			print("exited")
			user = ldap_user.authenticate(password)
			if user -- None:
				print("2fail")
			else :
				print("2sucess")
		return user