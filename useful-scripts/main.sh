#!/bin/bash
#############################################
#Date:2016-1-19
#Author:myou
#the main program for newhost update.
#############################################
echo "This is an initialization for New PCs!"
echo "Print system info:"
#echo "The HOSTNAME is $(yourhostname) \nDiskSpace=$(df -h)"
echo -e "IpInfo: \n$(ifconfig | grep 'inet addr')"
echo "apt-get update && apt-get upgrade:"
     ./apt_upgrade.sh
echo "AddUsers and private keys:"
     ./adduser.sh
echo "SSH changes:"
     ./sshAndchangepasswd.sh
read -p "Please Enter the hostname:" yourhostname 
if [ "$yourhostname" == "$HOSTNAME" ];then
   echo "The hostname is true,Then install zabbix and salt:";
     ./zabbixsalt.sh;
else 
   echo "Please check your hostname is true.";
   exit 0;
fi

