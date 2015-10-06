from django.conf.urls import patterns, include, url
from django.contrib import admin
from stranke4 import views, urls3
from lists import views as views_lists


urlpatterns = patterns('',
    # Examples:
    url(r'^stranket/', include('urls3', namespace='strankex', app_name='stranke4')),
    url(r'^strankez/', include('urls3', namespace='strankey', app_name='stranke4')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^$', views.redirekt, name='redirekt'),
    )
    