from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from model_utils.managers import InheritanceManagerMixin, InheritanceQuerySet

class GeoInheritanceManager(InheritanceManagerMixin, models.GeoManager):
    def get_queryset(self):
        return InheritanceQuerySet(self.model)

class GeoSubclassManager(InheritanceManagerMixin, models.GeoManager):
    def get_query_set(self):
        return InheritanceQuerySet(self.model).select_subclasses()