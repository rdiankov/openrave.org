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
import json
from django.conf import settings
from django.utils.html import strip_tags
import haystack
import haystack.indexes
from . import utils
from .models import Document

class DocumentIndex(haystack.indexes.SearchIndex):
    text = haystack.indexes.CharField(document=True)
    lang = haystack.indexes.CharField(model_attr='release__lang', faceted=True)
    version = haystack.indexes.CharField(model_attr='release__version', faceted=True)
    path = haystack.indexes.CharField(model_attr='path')
    title = haystack.indexes.CharField(model_attr='title')

    def get_queryset(self):
        return Document.objects.all().select_related('release')

    def prepare_text(self, obj):
        root = utils.get_doc_root(obj.release.version,obj.release.lang)
        docpath = utils.get_doc_path(root, obj.path)
        with open(docpath) as fp:
            doc = json.load(fp)
        return strip_tags(doc['body']).replace(u'¶', '')

haystack.site.register(Document, DocumentIndex)
