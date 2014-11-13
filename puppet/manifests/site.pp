
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
  server => 'puppetmaster',
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
  include nginx
  include uwsgi

  class { 'postgresql::server': }

  postgresql::server::role { 'openrave':
    password_hash => postgresql_password('openrave', 'testpass'),
    createdb      => true,
    createrole    => true,
    superuser     => true,
    inherit	  => true,
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
#    sshkey     => 'AAAAB3NzaC1yc2EAAAADAQABAAABAQC8EmeGfKH2vIfoGzaBOJUuns6SoYUdvouXqETChF/tzlcTMfKFdvsHUCJMDs8h3WnEiIwqWTSlyIKVYYvsI6EXPu94lILh4Dg668oaTl34YAw1h0GLAEBgjQXlSNRbm6jVvsHeEUHbtvr5VcSyKDFGbfkpp2Cz7iOzi8G2IjXLqiP6VZcVuo12CBlJgNaeke8TvL0soFcFa9aWRPa/tp/NApgj5fafKlC6TUdqh7j/ZbcyKh+flOGtcWzFCt7R6KkbEJZUc4L5a/hwO4iMEWWHMwI6ANWYDXEW2qLA4H8mVrvgm3PfFdPsOQlTSZIiGRqQLrf3sDUgHUOqdW8eges3',
#    #sshkey     => '' #ssh public key without type and user indicators  
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
 
  nginx::siteconfig {'openrave_nginx.conf':
    source => 'puppet:///modules/nginx/openrave_nginx.conf',
    owner  => "${localuser}",
    group  => "${localgroup}"
  }
  uwsgi::siteconfig{'openrave_uwsgi.ini':
    source => 'puppet:///modules/uwsgi/openrave_uwsgi.ini',
    owner  => "${localuser}",
    group  => "${localgroup}",
  }
}

