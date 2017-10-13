import json
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from watsan.models.basemap import Landmark, Road, Site, SearchResult, SewerLine, WaterLine, Village, Project
from django.views.decorators.csrf import csrf_exempt
from watsan.models import WatsanUserMeta, Organization
from django.contrib.auth.models import User
import base_map
from base_map.models import *
from django.http import HttpResponse
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.db import models
from django.contrib.gis.db import models as geomodels
import math

LOGIN_PAGE = 'watsan_landing'

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def dashboard(request):
	projects = Project.objects.filter(user=request.user).order_by('date_created').reverse()
	return render(request, 'dashboard/home.html', { 'projects': projects })

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def project(request, projectId=None):
	project = get_object_or_404(Project, pk=projectId)
	return render(request, 'dashboard/project.html', { 'project': project })

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def the_map(request, projectId=None):
	landmarks = Landmark.objects.all()
	roads = Road.objects.all()
	sewerlines = SewerLine.objects.all()
	waterlines = WaterLine.objects.all()
	villages = Village.objects.all()
	if projectId:
		project = get_object_or_404(Project, pk=projectId)
	else:
		project = Project.objects.filter(user=request.user).latest('date_created')

	return render(request, 'map.html', {
		'landmarks': landmarks, 
		'roads': roads, 
		'sewerlines': sewerlines, 
		'waterlines': waterlines, 
		'villages': villages,
		'project': project })

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def ncwsc(request, projectId=None):
	project = get_object_or_404(Project, pk=projectId)
	return render(request, 'dashboard/ncwsc.html', { 'project': project })

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def alts(request, projectId=None):
	project = get_object_or_404(Project, pk=projectId)
	return render(request, 'dashboard/alts.html', { 'project': project })

@login_required(login_url=LOGIN_PAGE)
@permission_required('watsan.access_watsan', login_url=LOGIN_PAGE)
def about(request):
	return render(request, 'about.html')

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def save_landmark(request):
	if request.method == 'POST':
		json_data = json.loads(request.body)
		name = json_data['name']
		search_engine = json_data['search_engine']

		shape = GEOSGeometry('POINT(' + str(json_data['shape']['lng']) + ' ' + str(json_data['shape']['lat']) + ')')

		new_search_result = SearchResult.objects.create(name=name, search_engine=search_engine)
		new_search_result._shape.add(base_map.models.Point(shape=shape))
		new_search_result.save()
		return HttpResponse(status=201)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def save_search_string(request):
	if request.method == 'POST':
		string = request.body
		new_search_result = SearchResult.objects.create(name=string, search_engine='string')
		return HttpResponse(status=201)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def save_site(request):
	if request.method == 'POST':
		coords = request.POST.get('coords')
		site = Site(name=request.POST.get('name'), color=request.POST.get('color'), user=request.user)
		try:
			site.save()
			site._shape.add(base_map.models.Point(shape=coords))
			Project.objects.get(pk=request.POST.get('projectId')).sites.add(site)
			return HttpResponse( '{ "siteId": "'+str(site.id)+'" }', status=201, content_type="application/json")
		except Exception as e:
			print e
			return HttpResponse(status=400)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def save_project(request):
	if request.method == 'POST':
		project = Project(name=request.POST.get('name'), user=request.user)
		try:
			project.save()
			return HttpResponse('{ "projectId": ' + str(project.id) + '}', status=201, content_type="application/json")
		except:
			HttpResponse(status=400)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def edit_site(request):
	if request.method == 'POST':
		site = Site.objects.get(pk=request.POST.get('id'))
		site.name = request.POST.get('name')
		site.save()
		return HttpResponse(status=201)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def delete_site(request):
	if request.method == 'POST':
		site = Site.objects.get(pk=request.POST.get('id'))
		site.delete()
		return HttpResponse(status=200)
	return HttpResponse(status=405)

@csrf_exempt
@login_required(login_url=LOGIN_PAGE)
def check_site_placement(request):
	point = request.POST.get('point')
	if request.method == 'POST' and point:
		site = Site(name='none', color='none', user=request.user)
		try:
			site.save()
			site._shape.add(base_map.models.Point(shape=point), bulk=False)
			site.save()
			if site.is_within():
				site_data = '''{
					"iswithin": "true",
					"pilot_area": "''' + site.is_within() + '''",
					"landmarks": "''' + site.get_closest_landmarks() + '''",
					"water_status":''' + str(site.get_water_info()) + ''',
					"sewer_status":''' + str(site.get_sewer_info()) + '''
				}'''
				site.delete()
				print site_data
				return HttpResponse(site_data, status=200, content_type='application/json')
			else:
				return HttpResponse('{ "iswithin": "false" }', status=200, content_type='application/json')
		except Exception as e:
			print e
			site.delete()
			return HttpResponse(status=500)
	return HttpResponse(status=405)