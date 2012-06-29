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
"""
Update and build the documentation into files for display with the openravedocs
app.
"""
import os
import json
import haystack
import optparse
import subprocess
import zipfile
import sphinx.cmdline
import shutil
from contextlib import closing
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.utils.html import strip_tags
from django.utils.text import unescape_entities
from unipath import FSPath as Path
from ...models import DocumentRelease, Document

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        optparse.make_option(
            '--skip-indexing',
            action='store_false',
            dest='reindex',
            default=True,
            help='Skip reindexing (for testing, mostly).'
        ),
    )

    def UncompressHTML(self,release):
        """uncompress the html files into MEDIA_ROOT
        """
        zipfilename = os.path.join(settings.OPENRAVE_DOCUMENT_ROOT_PATH,'openravehtml-%s.zip'%release.version)
        if not os.path.exists(zipfilename):
            print 'failed to find zipfile',zipfilename
            return

        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT,'docs'))
        except OSError:
            pass
        
        zipfiledir = os.path.join(settings.MEDIA_ROOT,'openravehtml-%s'%release.version)
        destzipfile = os.path.join(settings.MEDIA_ROOT,'docs','openravehtml-%s.zip'%release.version)
        docsdir = os.path.join(zipfiledir,release.lang,'coreapihtml')

        douncompress = True
        if os.path.exists(zipfiledir) and os.path.exists(docsdir):
            # check if timestamps of zipfile and dir match
            douncompress = os.stat(zipfiledir).st_mtime < os.stat(zipfilename).st_mtime

        if douncompress:
            print 'uncompressing',zipfilename
            try:
                zf = zipfile.ZipFile(zipfilename, 'r')
            except IOError,e:
                print e
                return

            for files in zf.namelist():
                zf.extract(files, settings.MEDIA_ROOT)
            zf.close()
            # have to touch zipfiledir incase zip file did not overwrite its timestamp
            os.utime(zipfiledir, None)

        if not os.path.exists(destzipfile) or os.stat(destzipfile).st_mtime < os.stat(zipfilename).st_mtime:
            print 'copying',zipfilename
            shutil.copyfile(zipfilename,destzipfile)
            
    def handle_noargs(self, **kwargs):
        try:
            verbosity = int(kwargs['verbosity'])
        except (KeyError, TypeError, ValueError):
            verbosity = 1

        # Somehow, bizarely, there's a bug in Sphinx such that if I try to
        # build 1.0 before other versions, things fail in weird ways. However,
        # building newer versions first works. I suspect Sphinx is hanging onto
        # some global state. Anyway, we can work around it by making sure that
        # "dev" builds before "1.0". This is ugly, but oh well.
        for release in DocumentRelease.objects.order_by('-version'):
            self.UncompressHTML(release)

            if verbosity >= 1:
                print "Updating %s..." % release

            zipfilename = os.path.join(settings.OPENRAVE_DOCUMENT_ROOT_PATH,'openravejson-%s.zip'%release.version)
            if not os.path.exists(zipfilename):
                print 'failed to find zipfile',zipfilename
                continue
            
            zipfiledir = os.path.splitext(zipfilename)[0]
            docsdir = os.path.join(zipfiledir,release.lang,'sphinxjson')

            douncompress = True
            if os.path.exists(zipfiledir) and os.path.exists(docsdir):
                # check if timestamps of zipfile and dir match
                douncompress = os.stat(zipfiledir).st_mtime < os.stat(zipfilename).st_mtime
            
            if douncompress:
                print 'uncompressing',zipfilename
                try:
                    zf = zipfile.ZipFile(zipfilename, 'r')
                except IOError,e:
                    print e
                    continue

                for files in zf.namelist():
                    zf.extract(files, settings.OPENRAVE_DOCUMENT_ROOT_PATH)
                zf.close()
                # have to touch zipfiledir incase zip file did not overwrite its timestamp
                os.utime(zipfiledir, None)

            # check if the language exists
            if not os.path.exists(docsdir):
                print 'language dir does not exist',docsdir
                continue
            
            #
            # Rebuild the imported document list and search index.
            #
            if not kwargs['reindex']:
                continue

            if verbosity >= 2:
                print "  reindexing...",release.version

            # Build a dict of {path_fragment: document_object}. We'll pop values
            # out of this dict as we go which'll make sure we know which
            # remaining documents need to be deleted (and unindexed) later on.
            documents = dict((doc.path, doc) for doc in release.documents.all())

            # Walk the tree we've just built looking for ".fjson" documents
            # (just JSON, but Sphinx names them weirdly). Each one of those
            # documents gets a corresponding Document object created which
            # we'll then ask Sphinx to reindex.
            #
            # We have to be a bit careful to reverse-engineer the correct
            # relative path component, especially for "index" documents,
            # otherwise the search results will be incorrect.
            for dirpath, dirnames, filenames in os.walk(docsdir):
                for filename in filenames:
                    basename,ext = os.path.splitext(filename)
                    if ext == '.fjson':
                        # Convert into a relative path for inclusion into the model                        
                        if basename == 'index':
                            path = os.path.normpath(os.path.relpath(dirpath,docsdir))
                        else:
                            path = os.path.normpath(os.path.relpath(os.path.join(dirpath,basename),docsdir))
                        with open(os.path.join(dirpath,filename)) as fp:
                            json_doc = json.load(fp)
                            try:
                                json_doc['body']  # Just to make sure it exists.
                                title = unescape_entities(strip_tags(json_doc['title']))
                            except KeyError, ex:
                                if verbosity >= 2:
                                    print "Skipping: %s (no %s)" % (path, ex.args[0])
                                continue
                            
                        doc = documents.pop(path, Document(path=path, release=release))
                        doc.title = title
                        doc.save()
                        haystack.site.update_object(doc)

            # Clean up any remaining documents.
            for doc in documents.values():
                if verbosity >= 2:
                    print "Deleting:", doc
                haystack.site.remove_object(doc)
                doc.delete()

#     def update_svn(self, url, destdir):
#         subprocess.call(['svn', 'checkout', '-q', url, destdir])
# 
#     def update_git(self, url, destdir):
#         if '@' in url:
#             repo, branch = url.rsplit('@', 1)
#         else:
#             repo, branch = url, 'master'
#         if destdir.child('.git').exists():
#             try:
#                 cwd = os.getcwdu()
#                 os.chdir(destdir)
#                 subprocess.call(['git', 'reset', '--hard', 'HEAD'])
#                 subprocess.call(['git', 'pull'])
#             finally:
#                 os.chdir(cwd)
#         else:
#             subprocess.call(['git', 'clone', '-q', '--branch', branch, repo, destdir])
