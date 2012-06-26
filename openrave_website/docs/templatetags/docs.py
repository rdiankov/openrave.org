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
from django import template
from ..forms import DocSearchForm
from ..models import DocumentRelease
from ..utils import get_doc_root, get_doc_path

register = template.Library()

@register.inclusion_tag('docs/search_form.html', takes_context=True)
def search_form(context, search_form_id='sidebar_search'):
    auto_id = 'id_%s_%%s' % search_form_id
    release = DocumentRelease.objects.get(version=context['version'],lang=context['lang'])
    return {
        'form': DocSearchForm(initial=context.get('GET',''), auto_id=auto_id, release=release),
        'search_form_id': search_form_id,
    }

@register.tag
def get_all_doc_versions(parser, token):
    """
    Get a list of all versions of this document to link to.

    Usage: {% get_all_doc_versions <docurl> as "varname" %}
    """
    return AllDocVersionsTag.handle(parser, token)

class AllDocVersionsTag(template.Node):
    @classmethod
    def handle(cls, parser, token):
        try:
            tagname, docurl, as_, asvar = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError("Usage: {% get_all_doc_versions <docurl> as <varname> %}")
        return cls(docurl, asvar)

    def __init__(self, docurl, asvar):
        self.docurl = template.Variable(docurl)
        self.asvar = asvar
        # FIXME
        self.lang = 'en'

    def render(self, context):
        try:
            url = self.docurl.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        versions = []

        # Look for each version of the docs.
        for release in DocumentRelease.objects.all():
            version_root = get_doc_root(release.version,release.lang)
            if os.path.exists(version_root):
                doc_path = get_doc_path(version_root, url)
                if doc_path:
                    if not release.version in versions:
                        versions.append(release.version)

        # Save the versions into the context
        context[self.asvar] = sorted(versions)
        return ''
