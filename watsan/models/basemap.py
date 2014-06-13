from django.utils.datetime_safe import datetime
from django.contrib.gis.db import models
from base_map.models.shapes import *
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
import base_map
import math

class Landmark(ShapeMixin, models.Model):
    PLACE_CHOICES = (
        ('church', 'Church'),
        ('mosque', "Mosque"),
        ('school', 'School'),
        ('bar', 'Bar'),
        ('shop', 'Shop'),
        ('hospital', "Hospital"),
        ('bridge', "Bridge"),
        ('water', 'Water'),
        ('sanitation', 'Sanitation'),
        ('community', 'Community'),
        ('entrance', 'Entrance'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=500)
    place_type = models.CharField(max_length=50, choices=PLACE_CHOICES)

    date_added = models.DateTimeField(default=datetime.now)

    visible = models.BooleanField(default=True)

    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    objects = GeoInheritanceManager()

    def get_fields(self):
        return self._meta.fields
    
    def get_field_details(self):
        return [(field.name, field.value_to_string(self)) for field in self._meta.fields]
        
    class Meta:
        ordering = ['place_type', 'name']
        app_label = 'watsan'
        db_table = 'watsan_landmark'
        
    def __unicode__(self):
        return self.name


class Road(ShapeMixin, models.Model):
    name = models.CharField(max_length=500)
    road_type = models.CharField(max_length=500)

    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['name']
        app_label = 'watsan'
        db_table = 'watsan_road'
        
    def __unicode__(self):
        return self.name

class SearchResult(ShapeMixin, models.Model):
    name = models.CharField(max_length=500)
    search_engine = models.CharField(max_length=500)

    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['name']
        app_label = 'watsan'
        db_table = 'watsan_searchresult'

    def __unicode__ (self):
        return self.name

class SewerLine(ShapeMixin, models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['name']
        app_label = 'watsan'
        db_table = 'watsan_sewerline'

    def __unicode__(self):
        return self.name

class WaterLine(ShapeMixin, models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['name']
        app_label = 'watsan'
        db_table = 'watsan_waterline'

    def __unicode__(self):
        return self.name


class Village(ShapeMixin, models.Model):
    name = models.CharField(max_length=50, default="")
    _shape =generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        ordering = ['name']
        app_label = 'watsan'
        db_table = 'watsan_village'

    def __unicode__(self):
        return self.name

class Site(ShapeMixin, models.Model):
    user = models.ForeignKey(User, blank=True, null=True)

    name = models.CharField(max_length=50)
    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    saved = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now)
    color = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'watsan'
        db_table = 'watsan_sites'

    def __unicode__(self):
        return self.name

    def is_within(self):
        for village in Village.objects.exclude(name='Kibera'):
            try:
                shape = village.shape
                point = GEOSGeometry(self.shape)
                if shape.contains(point):
                    return  village.name
            except Exception as e:
                print e
        return False

    def get_closest_landmarks(self):
        radius = 5
        unit = 'km'
        point = GEOSGeometry(self.shape)

        landmark_ctype = ContentType.objects.get(app_label='watsan', model='landmark')
        points_qs = base_map.models.Point.geo_objects.filter(content_type=landmark_ctype)
        points_qs = points_qs.filter(shape__distance_lte=(point, D(**{unit:radius})))
        if points_qs:
            point1 = points_qs.distance(point).order_by('distance')[0]
            point2 = points_qs.distance(point).order_by('distance')[1]
            landmark1 = Landmark.objects.get(_shape=point1)
            landmark2 = Landmark.objects.get(_shape=point2)
            return landmark1.name + ', ' + landmark2.name
        else:
            return ''

    def get_closest_utilityline(self, model_name):
        point = GEOSGeometry(self.shape)
        village_name = self.is_within()
        village = Village.objects.get(name=village_name)
        utilityline_ctype = ContentType.objects.get(app_label='watsan', model=model_name)
        utilityline_qs = base_map.models.Line.geo_objects.filter(content_type=utilityline_ctype)
        utilityline_qs = utilityline_qs.filter(shape__intersects=GEOSGeometry(village.shape))
        #utilityline_qs = utilityline_qs.filter(shape__distance_lte=(point, D(**{'m':500})))

        if utilityline_qs:
            return utilityline_qs.distance(point).order_by('distance')[0]
        else:
            return False


    def get_closest_waterline_distance(self):
        waterline = self.get_closest_utilityline(model_name='waterline')
        if waterline:
            return math.floor(float(str(waterline.distance).replace(" m", "") ))
        else:
            return False

    def get_closest_sewerline_distance(self):
        sewerline = self.get_closest_utilityline(model_name='sewerline')
        if sewerline:
            return math.floor(float(str(sewerline.distance).replace(" m", "") ))
        else:
            return False

    def get_closest_waterline_cost(self):
        waterline_distance = self.get_closest_waterline_distance()
        if waterline_distance:
            return waterline_distance * 350
        else:
            return False

    def get_closest_sewerline_cost(self):
        sewerline_distance = self.get_closest_sewerline_distance()
        if sewerline_distance:
            return sewerline_distance * 2800
        else:
            return False

    def get_water_info(self):
        distance = self.get_closest_waterline_distance()
        if distance:
            return '{"connect": "true", "distance":"' + str(distance) + '", "cost": "'+ str(self.get_closest_waterline_cost()) +'" }'
        else:
            return '{"connect": "False"}'

    def get_sewer_info(self):
        distance = self.get_closest_sewerline_distance()
        if distance:
            return '{"connect": "true", "distance":"' + str(distance) + '", "cost": "'+ str(self.get_closest_sewerline_cost()) +'" }'
        else:
            return '{"connect": "False"}'

class Project(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now)
    sites = models.ManyToManyField(Site)
   
    class Meta:
        app_label = 'watsan'
        db_table = 'watsan_project'

    def __unicode__(self):
        return self.name

class Manhole(models.Model):
    name = models.CharField(max_length=50)
    _shape = generic.GenericRelation(Shape, content_type_field='content_type', object_id_field='object_id')

    class Meta:
        app_label = 'watsan'
        db_table = 'watsan_manhole'

    def __unicode__(self):
        return self.name
        