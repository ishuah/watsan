import string
import random
from django.contrib import messages
from .models import UserProfile

def generate_confirmation_code(size=20):
	return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(size))

def get_user_status(request):
	try:
		profile = UserProfile.objects.get(user=request.user)
		if profile.confirmation_code:
			messages.warning(request, "Your account has not been confirmed. If you didn't receive a confirmation email please check your spam/junk folder")
	except UserProfile.DoesNotExist:
		messages.warning(request, "Please set up your user profile")