#!/usr/bin/expect
#for ((i=1;i<254;i++)) ; do  echo "192.168.2.$i:fangcang" >> hosts.txt; done
#yum install expect
#hosts.txt格式：host:ip
info=`awk '{print $0}' ./hosts.txt`
for i in $info;do
  ip=$(echo "$i" |cut -d ":" -f1)
  password=$(echo "$i"|cut -d ":" -f2)
  expect -c "
  spawn /usr/bin/ssh-copy-id -i /root/.ssh/id_rsa.pub root@$ip
    expect {
        \"*yes/no*\" {send \"yes\r\";exp_continue}
        \"*password*\" {send \"$password\r\";exp_continue}
        \"*password*\" {send \"$password\r\";}
  }
  "
done
