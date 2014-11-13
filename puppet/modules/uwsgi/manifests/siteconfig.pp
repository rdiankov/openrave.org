define uwsgi::siteconfig($source,$owner,$group){
  file {"/etc/uwsgi/vassals/$name":
    ensure  => present,
    source  => $source,
    owner   => $owner,
    group   => $group,
    mode    => 0644,
    require => Class['uwsgi'],
    notify  => Class["uwsgi::service"],
  }
}
