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
from django.conf import settings
from django.core.cache import cache
from openrave_website.models import DocumentRelease

if settings.IPYTHON_DEBUG:
   from IPython.Shell import IPShellEmbed
   
def recent_release(request):
    recent_release = cache.get('recent_release')
    try:
        if not recent_release:
            recent_release = DocumentRelease.objects.default().version
            cache.set(DocumentRelease.DEFAULT_CACHE_KEY, recent_release, settings.CACHE_MIDDLEWARE_SECONDS)
        return {'RECENT_RELEASE': recent_release}
    except DocumentRelease.DoesNotExist:
        return {}
    
