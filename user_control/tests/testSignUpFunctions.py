from django.test import TestCase, client
from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos.geometry import GEOSGeometry
from user_control.models import NewUserForm, UserProfile
from django.contrib.sites.models import Site
from spatialcollective.settings import DEFAULT_HOST

class testSignUpFunction(TestCase):
	def setUp(self):
		self.group = Group.objects.create(name="Public")
		self.site = Site.objects.create(name=DEFAULT_HOST, domain=DEFAULT_HOST)
		self.site2 = Site.objects.create(name='testserver', domain='testserver')
		
	def test_GET_returns_new_form(self):
		resp = self.client.get('/users/signup/')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(isinstance(resp.context['userform'], NewUserForm))

	def test_user_password_and_username_other_data_saved(self):
		resp = self.client.post('/users/signup/', {'username': 'username', 'password1': 'password', 'organization': 'org', 'email': 'email@email.com'})
		user = User.objects.get(username='username')
		profile = UserProfile.objects.get(user=user)

		self.assertTrue(user is not None)
		self.assertTrue(profile is not None)
		self.assertEquals(profile.organization, 'org')

	def test_confirmation_email_sends_on_successful_signup(self):
		html_content = render_to_string('email/confirmation.html', { 'username': 'username' })
		text_content = strip_tags(html_content)
		resp = self.client.post('/users/signup/', {'username': 'username', 'password1': 'password', 'organization': 'org', 'email': 'email@email.com'})
		self.assertEquals(mail.outbox[0].subject, 'Email Confirmation')
		self.assertEquals(mail.outbox[0].body, text_content)
		self.assertEquals(mail.outbox[0].recipients()[0], 'email@email.com')

	def test_verification_link_redirects_to_home(self):
		user = User.objects.get(username='username')
		profile = UserProfile.objects.get(user=user)

		resp = self.client.get('/users/confirm/'+profile.confirmation_code+'/'+user.username)
		self.assertRedirects(resp, '/', status_code=302, target_status_code=200, msg_prefix='')
