from django.test import TestCase, client
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.contrib.sites.models import Site
from spatialcollective.settings import DEFAULT_HOST

class testPasswordResetFunctions(TestCase):
	def setUp(self):
		self.group = Group.objects.create(name="Public")
		self.user = User.objects.create_user('user', 'email@email.com', 'password')
		self.site = Site.objects.create(name=DEFAULT_HOST, domain=DEFAULT_HOST)
		self.site2 = Site.objects.create(name='testserver', domain='testserver')
		
	def test_reset_password_sends_email(self):
		resp = self.client.post('/users/password_reset/', {'email': 'email@email.com'}, follow=True)
		# self.assertEquals(mail.outbox[0].subject, 'Welcome to Spatial Collective!')
		self.assertEqual(resp.template_name, 'settings/password/reset_done.html')
		self.assertEqual(len(mail.outbox), 1)
		self.assertEquals(mail.outbox[0].recipients()[0], 'email@email.com')

	def test_password_reset_link_isvalid(self):
		resp = self.client.post('/users/password_reset/', {'email': 'email@email.com'})
		self.assertEqual(resp.status_code, 302)
		token = resp.context[0]['token']
		uid = resp.context[0]['uid']

		resp = self.client.get('/users/password_reset_confirm/'+str(uid)+'/'+str(token), follow=True)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.template_name, 'settings/password/reset_confirm.html')
		self.assertEqual(resp.context[0]['validlink'], True)

	def test_submiting_blank_password_reset_returns_error(self):
		resp = self.client.post('/users/password_reset/', {'email': 'email@email.com'})
		self.assertEqual(resp.status_code, 302)
		token = resp.context[0]['token']
		uid = resp.context[0]['uid']

		resp = self.client.post(reverse('password_reset_confirm', kwargs={'token':token,'uidb64':uid}), {'new_password1':'','new_password2':''}, follow=True)
		self.assertEqual(resp.template_name, 'settings/password/reset_confirm.html')

	def test_successful_password_reset_logs_user_in(self):
		resp = self.client.post('/users/password_reset/', {'email': 'email@email.com'})
		self.assertEqual(resp.status_code, 302)
		token = resp.context[0]['token']
		uid = resp.context[0]['uid']

		resp = self.client.post(reverse('password_reset_confirm', kwargs={'token':token,'uidb64':uid}), {'new_password1':'pass','new_password2':'pass'}, follow=True)
		self.assertRedirects(resp, '/welcome/?next=/')