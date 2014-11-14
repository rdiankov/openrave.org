
## site.pp ##

# This file (/etc/puppetlabs/puppet/manifests/site.pp) is the main entry point
# used when an agent connects to a master and asks for an updated configuration.
#
# Global objects like filebuckets and resource defaults should go in this file,
# as should the default node definition. (The default node can be omitted
# if you use the console and don't define any other nodes in site.pp. See
# http://docs.puppetlabs.com/guides/language_guide.html#nodes for more on
# node definitions.)

## Active Configurations ##

# PRIMARY FILEBUCKET
# This configures puppet agent and puppet inspect to back up file contents when
# they run. The Puppet Enterprise console needs this to display file contents
# and differences.

# Define filebucket 'main':
filebucket { 'main':
  server => 'localhost',
  path   => false,
}

# Make filebucket 'main' the default backup location for all File resources:
File { backup => 'main' }

# DEFAULT NODE
# Node definitions in this file are merged with node data from the console. See
# http://docs.puppetlabs.com/guides/language_guide.html#nodes for more on
# node definitions.

# The default node definition matches any node lacking a more specific node
# definition. If there are no other nodes in this file, classes declared here
# will be included in every node's catalog, *in addition* to any classes
# specified in the console for that node.

node default {
  include "${operatingsystem}setup"
  include git
  include ssh
  include user
  class { 'postgresql::server': }

  postgresql::server::role { 'openrave':
    password_hash => postgresql_password('openrave', 'testpass'),
    createdb      => true,
    createrole    => true,
    superuser     => true,
    inherit	      => true,
    login         => true,
  }
  postgresql::server::db { 'openrave_website':
    user     => 'openrave',
    password => postgresql_password('openrave', 'testpass'),
    encoding => 'UTF8',
    template => 'template0',
  }
  postgresql::server::pg_hba_rule { 'local access to database for all':
    description => "none",
    type        => 'local',
    database    => 'all',
    user        => 'all',
    address     => '',
    auth_method => 'md5',
    order       => '002',
  }
#  user::create {'jenkins':
#    password   => '$1$963viJj/$VUiSdG/Sjsj4bsQD1uXTX0',
#    groups     => '$localuser',
#    sshkeytype => 'ssh-rsa',
#    sshkey     => '' #ssh public key without type and user indicators  
#}

  file {"${openraveorg_deploydir}":
    ensure => directory,
    owner   => "${localuser}",
    group   => "${localgroup}",
  }~>
  file {"${openraveorg_deploydir}/openrave_org_migrations":
    ensure => directory,
    owner   => "${localuser}",
    group   => "${localgroup}",
  }~>
  file {"${openraveorg_deploydir}/openrave_org_migrations/__init__.py": 
    ensure => present, 
    owner => "${localuser}", 
    group => "${localgroup}",
    #mode => 0644, 
  }~>
  file {"${openraveorg_deploydir}/openrave_org":
    ensure  => directory,
    owner   => "${localuser}",
    group   => "${localgroup}",
    #mode    => 0774,
    recurse => true,
    ignore  => '*.sock',
  }
  
  class { 'python':
    version    => 'system',
    pip        => true,
    dev        => true,
    virtualenv => true,
    gunicorn   => false,
  }
  python::virtualenv { "${openraveorg_gitdir}/openrave_org" :
    ensure       => present,
    version      => 'system',
    requirements => "${openraveorg_gitdir}/openrave_org/requirements.txt",
    systempkgs   => true,
    distribute   => false,
    venv_dir     => "${openraveorg_deploydir}/venv",
    owner        => "${localuser}",
    group        => "${localgroup}",
    cwd          => "${openraveorg_gitdir}/openrave_org",
    timeout      => 0,
  }

  class {'nginx':
    owner       => "${localuser}",
    group       => "${localgroup}",
    confcontent => "# openrave_nginx.conf\nupstream django { server unix:///var/run/openrave_org_wsgi.sock; }\nserver {\nlisten 80;\nserver_name localhost;\ncharset utf-8;\nerror_log ${openraveorg_deploydir}/openrave_nginx_error.log;\naccess_log ${openraveorg_deploydir}/openrave_nginx_access.log;\nclient_max_body_size 75M;\nlocation /media  { alias ${openraveorg_deploydir}/openrave_org/media; }\nlocation /static { alias ${openraveorg_deploydir}/openrave_org/openrave_org/static; }\nlocation /s { alias ${openraveorg_deploydir}/openrave_org/openrave_org/static; }\nlocation / { uwsgi_pass  django; include /etc/nginx/uwsgi_params; }\n}",
  }
  
  class {'uwsgi':
    owner  => "${localuser}",
    group  => "${localgroup}",
    inidir => "${openraveorg_deploydir}/vassals",
    inicontent => "# openrave_uwsgi.ini file\n[uwsgi]\n\n# Django-related settings\nchdir = ${openraveorg_deploydir}/openrave_org/\nmodule = openrave_org.wsgi\nhome = ${openraveorg_deploydir}/venv\n\n# process-related settings\nmaster = true\nprocesses = 10\nsocket = /var/run/openrave_org_uwsgi.sock\nchmod-socket = 664\nuid = ${localuser}\ngid = ${localgroup}\ndaemonize = ${openraveorg_deploydir}/uwsgi_error.log\n\n# clear environment on exit\nvacuum = true",
  }
}


