Managing OpenRave.org
=================
The code in this repository is modified from https://github.com/rdiankov/openrave.org, updated to work with Django 1.7 and Postgres 9.1. openrave.org uses Django for managing documentation, news, and blogs, similar to `djangoproject.com <https://github.com/django/djangoproject.com>`_

Install Puppet
------------------
First, install puppet.  For Debian Wheezy, use the following steps:

::

  wget https://apt.puppetlabs.com/puppetlabs-release-precise.deb
  dpkg -i puppetlabs-release-precise.deb
  apt-get update
  apt-get install puppet

Create environment variables from inside the working directory you want to clone into.
::

  export FACTER_localuser=$USER
  export FACTER_localgroup=$USER
  export FACTER_openraveorg_gitdir=`pwd`
  export FACTER_openraveorg_deploydir=`pwd`
  export FACTER_openraveorg_sitedir="$FACTER_openraveorg_deploydir/openrave_org"

Clone Repo
------------------
Once puppet is installed, the following commands will clone this repo into your new puppet folder: /var/openrave/puppet.

::

  git clone https://github.com/rdiankov/openrave.org.git --branch django1.7 $FACTER_openraveorg_gitdir

Apply Puppet
------------------
Running puppet apply, will apply the manifest in a standalone setup.  Documentation found here: https://docs.puppetlabs.com/references/3.3.1/man/apply.html

::

  sudo -E puppet apply --confdir $FACTER_openraveorg_gitdir/puppet $FACTER_openraveorg_gitdir/puppet/manifests/site.pp


Edit the openrave.org_secrets.json file in the deploy directoy, containing something like:

::

  { "secret_key": "xyz",
    "superfeedr_creds": ["any@email.com", "some_string"] }


Setup documentation
------------------
1. Go into the website directory and activate the virtual environment, then migrate with Django. This will set OPENRAVEORG_DEPLOYDIR environment variable.
::

  source $FACTER_openraveorg_deploydir/setup.bash
  cd $FACTER_openraveorg_gitdir/openrave_org; ./manage.py makemigrations docs
  cd $FACTER_openraveorg_gitdir/openrave_org; ./manage.py migrate

2. Load fixtures
::

   cd $FACTER_openraveorg_gitdir/openrave_org; ./manage.py loaddata doc_releases.json

3. Load documents. Make sure you add the docdata directory with zip files before updating docs::
   
   ./manage.py update_docs

4. Re-index the documents::

   ./manage.py update_index

5. Run django manually to test if all data is present::

  ./manage.py runserver

Update permissions and restart
--------------------------

Run puppet apply command to update permissions for documents

.. code-block:: bash

   deactivate
   puppet apply --confdir $FACTER_openraveorg_deploydir/puppet $FACTER_openraveorg_deploydir/puppet/manifests/site.pp
   sudo service uwsgi restart
   sudo service nginx restart

Visit site at port :80

Deployment Notes
================

These instructions are for installing OpenRave.org code in a standalone environment.  This library can be used in a puppet master setup, however the default path of the puppet installation would be /etc/puppetlabs/puppet.  Documentation for running a separate puppet master server can be found here: https://docs.puppetlabs.com/pe/latest/install_basic.html

Help
====

For adding new document.

.. code-block:: bash
 
    export OPENRAVE_VERSION=0.8.0
    export DOC_LANG=en
    DJANGO_SETTINGS_MODULE=openrave_org.settings python -c "from openrave_org.docs import models; models.DocumentRelease.objects.create(lang='$DOC_LANG',version='$OPENRAVE_VERSION', scm=models.DocumentRelease.GIT, scm_url='https://github.com/rdiankov/openrave/tree/v$OPENRAVE_VERSION', is_default=False);"

Debugging Notes
===============

 Facter Notes
-------------

.. code-block:: bash

    facter -p  #See if your evn vars are set
    
    facter apply --test
    
    facter apply  --verbose --no-listen --no-daemonize --onetime --no-splay --test --pluginsync

"--noop" is a dry run::

    sudo -E puppet apply --confdir $FACTER_openraveorg_deploydir/puppet $FACTER_openraveorg_deploydir/puppet/manifests/site.pp --test --debug --noop
    
Puppet help::
  
  puppet config print all
  puppet config print modulepath
  
  --verbose --debug --trace

Creating PostgreSQL Database
----------------------------

If you need to setup the database manually

.. code-block:: bash

  sudo -u postgres psql --command "CREATE ROLE openrave PASSWORD 'testpass' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;"
  createdb --host localhost --username openrave --encoding UTF-8 openrave_website

Systemd
-------
::

2.3.4. systemd
Debian 7.0 introduces preliminary support for systemd, an init system with advanced monitoring, logging and service management capabilities.
While it is designed as a drop-in sysvinit replacement and as such makes use of existing SysV init scripts, the systemd package can be installed safely alongside sysvinit and started via the init=/bin/systemd kernel option. To utilize the features provided by systemd, about 50 packages already provide native support, among them core packages like udev, dbus and rsyslog.
systemd is shipped as a technology preview in Debian 7.0. For more information on this topic, see the Debian wiki. 

