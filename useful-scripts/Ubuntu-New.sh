#!/bin/sh


#new pc update
#必须先修改hostname
#先检测resolv.conf

echo "This is an initialization for New PCs!"

echo "Print system info:"

echo "DiskSpace=$(df -h)"

echo "IpInfo:$(ifconfig | grep 'inet addr')"

sleep 10

cat >/etc/apt/sources.list<<EFF
deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse

deb http://mirrors.aliyun.com/ubuntu trusty main restricted
deb-src http://mirrors.aliyun.com/ubuntu trusty main restricted
deb http://mirrors.aliyun.com/ubuntu trusty-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates main restricted
deb http://mirrors.aliyun.com/ubuntu trusty universe
deb-src http://mirrors.aliyun.com/ubuntu trusty universe
deb http://mirrors.aliyun.com/ubuntu trusty-updates universe
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates universe
deb http://mirrors.aliyun.com/ubuntu trusty multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty multiverse
deb http://mirrors.aliyun.com/ubuntu trusty-updates multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates multiverse
deb http://mirrors.aliyun.com/ubuntu trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty-backports main restricted universe multiverse

deb http://mirrors.sohu.com/ubuntu/  trusty main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/  trusty-security main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/  trusty-updates main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/  trusty-proposed main restricted universe multiverse
deb http://mirrors.sohu.com/ubuntu/  trusty-backports main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/  trusty main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/  trusty-security main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/  trusty-updates main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/  trusty-proposed main restricted universe multiverse
deb-src http://mirrors.sohu.com/ubuntu/  trusty-backports main restricted universe multiverse
EFF


apt-get update && apt-get upgrade   
sleep 10 

echo "addusers:"
adduser xiaofei
adduser nianyong
adduser zhangjingqiu
adduser huangliang
echo "\n\n\n\n\n"

echo "nianyong ALL=(ALL:ALL) ALL"  >> /etc/sudoers
echo "nianyong ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
echo  "xiaofei  ALL=(ALL:ALL) ALL" >>/etc/sudoers
echo "xiaofei ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
echo  "zhangjingqiu ALL=(ALL:ALL) ALL" >>/etc/sudoers
echo "zhangjingqiu ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers
echo  "megaium ALL=(ALL:ALL) ALL" >>/etc/sudoers
echo "megaium ALL=(ALL) NOPASSWD: ALL"  >> /etc/sudoers

mkdir /home/zhangjingqiu/.ssh/
mkdir /home/xiaofei/.ssh/
mkdir /home/nianyong/.ssh/
mkdir /home/huangliang/.ssh/

echo "get rsa_pubs:"
cd /home/xiaofei/.ssh/ ; wget http://183.57.151.178/keys/xiaofei_rsa.pub ; mv xiaofei_rsa.pub authorized_keys
cd /home/zhangjingqiu/.ssh/ ; wget http://183.57.151.178/keys/zhangjingqiu_rsa.pub ; mv zhangjingqiu_rsa.pub authorized_keys
cd /home/nianyong/.ssh/ ; wget http://183.57.151.178/keys/nianyong_rsa.pub ; mv nianyong_rsa.pub authorized_keys
cd /home/huangliang/.ssh/ ; wget http://183.57.151.178/keys/huangliang_rsa.pub ; mv huangliang_rsa.pub authorized_keys

echo "change changes:"
chown -R xiaofei:xiaofei /home/xiaofei/ ; chmod 700 /home/xiaofei/.ssh/ ; chmod 400 /home/xiaofei/.ssh/authorized_keys
chown -R nianyong:nianyong /home/nianyong/ ; chmod 700 /home/nianyong/.ssh/ ; chmod 400 /home/nianyong/.ssh/authorized_keys
chown -R zhangjingqiu:zhangjingqiu /home/zhangjingqiu/ ; chmod 700 /home/zhangjingqiu/.ssh/ ; chmod 400 /home/zhangjingqiu/.ssh/authorized_keys
chown -R huangliang:huangliang /home/huangliang/ ; chmod 700 /home/huangliang/.ssh/ ; chmod 400 /home/huangliang/.ssh/authorized_keys



#1.安装容器配置包：
#RHEL5 CenOS5:
#   rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/5/x86_64/zabbix-release-2.2-1.el5.noarch.rpm
#RHEL6 CenOS6:
#   rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm

#2.yum install zabbix-server-mysql zabbix-web-mysql

rpm -ivh http://repo.zabbix.com/zabbix/2.2/rhel/6/x86_64/zabbix-release-2.2-1.el6.noarch.rpm
yum install zabbix-agent -y

rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
 rpm -Uvh http://apt.sw.be/redhat/el6/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
 yum -y install salt-minion
echo "master:"     > /etc/salt/minion 
echo "   - 192.168.2.223" >>/etc/salt/minion 
echo "id: $HOSTNAME" >> /etc/salt/minion
echo "log_file: /var/log/salt/minion" >> /etc/salt/minion
 service salt-minion start
/etc/init.d/salt-minion restart
sleep 10
sed -i "s/Server=127.0.0.1/Server=193.167.10.69/g" `grep "ServerActive=127.0.0.1" -rl /etc/zabbix/zabbix_agentd.conf`
sed -i "s/ServerActive=127.0.0.1/ServerActive=193.167.10.69/g" `grep "ServerActive=127.0.0.1" -rl /etc/zabbix/zabbix_agentd.conf` 
sed -i "s/Hostname=Zabbix server/Hostname=$HOSTNAME/g" `grep "Hostname=Zabbix server" -rl /etc/zabbix/zabbix_agentd.conf`
yum install sysstat -y
nohup /usr/bin/iostat -dxkt 30  > /tmp/iostat_output 2>/dev/null &
mkdir -p /opt/script && cd /opt/script 
salt "*" cp.get_file salt://script/disk_status.sh /opt/script/disk_status.sh
salt "*" cmd.run "service zabbix-agent restart"
service zabbix-agent restart
0 0 */1 * * * root /usr/sbin/ntpdate 192.168.2.223;/sbin/hwclock -w

echo "ssh changes:"
sed -i 's/Port 22/Port 10022/g' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin without-password/PermitRootLogin no/g' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication no/PasswordAuthentication no/g' /etc/ssh/sshd_config

echo "ssh restart"
service ssh restart

echo "0  *   * * *   root     ntpdate 192.168.2.216" >> /etc/crontab && echo "30  *   * * *   root     ntpdate 192.168.2.217" >> /etc/crontab  &&  service cron restart

user=root
#password='F7o6q4B%ze8k*K&RO*#%amvquI6t2LUD'
password='1VX02tKYa8HxN9cJHg7Ip74MLwU='
passwd $user << modpwd
$password
$password
modpwd

echo "mkdir /backup/"
mkdir -p /backup/script /backup/shell
## F7o6q4B%ze8k*K&RO*#%amvquI6t2LUD
#salt "sjz-*" cp.get_file salt://get_connections.py  /backup/scrip/get_connections.py #所有relay


dpkg-reconfigure tzdata  #时区更改  Asia/Chongqi
