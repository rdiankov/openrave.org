define nginx::siteconfig($source,$owner,$group){
  file {"/etc/nginx/conf.d/$name":
    ensure  => present,
    source  => $source,
    owner   => $owner,
    group   => $group,
    mode    => 0644,
    require => Class['nginx'],
    notify  => Class["nginx::service"],
  }
}
