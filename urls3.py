from django.conf.urls import patterns, include, url
from django.contrib import admin
from stranke4 import views
from lists import views as views_lists


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.stranke, name='stranke'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^nova', views.MyRegistrationiew.as_view(), name='nova'),
    url(r'^stranka/(?P<stranka_id>\d+)/$', views.stranka, name='stranka'),
    url(r'^stranke', views.stranke, name='stranke'),
    #url(r'^obisk/(?P<stranka_id>\d+)$', views.obisk, name='obisk'),
    url(r'^pokazi_listo/', views.pokazi_listo, name='pokazi_listo'),
    url(r'^filtriraj_obiske/(?P<stranka_id>\d+)/$', views.filtriraj_obiske, name='filtriraj_obiske'),
    url(r'^obiski_med_datumoma/(?P<stranka_id>\d+)$', views.filtriraj_obiske, name='obiski_med_datumoma'),
    url(r'^pokazi_skladisce/', views.pokazi_skladisce, name='pokazi_skladisce'),
    url(r'^dodaj_produkt/', views.dodaj_produkt, name='dodaj_produkt'),
    url(r'^validacija/(?P<stranka_id>\d+)$', views.validacija, name='validacija'),
    #url(r'^index/$', views.prijava,
    #                       {'template_name': 'polls/index.html'},
    #                       name='auth_login'),
    url(r'^odjava', views.odjava, name='odjava'),
    url(r'^trest/$', views_lists.home_page, name='home_page'),
    



    )

