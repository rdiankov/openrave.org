Managing OpenRave.org
=================
The code in this repository is modified from https://github.com/rdiankov/openrave.org, updated to work with Django 1.7 and Postgres 9.1. openrave.org uses Django for managing documentation, news, and blogs, similar to `djangoproject.com <https://github.com/django/djangoproject.com>`_

Install Puppet
------------------
First, install puppet.  For Debian Wheezy, use the following steps:

::

  export FACTER_localuser=www-data
  export FACTER_localgroup=www-data
  export FACTER_OPENRAVEORG_DEPLOYDIR="/var/openrave"
  export FACTER_OPENRAVEORG_PUPPETDIR="$FACTER_OPENRAVEORG_DEPLOYDIR/puppet"
  export FACTER_OPENRAVEORG_SITEDIR="$FACTER_OPENRAVEORG_DEPLOYDIR/openrave_org"

  wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb
  dpkg -i puppetlabs-release-precise.deb
  apt-get update
  apt-get install puppet


Clone Repo
------------------
Once puppet is installed, the following commands will clone this repo into your new puppet folder: /var/openrave/puppet.

::

  mkdir -p $FACTER_OPENRAVEORG_DEPLOYDIR
  git clone https://github.com/rdiankov/openrave.org.git --branch django1.7 $FACTER_OPENRAVEORG_DEPLOYDIR


Apply Puppet
------------------
Running puppet apply, will apply the manifest in a standalone setup.  Documentation found here: https://docs.puppetlabs.com/references/3.3.1/man/apply.html

::

  puppet apply $FACTER_OPENRAVEORG_PUPPETDIR/manifests/site.pp --confdir $FACTER_OPENRAVEORG_PUPPETDIR


Setup documentation
------------------
1. Go into the website directory and activate the virtual environment, then migrate with Django
::

  cd $FACTER_OPENRAVEORG_SITEDIR
  source ../../openravevenv/bin/activate
  ./manage.py makemigrations
  ./manage.py migrate

2. Load fixtures
::

   ./manage.py loaddata doc_releases.json

3. Load documents
::

   scp www-data@128.199.207.239:/var/opraveorg-tmp/docdata.tar.gz docdata.tar.gz
   tar -vxzf docdata.tar.gz
   ./manage.py update_docs

4. Re-index the documents:
::

   ./manage.py update_index


Update permissions and restart
--------------------------
Run puppet apply command to update permissions for documents
::

   deactivate
   puppet apply $FACTER_OPENRAVEORG_PUPPETDIR/manifests/site.pp --confdir $FACTER_OPENRAVEORG_PUPPETDIR

::

   init 6

Visit site at port :80

Notes
=========================
These instructions are for installing OpenRave.org code in a standalone environment.  This library can be used in a puppet master setup, however the default path of the puppet installation would be /etc/puppetlabs/puppet.  Documentation for running a separate puppet master server can be found here: https://docs.puppetlabs.com/pe/latest/install_basic.html

Help
====================
For adding new document:
::
 
    export OPENRAVE_VERSION=0.8.0
    export DOC_LANG=en
    DJANGO_SETTINGS_MODULE=openrave_org.settings python -c "from openrave_org.docs import models; models.DocumentRelease.objects.create(lang='$DOC_LANG',version='$OPENRAVE_VERSION', scm=models.DocumentRelease.GIT, scm_url='https://github.com/rdiankov/openrave/tree/v$OPENRAVE_VERSION', is_default=False);"
  

Creating PostgreSQL Database
---------------------
If you need to setup the database manually
.. code-block:: bash

  sudo -u postgres psql --command "CREATE ROLE openrave PASSWORD 'testpass' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
  createdb --host localhost --username openrave --encoding UTF-8 openrave_website

