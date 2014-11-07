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
import os
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import get_language_from_request

if settings.IPYTHON_DEBUG:
    import IPython
    IPython.embed()
    #ipshell = IPShellEmbed(argv='',banner = 'MUJIN Controller Dropping into IPython',exit_msg = 'Leaving Interpreter.')
    #ipshell(local_ns=locals())

# enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def indexview(request,name):
    if len(name) == 0:
        name = 'index.html'

    htmlvars = dict()
    if name == 'index.html':
        gallery_intro_dir = None
        for staticdir in settings.STATICFILES_DIRS:
            if os.path.exists(os.path.join(staticdir,'img','gallery_intro')):
                gallery_intro_dir = os.path.join(staticdir,'img','gallery_intro')
                break
        if gallery_intro_dir is not None:
            LANG = get_language_from_request(request)
            if not os.path.exists(os.path.join(gallery_intro_dir,LANG)):
                LANG = 'en'
            imagefilenames = u''
            imagedirs = [gallery_intro_dir,os.path.join(gallery_intro_dir,LANG)]
            for imagedir in imagedirs:
                urldir = os.path.join(settings.STATIC_URL, os.path.relpath(imagedir,staticdir))
                for imagename in os.listdir(imagedir):
                    ext = os.path.splitext(imagename)[1].lower()
                    if ext == '.png' or ext == '.jpg':
                        imagefilenames += u'<img src="%s" width="640"/>\n'%os.path.join(urldir,imagename)
            htmlvars['intro_gallery_images'] = imagefilenames

    return render_to_response(name, RequestContext(request,htmlvars))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'openrave_org.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', indexview, {'name':'index.html'}),
    url(r'^news/$', indexview, {'name':'news.html'}),
    url(r'^dev/$', indexview, {'name':'dev.html'}),
    url(r'^(?P<name>[\w\.]+)$', indexview),
    url(r'^docs/', include('openrave_org.docs.urls')),
    url(r'^en/main/(?P<urlpath>[\w./-]*)$', 'openrave_org.docs.views.document_compat'),
    url(r'^en/coreapihtml/(?P<urlpath>[\w./-]*)$', 'openrave_org.docs.views.doxygenstatic_compat'),
    url(r'^favicon\.ico$', 'redirect', {'url': '/static/img/openrave_icon_32.png'}),
    url(r'^m/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.MEDIA_ROOT})
)
