import os
from fabric.api import *
from fabric.contrib import files

# Fab settings
env.hosts = ['openrave.org']

# Deployment environment paths and settings and such.
env.deploy_base = '/var/openrave'
env.virtualenv = '/usr/local'
env.code_dir = os.path.join(env.deploy_base, 'openrave.org_svn')
env.svn_url = 'https://openrave.svn.sourceforge.net/svnroot/openrave/openrave.org'

def full_deploy():
    """
    Full deploy: new code, update dependencies, migrate, and restart services.
    """
    deploy_code()
    update_dependencies()
    migrate()
    apache("restart")
    memcached("restart")

def deploy():
    """
    Quick deploy: new code and an in-place reload.
    """
    deploy_code()
    apache("reload")

def apache(cmd):
    """
    Manage the apache service. For example, `fab apache:restart`.
    """
    sudo('invoke-rc.d apache2 %s' % cmd)

def memcached(cmd):
    """
    Manage the memcached service. For example, `fab apache:restart`.
    """
    sudo('invoke-rc.d memcached %s' % cmd)

def deploy_code(ref=None):
    """
    Update code on the servers from Git.
    """
    puts("Deploying")
    if not files.exists(env.code_dir):
        run('svn checkout %s %s'%(env.svn_url,env.code_dir))
    with cd(env.code_dir):
        run('svn update')
    run('rm -rf %s'%os.path.join(env.deploy_base,'staticnew'))
    run('svn export %s %s'%(os.path.join(env.code_dir,'openrave_website','static'), os.path.join(env.deploy_base,'staticnew')))
    run('rm -rf %s; mv %s %s'%(os.path.join(env.deploy_base,'static'), os.path.join(env.deploy_base,'staticnew'), os.path.join(env.deploy_base,'static')))
    # have to chown/chmod docdata for searching
    sudo('chown -R $USER:www-data %s'%os.path.join(env.code_dir,'docdata'))
    sudo('chmod -R g+w %s'%os.path.join(env.code_dir,'docdata'))

def update_dependencies():
    """
    Update dependencies in the virtualenv.
    """
    pip = os.path.join(env.virtualenv,'bin', 'pip')
    reqs = os.path.join(env.code_dir, 'deploy-requirements.txt')
    sudo('%s -q install -U pip' % pip)
    sudo('%s -q install -r %s' % (pip, reqs))

def migrate():
    """
    Run migrate/syncdb.
    """
    managepy('syncdb')
    managepy('migrate')
    managepy('compilemessages --locale=ja_JP')

def update_docs():
    """
    Force an update of the docs on the server.
    """
    managepy('update_docs -v2')

def copy_db():
    """
    Copy the production DB locally for testing.
    """
    local('ssh %s pg_dump -U openrave -c openrave_website | psql openrave_website ' % env.hosts[0])

def copy_docs():
    """
    Copy build docs locally for testing.
    """
    local('rsync -av --delete --exclude=.svn %s:%s/ /tmp/openravedocs/' %(env.hosts[0], env.deploy_base.child('docbuilds')))

def managepy(cmd):
    """
    Helper: run a management command remotely.
    """
    django_admin = os.path.join(env.virtualenv, 'bin', 'django-admin.py')
    run('%s %s --settings=openrave_website.settings' % (django_admin, cmd))

def southify(app):
    """
    Southify an app remotely.

    This fakes the initial migration and then migrates forward. Use it the first
    time you do a deploy on app that's been newly southified.
    """
    managepy('migrate %s 0001 --fake' % app)
    managepy('migrate %s' % app)
