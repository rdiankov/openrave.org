# class uwsgi
# 
# installs uwsgi package
# and sets the config file
#
class uwsgi ($owner='www-data',$group='www-data',$inidir,$inicontent) {
  include uwsgi::service
  uwsgi::install{'install-uwsgi':
    owner => $owner,
    group => $group,
    inidir => $inidir,
    inicontent => $inicontent,
  }
}

define uwsgi::install($owner,$group,$inidir,$inicontent) {
  python::pip {'uwsgi':
    pkgname => 'uwsgi', 
  }

  file {"$inidir":
    ensure => directory,
    owner => $owner,
    group => $group,
  }~>
  file {"$inidir/uwsgi.ini":
    ensure  => present,
    content => $inicontent,
    owner   => $owner,
    group   => $group,
    mode    => 0644,
    notify  => Class["uwsgi::service"],
  }
  file {"$inidir/uwsgi":
    ensure => directory,
    owner  => $owner,
    group  => $group,
    mode   => 0644,
  }

  concat {"/etc/rc.local":
    #ensure => present,
    mode    => 0755,
  } 
  concat::fragment {'00_rc.local_header':
    target  => '/etc/rc.local',
    content => "#!/bin/sh -e \n# This file is managed by Puppet. \n\n",
    order   => '01',
  }
  concat::fragment {'02_rc.local_custom':
    target => '/etc/rc.local',
    content => "/usr/local/bin/uwsgi --emperor $inidir --uid ${localuser} --gid ${localgroup} --env FACTER_openraveorg_deploydir=${openraveorg_deploydir}\n",
    order  => '02',
  }
  concat::fragment {'99_rc.local_footer':
    target  => '/etc/rc.local',
    content => "exit 0\n",
    order   => '99',
  }
}

class uwsgi::service{
  #service {'uwsgi':
  #  ensure  => running,
  #  require => Package['uwsgi'],
  #}
}

Class['uwsgi'] -> Class["uwsgi::service"]
