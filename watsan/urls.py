from django.conf.urls import *
from django.contrib import admin, admindocs
from django.views.generic import RedirectView, TemplateView
admin.autodiscover()
    
urlpatterns = patterns('',
    url(r'^landing/$', TemplateView.as_view(template_name="watsan/landing.html"), name='watsan_landing'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'watsan/registration/login.html'},  name='watsan_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'watsan/registration/login.html'}, name='watsan_logout' ),
    url(r'^$', RedirectView.as_view(url='/watsan/dashboard'), name='watsan_home'),

    url(r'^dashboard/$', 'watsan.views.dashboard', name='watsan_dashboard'),
    (r'^map/(?P<projectId>[0-9]*)$', 'watsan.views.map'),
    (r'^project/(?P<projectId>[0-9]*)$', 'watsan.views.project'),
    (r'^ncwsc/(?P<projectId>[0-9]*)$', 'watsan.views.ncwsc'),
    (r'^alts/(?P<projectId>[0-9]*)$', 'watsan.views.alts'),

    url(r'^register/$', RedirectView.as_view(url='/watsan/register/org'), name='watsan_register'),
    url(r'^register/org/$', 'watsan.views.register_org', name='watsan_register_org'),
    url(r'^register/user/$', 'watsan.views.register_user', name='watsan_register_user'),
    url(r'^register/final/$', 'watsan.views.register_final', name='watsan_register_final'),

    (r'^password_reset/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'watsan/password_reset/password_reset.html',
        'post_reset_redirect': '/watsan/password_reset_done/'}),
    (r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'watsan/password_reset/password_reset_done.html'}),
    (r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'watsan/password_reset/password_reset_complete.html'}),
    (r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/watsan/password_reset_complete', 'template_name': 'watsan/password_reset/password_reset_confirm.html'}),

    (r'^about/$', 'watsan.views.about'),
    (r'^settings/$', 'watsan.views.settings'),
    (r'^settings/password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'watsan/dashboard/password_change.html'}),
    (r'^settings/password_change_done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'watsan/dashboard/password_change_done.html'}),
    (r'^settings/change_user_name/$', 'watsan.views.change_user_name'),
    (r'^settings/change_user_email/$', 'watsan.views.change_user_email'),
    (r'^settings/change_user_email_complete/(?P<hash_string>[0-9A-Za-z]+)/$', 'watsan.views.change_user_email_complete'),
    
    (r'^saveLandmark/$', 'watsan.views.save_landmark'),
    (r'^saveSearchString/$', 'watsan.views.save_search_string'), 
    (r'^map/site/save/$', 'watsan.views.save_site'),
    (r'^map/site/edit/$', 'watsan.views.edit_site'),
    (r'^map/site/delete/$', 'watsan.views.delete_site'),
    (r'^map/check_site/$', 'watsan.views.check_site_placement'),
    (r'^project/save/$', 'watsan.views.save_project'),
)