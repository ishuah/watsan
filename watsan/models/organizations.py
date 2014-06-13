from django.contrib.gis.db import models

class Organization(models.Model):
	name = models.CharField(max_length=50)
	org_type = models.CharField(choices=(('CBO', 'CBO'), ('NGO', 'NGO'), ('school', 'School'), ('private', 'Private')), max_length=10)

	class Meta:
		app_label = 'watsan'
		db_table = 'watsan_organization' 
		permissions = (
			("access_watsan", "Can access watsan portal"),
		)

	def __unicode__(self):
		return self.name