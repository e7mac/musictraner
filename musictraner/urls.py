from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       
                       (r'^$', 'tunes.views.main_page'),
                       (r'^contact/$', 'tunes.views.contact'),
                       (r'^links/$', 'tunes.views.links'),
                       
                       (r'^accounts/login/$', 'django.contrib.auth.views.login'),
                       (r'^accounts/logout/$', 'tunes.views.logout_page'),
                       (r'^accounts/register/$', 'tunes.views.register_page'),
                       (r'^accounts/profile/$', 'tunes.views.main_page'),
                       (r'^([\w\d]+)/', include('tunes.urls')),                       
                       )
