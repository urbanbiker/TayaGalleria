from django.conf.urls.defaults import *

urlpatterns = patterns('galleries.views',
    url(r'^(?P<slug>[a-zA-Z0-9_.-]+)/$', 'galleria_detail',  name='galleria'),
)
