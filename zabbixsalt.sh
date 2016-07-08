#!/bin/sh
###########################################
#Date:2016-1-19
#Author:DT
#get salt-minion and zabbix-agent program
###########################################

#Ubuntu
apt-get install salt-minion
echo "master:"    > /etc/salt/minion 
echo "   - 192.168.2.2" >>/etc/salt/minion 
echo "   - 192.168.2.254" >>/etc/salt/minion 
echo "hostname="
read hostname <<EFF
echo "$HOSTNAME"
EFF
echo "id: $(hostname)" >> /etc/salt/minion
echo "log_file: /var/log/salt/minion" >> /etc/salt/minion
/etc/init.d/salt-minion restart
echo "salt-minion install successfull"
sleep 10
apt-get install zabbix-agent
echo "Please input zabbix-proxy or zabbix-server local_ip:"
read localip
echo "$localip"
sed -i "s/Server=127.0.0.1/Server=${localip}/g" `grep "ServerActive=127.0.0.1" -rl /etc/zabbix/zabbix_agentd.conf`
sed -i "s/ServerActive=127.0.0.1/ServerActive=${localip}/g" `grep "ServerActive=127.0.0.1" -rl /etc/zabbix/zabbix_agentd.conf`
sed -i "s/Hostname=Zabbix server/Hostname=${hostname}/g" `grep "Hostname=Zabbix server" -rl /etc/zabbix/zabbix_agentd.conf`

service zabbix-agent restart
echo "zabbix-agent install successfull"
sleep 10

#redhat
#os_version=`awk '{printf "%d" ,$3}' /etc/redhat-release`
#if [ $os_version -lt 5 ];then
#	echo 'need centos 5 or newer'
#	exit 254
#fi
#if [ $os_version -eq 5 ];then
#    if ! rpm -ql epel-release ;then
#	if rpm -Uvh http://repo.zabbix.com/zabbix/3.0/rhel/6/x86_64/zabbix-agent-3.0.2-1.el6.x86_64.rpm ;then
#		yum -y zabbix-agent
#	fi
#     else
#		yum -y install zabbix-agent
#    fi
#fi
#
#if [ $os_version -eq 6 ];then
#    if ! rpm -ql epel-release ;then
#        if  rpm -Uvh http://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-agent-3.0.2-1.el7.x86_64.rpm ;then
#               yum -y install zabbix-agent
#        fi
#    else
#		yum -y install zabbix-agent
#    fi
#fi
