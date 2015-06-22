# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/vivid64"

  config.vm.provider :virtualbox do |v|
    v.name = "productbase"
    v.memory = 1024
    v.cpus = 1
    v.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.synced_folder ".", "/home/vagrant/dream_ticket", id: "vagrant-root",
    owner: "vagrant",
    group: "vagrant",
    mount_options: ["dmode=775,fmode=664"]

  config.vm.network :private_network, ip: "172.28.128.30"

  # for supress "stdin: is not a tty error"
  config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"

  config.vm.provision "shell", inline: "sudo apt-get update -qq && sudo apt-get install python-dev python-pip libpython2.7-dev libyaml-dev mc -y -q"
  config.vm.provision "shell", inline: "sudo pip install ansible fabric"
  config.vm.provision "shell", privileged: false, inline: "cd dream_ticket/provision && fab provision_local"

end
