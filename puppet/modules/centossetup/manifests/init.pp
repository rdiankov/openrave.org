# class centossetup
#
# to do yum installs needed for centos development
#

class centossetup {
  exec {
    'yum update'             : command => '/usr/bin/yum -y update';
    'yum install development': command => '/usr/bin/yum groupinstall -y development';
    'easy_install pip'       : path => "/usr/local/bin:/usr/bin:/bin",
                               refreshonly => true,
                               require => Package["python-setuptools"],
                               subscribe => Package["python-setuptools"];
  }

  package {
    "epel-release"     : ensure   => installed, 
                         source   => "http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm",
                         provider => rpm;
    "zlib-devel"       : ensure   => installed;
    "openssl-devel"    : ensure   => installed;
    "sqlite-devel"     : ensure   => installed;
    "bzip2-devel"      : ensure   => installed;
    "python"           : ensure   => present;
    "python-devel"     : ensure   => present;
    "python-setuptools": ensure   => installed;
  }
}
