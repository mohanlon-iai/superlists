from accounts.models import User, Token

class PasswordlessAuthenticationBackend():
	
	def authenticate(self, uid):
		if not Token.objects.filter(uid=uid).exists():
			return None
		token = Token.objects.get(uid=uid)
		
		if not User.objects.filter(email=token.email).exists():
			return User.objects.create(email=token.email)
		else:
			return User.objects.get(email=token.email)			
		
	def get_user(self, email):
		if User.objects.filter(email=email).exists():
			return User.objects.get(email=email)
		else:
			return None