# -*- coding: utf-8 -*-
# Copyright (C) 2012 OpenRAVE, djangoproject.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.conf.urls.defaults import *
from django.conf import settings

from haystack.views import search_view_factory
from . import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^/$', views.index),
    url(r'^search/$', search_view_factory(view_class=views.DocSearchView), name = 'document-search'),
    url(r'^(?P<version>[\w.-]+)/$', views.document, {'urlpath': ''}, name = 'document-index'),
    url(r'^(?P<version>[\w.-]+)/_objects/$', views.objects_inventory, name = 'objects-inv'),
    url(r'^(?P<version>[\w.-]+)/_images/(?P<path>.*)$', views.SphinxStatic('_images')),
    url(r'^(?P<version>[\w.-]+)/_source/(?P<path>.*)$', views.SphinxStatic('_sources')),
    url(r'^(?P<version>[\w.-]+)/_downloads/(?P<path>.*)$', views.SphinxStatic('_downloads')),
    url(r'^(?P<version>[\w.-]+)/coreapihtml/(?P<path>.*)$', views.doxygenstatic),
    url(r'^(.*)/index/$', views.redirect_index),
    url(r'^(?P<version>[\w.-]+)/(?P<urlpath>[\w./-]*)$', views.document, name = 'document-detail'),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}))
