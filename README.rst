Managing openrave.org
=====================

These instructions are for installing OpenRave.org code in a standalone environment.  This library can be used in a puppet master setup, however the default path of the puppet installation would be /etc/puppetlabs/puppet.  Documentation for running a separate puppet master server can be found here: https://docs.puppetlabs.com/pe/latest/install_basic.html

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
  export FACTER_openraveorg_gitdir=`pwd`/openrave.org
  export FACTER_openraveorg_deploydir=`pwd`/openrave.org
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

3. Load documents. Make sure to add openrave documentation html and json zip files (generated via http://openrave.org/docs/latest_stable/devel/documentation_system/) to::

  cp openravehtml-latest_stable.zip $FACTER_openraveorg_deploydir/docdata/ 
  
  cp openravejson-latest_stable.zip $FACTER_openraveorg_deploydir/docdata/
  
Then register the document version via

.. code-block:: bash
 
    cd $FACTER_openraveorg_gitdir/openrave_org
    export OPENRAVE_VERSION=latest_stable
    export DOC_LANG=en
    DJANGO_SETTINGS_MODULE=openrave_org.settings python -c "from openrave_org.docs import models; models.DocumentRelease.objects.create(lang='$DOC_LANG',version='$OPENRAVE_VERSION', scm=models.DocumentRelease.GIT, scm_url='https://github.com/rdiankov/openrave/tree/v$OPENRAVE_VERSION', is_default=False);"

  Then can update docs using::
   
   ./manage.py update_docs

4. Re-index the documents::

   ./manage.py update_index

5. Run django manually to test if all data is present::

  ./manage.py runserver

Update permissions and restart
--------------------------

Run puppet apply command to update permissions for documents.
Note that uwsgi is set to run from /etc/rc.local

.. code-block:: bash

   deactivate
   sudo -E puppet apply --confdir $FACTER_openraveorg_gitdir/puppet $FACTER_openraveorg_gitdir/puppet/manifests/site.pp
   sudo service nginx restart

Visit site at port :80

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


Mini script to convert latest_stable docdata to a specific version:

  .. code-block:: bash
  
    export OPENRAVE_VERSION=0.8.0
    unzip openravejson-latest_stable.zip
    mv openravejson-latest_stable openravejson-$OPENRAVE_VERSION
    zip -r openravejson-$OPENRAVE_VERSION.zip openravejson-$OPENRAVE_VERSION
    unzip openravehtml-latest_stable.zip
    mv openravehtml-latest_stable openravehtml-$OPENRAVE_VERSION
    zip -r openravehtml-$OPENRAVE_VERSION.zip openravehtml-$OPENRAVE_VERSION

Internationalization. For Japanese, edit **locale/ja_JP/LC_MESSAGES/django.po** file::

    django-admin.py makemessages --locale=ja_JP
    django-admin.py compilemessages --locale=ja_JP

For deployment checkout fabfile.py::

    https://openrave.svn.sourceforge.net/svnroot/openrave/openrave.org/fabfile.py

Translating to Japanese
=======================

When English templates are done, execute:

.. code-block:: bash

  django-admin.py makemessages --locale=ja_JP

Open **locale/ja_JP/LC_MESSAGES/django.po** and edit the translations. When done execute:

.. code-block:: bash

  django-admin.py compilemessages --locale=ja_JP


Systemd
-------
::

2.3.4. systemd
Debian 7.0 introduces preliminary support for systemd, an init system with advanced monitoring, logging and service management capabilities.
While it is designed as a drop-in sysvinit replacement and as such makes use of existing SysV init scripts, the systemd package can be installed safely alongside sysvinit and started via the init=/bin/systemd kernel option. To utilize the features provided by systemd, about 50 packages already provide native support, among them core packages like udev, dbus and rsyslog.
systemd is shipped as a technology preview in Debian 7.0. For more information on this topic, see the Debian wiki. 

/boot/grub/grub.cfg:
add boot option with  init=/bin/systemd


--- Using system similar to djangoproject.com ---
