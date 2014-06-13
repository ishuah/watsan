from django.contrib.gis.db import models
from django.contrib.auth.models import User 

from watsan.models.organizations import Organization 

class WatsanUserMeta(models.Model):

	user = models.OneToOneField(User)
	organization = models.ForeignKey(Organization)
	question_1 = models.CharField(max_length=350)
	question_2 = models.CharField(max_length=350)
	
	
	class Meta:
		app_label = 'watsan'
		db_table = 'watsan_usermeta'

	def __unicode__(self):
		return self.user.username