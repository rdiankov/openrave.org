# class openrave
#
# This class installs all of the necessary packages for OpenRave and Collada support
#
#

class openrave {
  package{
    'libboost-python-dev'        : ensure => installed;
    'python-numpy'               : ensure => installed;
    'ipython'                    : ensure => installed;
    'g++'                        : ensure => installed;
    'libqt4-dev'                 : ensure => installed;
    'qt4-dev-tools'              : ensure => installed;
    'ffmpeg'                     : ensure => installed;
    'libavcodec-dev'             : ensure => installed;
    'libavformat-dev'            : ensure => installed;
    'libxvidcore-dev'            : ensure => installed;
    'libx264-dev'                : ensure => installed;
    'libogg-dev'                 : ensure => installed;
    'libvorbis-dev'              : ensure => installed;
    'libgsm1-dev'                : ensure => installed;
    'libboost-dev'               : ensure => installed;
    'libboost-regex-dev'         : ensure => installed;
    'libxml2-dev'                : ensure => installed;
    'libglew-dev'                : ensure => installed;
    'libboost-graph-dev'         : ensure => installed;
    'libboost-wave-dev'          : ensure => installed;
    'libboost-serialization-dev' : ensure => installed;
    'libboost-filesystem-dev'    : ensure => installed;
    'libpcre3-dev'               : ensure => installed;
    'libboost-thread-dev'        : ensure => installed;
    'libmpfr-dev'                : ensure => installed;
    'libboost-date-time-dev'     : ensure => installed;
    'libqhull-dev'               : ensure => installed;
    'libswscale-dev'             : ensure => installed;
    'libode-dev'                 : ensure => installed;
    'libsoqt4-dev'               : ensure => installed;
    'libassimp-dev'              : ensure => installed;
    'python-scipy'               : ensure => installed;
    'python-matplotlib'          : ensure => installed;
    'ipython-notebook'          : ensure => installed;
    'python-pandas'              : ensure => installed;
    'python-sympy'               : ensure => installed;
    'python-nose'                : ensure => installed;
    'python-software-properties' : ensure => installed;
  }~>
  #clone collada-dom code into the server
  git::clone {'collada-dom':
    repo => 'https://github.com/rdiankov/collada-dom.git',
    path => '/root',
    dir  => 'collada-dom',
  }~>
  file {'/root/collada-dom/build':
    ensure => directory,
  }~>
  exec {'install collada':
    command => '/usr/bin/cmake .. && /usr/bin/make && /usr/bin/make install',
    cwd     => '/root/collada-dom/build',
    onlyif  => '/usr/bin/test /root/collada-dom/build/Makefile && echo 0 || echo 1', #only if dir is NOT there
    timeout => 6000,
  }~>
  git::clone {'openrave':
    repo   => 'https://github.com/rdiankov/openrave.git',
    branch => 'latest_stable',
    path => '/root',
    dir    => 'openrave',
  }~>
  exec {'install openrave':
    command => '/usr/bin/make && /usr/bin/make install',
    cwd     => '/root/openrave',
    onlyif  => '/usr/bin/test /usr/local/bin/openrave && echo 0 || echo 1', #only if dir is NOT there
    timeout => 3000,
  }
}
