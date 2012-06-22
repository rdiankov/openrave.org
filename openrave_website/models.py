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
from django.db import models
from django.conf import settings
from django.core.cache import cache

from django.utils.translation import ugettext_lazy as _

class DocumentReleaseManager(models.Manager):
    def default(self):
        return DocumentRelease.objects.get(is_default=True)

class DocumentRelease(models.Model):
    """
    A "release" of documentation -- i.e. English for v1.2.
    """
    DEFAULT_CACHE_KEY = "%s_recent_release" % settings.CACHE_MIDDLEWARE_KEY_PREFIX
    SVN = 'svn'
    GIT = 'git'
    SCM_CHOICES = ( (SVN, 'SVN'), (GIT, 'git') )

    lang = models.CharField(max_length=2, choices=settings.LANGUAGES, default='en')
    version = models.CharField(max_length=20)
    scm = models.CharField(max_length=10, choices=SCM_CHOICES)
    scm_url = models.CharField(max_length=200)
    docs_subdir = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField()

    objects = DocumentReleaseManager()

    def __unicode__(self):
        return "%s/%s" % (self.version,self.lang)

    @models.permalink
    def get_absolute_url(self):
        return ('document-index', [], {'version': self.version, 'lang': self.lang})

    def save(self, *args, **kwargs):
        # There can be only one. Default, that is.
        if self.is_default:
            DocumentRelease.objects.update(is_default=False)
            cache.set(self.DEFAULT_CACHE_KEY, self.version, settings.CACHE_MIDDLEWARE_SECONDS)
        super(DocumentRelease, self).save(*args, **kwargs)

    @property
    def human_version(self):
        """
        Return a "human readable" version of the version.
        """
        return _('Latest Stable') if self.version == 'latest_stable' else 'OpenRAVE %s'%self.version

class Document(models.Model):
    """
    An individual document. Used mainly as a hook point for Haystack.
    """
    release = models.ForeignKey(DocumentRelease, related_name='documents')
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=500)

    def __unicode__(self):
        return "/".join([self.release.version, self.release.lang, self.path])

    @models.permalink
    def get_absolute_url(self):
        kwargs = {
            'version': self.release.version,
            'lang': self.release.lang,
            'url': self.path
        }
        return ('document-detail', [], kwargs)
