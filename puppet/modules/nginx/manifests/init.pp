# class nginx
# 
# installs nginx package
# and sets the config file
#
class nginx($owner='www-data',$group='www-data',$confcontent){
  include nginx::service
  nginx::install{'install-nginx':
    owner       => $owner,
    group       => $group,
    confcontent => $confcontent,
  }
}

define nginx::install($owner,$group,$confcontent) {
  package {'nginx':
    ensure =>present,
  }
  file {"/etc/nginx/conf.d":
    ensure  => directory,
  }~>
  file {"/etc/nginx/conf.d/openrave_nginx.conf":
    ensure  => present,
    content => $confcontent,
    owner   => $owner,
    group   => $group,
    mode    => 0644,
    notify  => Class["nginx::service"],
  }
}

class nginx::service{
  service {'nginx':
    ensure  => running,
    require => Package['nginx'],
  }
}

Class['nginx'] -> Class["nginx::service"]
