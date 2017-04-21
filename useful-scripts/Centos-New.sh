#!/bin/sh


#new pc update
#必须先修改hostname
#先检测resolv.conf

echo "This is an initialization for New PCs!"

echo "Print system info:"

echo "DiskSpace=$(df -h)"

echo "IpInfo:$(ifconfig | grep 'inet addr')"

#yum 源
cd /etc/yum.repos.d/ && rename repo repo.bak *.repo
curl -O http://mirrors.163.com/.help/CentOS7-Base-163.repo
yum clean all
yum makecache
yum update -y
yum install vim ntpdate wget net-tools lrzsz -y

sleep 10 

#4 修改系统默认的umask值
sed -i -e 's/umask 022/umask 027/' /etc/bashrc

#5 只有root才能执行如下目录下面的脚本
chmod -R 750  /etc/init.d/*

#6 只有root才能读取
chmod 644 /etc/passwd
chmod 644 /etc/group
chmod 600 /etc/shadow
chmod 600 /etc/gshadow

#7 给下面的文件加上不可更改属性，从而防止非授权用户获得权限。 
chattr +i /etc/passwd
chattr +i /etc/shadow
chattr +i /etc/group
chattr +i /etc/gshadow

#8 隐藏系统信息
cat /dev/null >/etc/issue
cat /dev/null >/etc/issue.net

#9 设置登陆超时时间
echo "TMOUT=180">>/etc/profile

#10 禁止非法重起服务器
sed -i -e '/ctrlaltdel/s/^/#/' /etc/inittab

#11 时间对时
echo "0 3 * * * /usr/sbin/ntpdate -u 192.168.2.223 >> /var/log/ntpdate.log 2>&1" >/var/spool/cron/root

#12 历史命令保存数为0，退出系统时自动清空历史命令
sed -i 's@HISTSIZE=[0-9]*@HISTSIZE=0@' /etc/profile
source /etc/profile
echo "history -c" >>/root/.bash_logout

#14 set ssh
sed -i 's/^GSSAPIAuthentication yes$/GSSAPIAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config


#16 关闭不必要的服务
cat >/tmp/service.conf<<EOF
microcode_ctl
gpm
kudzu
amd
nfs
apmd
arpwatch
autofs
automount
bootparamd
dhcpd
gated
httpd
inetd
innd
linuxconf
lpd
mars-nwe
mcserv
named
netfs
samba
nfs
nscd
portmap
postgresql
rstatd
ruserd
rwalld
whod
sendmail
smb
squid
xfs
ypbind
yppasswdd
pserv
identd
bluetooth
ibmasm
ip6tables
lm_sensors
saslauthd
vncserver
nfslock
rawdevices
svnserve
acpid
capi
cpuspeed
hidd
ip6tables
cups
dund
haldaemon
isdn
irda
netplugd
pand
conman
lvm2-monitor
mdmonitor
restorecond
talk
finger
telnet
EOF

while read service other
do
        if chkconfig --list|grep ${service};then
        service ${service} stop
        chkconfig ${service} off
        fi
done</tmp/service.conf

#17 内核参数优化
true > /etc/sysctl.conf
cat >> /etc/sysctl.conf << EOF
net.ipv4.ip_forward = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.default.accept_source_route = 0
kernel.sysrq = 0
kernel.core_uses_pid = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.ip_local_port_range = 1024 65535
net.core.rmem_max=16777216
net.core.wmem_max=16777216
net.ipv4.tcp_rmem=4096 87380 16777216
net.ipv4.tcp_wmem=4096 65536 16777216
net.ipv4.tcp_fin_timeout = 10
net.ipv4.tcp_tw_recycle = 1 
net.ipv4.tcp_tw_reuse = 1 
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_window_scaling = 0
net.ipv4.tcp_sack = 0
net.core.netdev_max_backlog = 30000
net.ipv4.tcp_no_metrics_save=1
net.core.somaxconn = 262144
net.ipv4.tcp_max_orphans = 262144
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_keepalive_time=1200 
net.nf_conntrack_max = 6553600
EOF
/sbin/sysctl -p

#18 系统资源限制
cat > /etc/security/limits.conf << EOF
*       soft nofile 65535
*       hard nofile 65535
root   soft    nproc   65535
root   soft    nproc   65535
oracle   hard    nproc   65535
oracke   hard    nproc   65535
nginx   hard    nproc   65535
nginx   hard    nproc   65535
EOF