from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'(?P<comic_id>\d+)$', 'viewer.views.comic'),
    (r'list$', 'viewer.views.list'),
    (r'random$', 'viewer.views.random'),
    (r'', 'viewer.views.comic'),
)
