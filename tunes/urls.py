from django.conf.urls import patterns, include, url
from tunes.models import *

import views

urlpatterns = patterns('',

                       url(r'^tunes/add/$', views.add_tune, name='tunes-add'),
                       url(r'^tunes/remove/(\d+)/$', views.remove_tune, name='tunes-remove'),
                       url(r'^tunes/edit/(\d+)/$', views.edit_tune, name='tunes-edit'),
                       url(r'^tunes/(\d+)/$', views.show_tune, name='tunes-show'),
                       url(r'^tunes/$', views.list_tunes, name='tunes-list'),
                       
                       url(r'^concepts/$', views.list_concepts, name='concepts-list'),
                       url(r'^concepts/add/$', views.add_concept, name='concepts-add'),
                       url(r'^concepts/remove/(\d+)/$', views.remove_concept, name='concepts-remove'),
                       url(r'^concepts/edit/(\d+)/$', views.edit_concept, name='concepts-edit'),
                       url(r'^concepts/(\d+)/$', views.show_concept, name='concepts-show'),
                       
                       url(r'^resources/add/$', views.add_resource, name='resources-add'),
                       url(r'^resources/$', views.list_resources, name='resources-list'),
                       url(r'^resources/remove/(\d+)/$', views.remove_resource, name='resources-remove'),
                       url(r'^resources/edit/(\d+)/$', views.edit_resource, name='resources-edit'),
                       url(r'^resources/(\d+)/$', views.show_resource, name='resources-show'),

#                      url(r'^download/(?P<path>.*)$', 'django.views.static.serve',                           {'document_root': settings.MEDIA_ROOT}, name=''),

                        )
