from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime

class NewEmail(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField()
	hash_string = models.CharField(max_length=10)
	created_on = models.DateTimeField(default=datetime.now)
	transfered = models.BooleanField()

	class Meta:
		app_label = 'watsan'

	def __unicode__(self):
		return self.email

