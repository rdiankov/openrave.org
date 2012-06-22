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
from django.conf import settings
from django.http import Http404

def get_doc_root(version,lang):
    return os.path.join(settings.OPENRAVE_DOCUMENT_ROOT_PATH, version, lang, "json")
    
def get_doc_root_or_404(version,lang):
    docroot = get_doc_root(version,lang)
    if not os.path.exists(docroot):
        raise Http404(docroot)
    return docroot

def get_doc_path(docroot, subpath):
    # First look for <bits>/index.fpickle, then for <bits>.fpickle
    bits = subpath.strip('/').split('/') + ['index.fjson']
    doc = os.path.join(*bits)
    if doc.exists():
        return doc

    bits = bits[:-2] + ['%s.fjson' % bits[-2]]
    doc = os.path.join(*bits)
    if doc.exists():
        return doc
        
    return None

def get_doc_path_or_404(docroot, subpath):
    doc = get_doc_path(docroot, subpath)
    if doc is None:
        raise Http404(doc)
    return doc
