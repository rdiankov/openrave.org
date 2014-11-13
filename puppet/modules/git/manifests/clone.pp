define git::clone ($repo, $branch='master', $path, $dir){
  exec { "clone-$name-$path":
    command => "/usr/bin/git clone --branch $branch $repo $path/$dir",
    creates => "$path/$dir",
    require => Class["git"],
    onlyif  => "/usr/bin/test -d $path/$dir && echo 0 || echo 1", #only if dir is NOT there
  }
}
