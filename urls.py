from django.conf.urls.defaults import *
import os.path

from feeds import *

css_root = os.path.join(os.path.dirname(__file__),"media/css")
img_root = os.path.join(os.path.dirname(__file__),"media/images")
comic_root = os.path.join(os.path.dirname(__file__),"comics/")

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
  'latest': LatestComics, 
}

urlpatterns = patterns('',
    # Example:
    # (r'^robotkitten/', include('robotkitten.foo.urls')),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': css_root}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': img_root}),
    (r'^comics/(?P<path>.*)$', 'django.views.static.serve',
                              {'document_root': comic_root}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
                              {'feed_dict':feeds}),
    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    (r'', include('robotkitten.viewer.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
