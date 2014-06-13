from django.test import TestCase, client
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos.geometry import GEOSGeometry
from django.core.exceptions import ValidationError
from watsan.models import *
from django.core.urlresolvers import reverse #this isn't working

class Tests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('user', 'email@email.com', 'password')
		self.privateUser = User.objects.create_user('privateUser', 'email@email.com', 'password')
		self.adminUser = User.objects.create_superuser('admin', 'email@email.com', 'password')
		self.publicGroup = Group.objects.create(name="Public")
		self.privateGroup = Group.objects.create(name="Private")
		self.privateUser.groups.add(self.privateGroup)

	def tearDown(self):
		Group.objects.all().delete()
		User.objects.all().delete()

	def test_without_logging_in_I_should_be_redirected(self):
		resp = self.client.get('')
		self.assertEqual(resp.status_code, 302)

	def test_as_user_I_want_to_log_in(self):
		self.client.login(username='user', password='password')	
		resp = self.client.get('')
		self.assertEqual(resp.status_code, 200)

	def test_if_I_log_in_then_out_should_be_denied_access(self):
		self.client.login(username='user', password='password')	
		resp = self.client.get('')
		self.client.logout()
		resp = self.client.get('')
		self.assertEqual(resp.status_code, 302)

