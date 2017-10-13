from django.conf.urls import *
from django.contrib import admin, admindocs
from django.contrib.auth.views import logout, login, password_reset, password_reset_done, password_reset_complete, password_reset_confirm
from django.views.generic import RedirectView, TemplateView
from watsan.views import *

admin.autodiscover()
    
urlpatterns = [
    url(r'^landing/$', TemplateView.as_view(template_name="landing.html"), name='watsan_landing'),
    url(r'^login/$', login, {'template_name': 'registration/login.html'},  name='watsan_login'),
    url(r'^logout/$', logout, {'template_name': 'registration/login.html'}, name='watsan_logout' ),
    url(r'^$', RedirectView.as_view(url='/dashboard'), name='watsan_home'),

    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^map/(?P<projectId>[0-9]*)$', the_map),
    url(r'^project/(?P<projectId>[0-9]*)$', project),
    url(r'^ncwsc/(?P<projectId>[0-9]*)$', ncwsc),
    url(r'^alts/(?P<projectId>[0-9]*)$', alts),

    url(r'^register/$', RedirectView.as_view(url='/register/org'), name='watsan_register'),
    url(r'^register/org/$', register_org, name='watsan_register_org'),
    url(r'^register/user/$', register_user, name='watsan_register_user'),
    url(r'^register/final/$', register_final, name='watsan_register_final'),

    url(r'^password_reset/$', password_reset,
        {'template_name': 'password_reset/password_reset.html',
        'post_reset_redirect': '/watsan/password_reset_done/'}),
    url(r'^password_reset_done/$', password_reset_done, {'template_name': 'password_reset/password_reset_done.html'}),
    url(r'^password_reset_complete/$', password_reset_complete, {'template_name': 'password_reset/password_reset_complete.html'}),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, 
        {'post_reset_redirect' : '/watsan/password_reset_complete', 'template_name': 'password_reset/password_reset_confirm.html'}),

    url(r'^about/$', about, name='about'),
    url(r'^settings/$', settings, name='settings'),
    #(r'^settings/password_change/$', password_change, {'template_name': 'watsan/dashboard/password_change.html'}),
    #(r'^settings/password_change_done/$', password_change_done, {'template_name': 'watsan/dashboard/password_change_done.html'}),
    url(r'^settings/change_user_name/$', change_user_name),
    url(r'^settings/change_user_email/$', change_user_email),
    url(r'^settings/change_user_email_complete/(?P<hash_string>[0-9A-Za-z]+)/$', change_user_email_complete),
    
    url(r'^saveLandmark/$', save_landmark),
    url(r'^saveSearchString/$', save_search_string), 
    url(r'^map/site/save/$', save_site),
    url(r'^map/site/edit/$', edit_site),
    url(r'^map/site/delete/$', delete_site),
    url(r'^map/check_site/$', check_site_placement),
    url(r'^project/save/$', save_project),
    url(r'^admin/', admin.site.urls)
]