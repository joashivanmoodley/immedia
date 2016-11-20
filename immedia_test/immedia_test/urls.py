
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.conf import settings

from image.views import view_locations, list_images, view_image
'''
All URLS defined below, ULRL points to related imported function definition. 
'''
urlpatterns = [
    url(r'^$', view_locations),
    url(r'^(?P<location_id>\d+)/images/$', list_images),
    url(r'^images/(?P<image_id>\d+)/$', view_image),
    url(r'^html/(?P<path>.*)$', serve, {'document_root': settings.TEMPLATES[0]['DIRS'][0]}),
    url(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
