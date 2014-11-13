require 'facter'
Facter.add(:localuser) do
    setcode do
	Facter::Util::Resolution.exec('env | grep FACTER_localuser | cut -d "=" -f 2')
    end
end

Facter.add(:localgroup) do
    setcode do
        Facter::Util::Resolution.exec('env | grep FACTER_localgroup | cut -d "=" -f 2')
    end
end

Facter.add(:openraveorg_deploydir) do
    setcode do
        Facter::Util::Resolution.exec('env | grep FACTER_openraveorg_deploydir | cut -d "=" -f 2')
    end
end

Facter.add(:openraveorg_gitdir) do
    setcode do
        Facter::Util::Resolution.exec('env | grep FACTER_openraveorg_gitdir | cut -d "=" -f 2')
    end
end

