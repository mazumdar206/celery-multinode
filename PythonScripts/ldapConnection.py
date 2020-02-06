import ldap
import os

class LdapConnection:

	def __init__(self,data):
		self.uri = data['uri']
		self.port = data['port']
		self.ldaps = data['ldaps']
		self.cert_content = data['cert_content']
		self.bind_dn = data['bind_dn']
		self.bind_password = data['bind_password']
		self.access_groups = data['access_groups'].split(',')
		self.bind_conn = self.get_connection()
		self.bind_conn.simple_bind_s(self.bind_dn,self.bind_password)
		self.user_base_dn = 'cn=users,cn=accounts,dc=autonet,dc=auth'

	def get_connection(self):
		conn = ldap.initialize(self.uri)
		conn.protocol_version=ldap.VERSION3
		conn.set_option(ldap.OPT_REFERRALS,0)
		conn.set_option(ldap.OPT_TIMEOUT, 5)
		if self.ldaps:
			conn.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,ldap.OPT_X_TLS_DEMAND)
			print(os.path.exists(os.path.join("ldapcert",self.bind_dn+".pem")))
			conn.set_option(ldap.OPT_X_TLS_CACERTFILE,os.path.join("ldapcert",self.bind_dn+".pem"))
			conn.set_option(ldap.OPT_X_TLS_NEWCTX,0)
			conn.start_tls_s()
		return conn


	def search(self,base_dn,filter,attrs):

		res = self.bind_conn.search_s(base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
		return res

	def user_search(self,username):
		res = self.search(self.user_base_dn,'(uid={})'.format(username),['memberOf'])
		return res

	def groups_allowed(self,user_groups):
		res = []
		print(user_groups)
		for group in user_groups:
			print(group)
			group_name = group.decode().split(',')[0].split('=')[1]
			print(group_name)
			if group_name in self.access_groups:
				res.append(group_name)
		return res

	def authenticate(self,username,password):
		res = self.user_search(username)
		if res:
			user_dn = res[0][0] 
			conn = self.get_connection()
			try:
				conn.simple_bind_s(user_dn,password)
				conn.unbind()
				user_groups = res[0][1].get('memberOf',{})
				if self.groups_allowed(user_groups):
					return self.groups_allowed(user_groups)

			except Exception as e:
				print(e)
				return None
		return None

