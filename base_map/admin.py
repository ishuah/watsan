from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from base_map.models import   Point, Polygon, MultiPolygon, Line

class PointInline(GenericTabularInline):
    max_num = 1
    model = Point
    
class PolygonInline(GenericTabularInline):
    max_num = 1
    model = Polygon

class MultiPolygonInline(GenericTabularInline):
    max_num = 1
    model = MultiPolygon
    
class LineInline(GenericTabularInline):
    max_num = 1
    model = Line


