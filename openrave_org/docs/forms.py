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
import haystack.forms
from django import forms
from .models import DocumentRelease

# Right now this just does version because we don't really have
# multiple languages. If we get them, we'll need to deal with that.
class DocSearchForm(haystack.forms.SearchForm):
    def __init__(self, *args, **kwargs):
        initial_rel = kwargs.pop('release', DocumentRelease.objects.default())
        super(DocSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget = SearchInput()
        self.fields['release'] = DocumentReleaseChoiceField(queryset = DocumentRelease.objects.all().order_by('version'), initial = initial_rel, empty_label = None, required = False)

    def search(self):
        sqs = super(DocSearchForm, self).search()
        if self.is_valid():
            rel = self.cleaned_data['release'] or DocumentRelease.objects.default()
            sqs = sqs.filter(lang=rel.lang, version=rel.version)
        return sqs

class DocumentReleaseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.human_version

class SearchInput(forms.TextInput):
    input_type = 'search'
