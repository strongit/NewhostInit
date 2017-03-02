#!/bin/sh
echo "ssh changes:"
sed -i 's/Port 22/Port 122/g' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin without-password/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication no/PasswordAuthentication no/g' /etc/ssh/sshd_config

echo "ssh restart:"
service ssh restart
echo "Change root passwd:"
user=root
password='F7o6q4B%ze8k*K&RO*#%amvq'
passwd $user << EOF
$password
$password
EOF
