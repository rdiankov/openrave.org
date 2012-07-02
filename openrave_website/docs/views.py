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
import datetime
import os
import django.views.static
from django.core import urlresolvers
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import get_language_from_request
from django.conf import settings

import haystack.views

from .forms import DocSearchForm
from .models import DocumentRelease
from .utils import get_doc_root_or_404, get_doc_path_or_404

from django.views.decorators.clickjacking import xframe_options_exempt

def index(request):
    return redirect(DocumentRelease.objects.default())

def document(request, version, urlpath):
    docroot,LANG = get_doc_root_or_404(version, get_language_from_request(request))
    if len(urlpath) > 0 and not urlpath.endswith('/'):
        print 'yo',version,urlpath
        return redirect('/docs/%s/%s/'%(version,urlpath))
    
    doc_path = get_doc_path_or_404(docroot, urlpath)
    template_names = ['docs/%s.html'%os.path.relpath(os.path.splitext(doc_path)[0],docroot), 'docs/doc.html']
    return render_to_response(template_names, RequestContext(request, {
        'doc': simplejson.load(open(doc_path, 'rb')),
        'env': simplejson.load(open(os.path.join(docroot, 'globalcontext.json'), 'rb')),
        'lang': LANG,
        'version': version,
        'docurl': urlpath,
        'update_date': datetime.datetime.fromtimestamp(os.stat(os.path.join(docroot,'last_build')).st_mtime),
        'home': urlresolvers.reverse('document-index', kwargs={'version':version}),
        'redirect_from': request.GET.get('from', None),
        'GET':request.GET,
    }))

class SphinxStatic(object):
    """
    Serve Sphinx static assets from a subdir of the build location.
    """
    def __init__(self, subpath):
        self.subpath = subpath

    def __call__(self, request, version, path):
        docroot,LANG = get_doc_root_or_404(version, get_language_from_request(request))
        return django.views.static.serve(request,  document_root = os.path.join(docroot, self.subpath), path = path)

@xframe_options_exempt
def doxygenstatic(request,version,path):
    docroot,LANG = get_doc_root_or_404(version, get_language_from_request(request))
    if len(path) == 0:
        path = 'index.html'
    return django.views.static.serve(request,  document_root = os.path.join(settings.MEDIA_ROOT,'openravehtml-%s'%version,LANG,'coreapihtml'), path = path)
    
def objects_inventory(request, version):
    docroot,LANG = get_doc_root_or_404(version, get_language_from_request(request))
    response = django.views.static.serve(request, document_root = docroot, path = "objects.inv")
    response['Content-Type'] = "text/plain"
    return response

def redirect_index(request, *args, **kwargs):
    assert request.path.endswith('index/')
    return redirect(request.path[:-6])

class DocSearchView(haystack.views.SearchView):
    def __init__(self, **kwargs):
        kwargs.update({'template': 'docs/search.html', 'form_class': DocSearchForm, 'load_all': False })
        super(DocSearchView, self).__init__(**kwargs)
    
    def extra_context(self):
        # Constuct a context that matches the rest of the doc page views.
        default_release = DocumentRelease.objects.default()
        return { 'lang': default_release.lang, 'version': default_release.version, 'release': default_release }
