from django.contrib import admin
from django.contrib.contenttypes import generic
from base_map.models import   Point, Polygon, MultiPolygon, Line

class PointInline(generic.GenericTabularInline):
    max_num = 1
    model = Point
    
class PolygonInline(generic.GenericTabularInline):
    max_num = 1
    model = Polygon

class MultiPolygonInline(generic.GenericTabularInline):
    max_num = 1
    model = MultiPolygon
    
class LineInline(generic.GenericTabularInline):
    max_num = 1
    model = Line


