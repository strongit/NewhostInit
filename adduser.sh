#!/bin/bash
#########################
#Date:2016-1-19
#Author:myou
#Add Relay Users Program
#########################
echo "addusers function:"
echo "You could add these users:"
echo -e  "#########################"
echo "运维部：liu,zhang,nian,xiao,operator1"
echo "Web:liang,bing"
echo "storage:wei"
echo "db:tony,man"
echo -e  "#########################"
autoaddusers()
{
   echo -n "Enter username:";
   read user;
   echo "Welcome $user";
   adduser $user << EOF
   echo -e "\n"
   echo -e "\n"
   echo -e "\n"
   echo -e "\n"
   echo -e "\n"
   echo -e "\n"
   echo -e "\n"
EOF
   echo "adduser $user successful!";
   echo "$user ALL=(ALL:ALL) ALL" >> /etc/sudoers; 
   echo "$user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers;
   mkdir /home/$user/.ssh/;
   echo "get rsa_pubs:";
   cd /home/$user/.ssh/ && wget http://*********/keys/$user\_rsa.pub && mv $user\_rsa.pub authorized_keys;
   echo "change changes:";
   chown -R $user:$user /home/$user/ &&  chmod 700 /home/$user/.ssh/ &&  chmod 400 /home/$user/.ssh/authorized_keys;
   return $?;
}

autoaddusers
