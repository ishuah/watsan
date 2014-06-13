from django.contrib import admin
from django.contrib.contenttypes import generic
from watsan.models.users import WatsanUserMeta
from watsan.models.organizations import Organization
from watsan.models.change_email import NewEmail
from watsan.models.basemap import Landmark, Road, Site, SearchResult, SewerLine, WaterLine, Village, Project, Manhole
from base_map.models import Shape, Point, Polygon, MultiPolygon, Line

class PointInline(generic.GenericTabularInline):
    max_num = 1
    model = Point

class LineInline(generic.GenericTabularInline):
    max_num = 1
    model = Line

class PolygonInline(generic.GenericTabularInline):
    max_num = 1
    model = Polygon

class LandmarkAdmin(admin.ModelAdmin):
    inlines = [
        PointInline,
    ]

class RoadAdmin(admin.ModelAdmin):
    inlines = [
        LineInline,
    ]

class SiteAdmin(admin.ModelAdmin):
    inlines = [
        PointInline,
    ]

class SearchResultAdmin(admin.ModelAdmin):
    inlines = [
        PointInline,
    ]

class SewerLineAdmin(admin.ModelAdmin):
    inlines = [
        LineInline,
    ]

class WaterLineAdmin(admin.ModelAdmin):
    inlines = [
        LineInline,
    ]

class VillageAdmin(admin.ModelAdmin):
    inlines = [
        PolygonInline
    ]

class ManholeAdmin(admin.ModelAdmin):
    inlines = [
        PointInline,
    ]

admin.site.register(WatsanUserMeta)
admin.site.register(Organization)
admin.site.register(NewEmail)
admin.site.register(SearchResult, SearchResultAdmin)
admin.site.register(Landmark, LandmarkAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(SewerLine, SewerLineAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Project)
admin.site.register(WaterLine, WaterLineAdmin)
admin.site.register(Manhole, ManholeAdmin)
#admin.site.register(WatsanUser, WatsanUserAdmin)
#admin.site.unregister(Group)