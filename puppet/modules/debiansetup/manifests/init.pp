# class debiansetup
#
# to do installs needed for debian development
#

class debiansetup{
  exec {'update apt-get':
    command => '/usr/bin/apt-get update',
  }  
  package {
	"build-essential"   : ensure => installed;
        "chkconfig"         : ensure => installed;
	"cmake"             : ensure => installed;
	"vim"               : ensure => installed;
	"libpq-dev"         : ensure => installed;
    }
}
