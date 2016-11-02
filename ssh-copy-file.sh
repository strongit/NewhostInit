#!/bin/bash 
case $1 in # 获取option 
-cp | --cpoy)  #判断option
        for ip_list in `cat $2`;do  #读取$2文件每一行，将ip密码信息存入ip_list变量
        ip=`echo $ip_list | cut -d: -f1` #提取ip
        ps=`echo $ip_list | cut -d: -f2` #提取密码
            expect -c"                   
            spawn scp -r /root/.ssh/  $ip:  #直接拷贝.ssh目录，配置免密码登录
            expect {       
                \"*password*\" {send \"$ps\r\";exp_continue}
                \"*password*\" {send \"$ps\r\";}
            }
           "
       done
;;
-c  | --cmd) #执行命令
        for ip_line in `cat $2`;do
        ip=`echo $ip_line| cut -d: -f1`
            if [[ "$4" = \h ]];then
                echo -e "\033[33m $ip: \033[0m" 
                ssh $ip $3
            else
            echo -e "\033[33m $ip: \033[0m" `ssh $ip $3`
            fi
        done
;;
-h | --help )
echo -e "\e[1;32m  Please create a IP Password file in advance: \e[0m"
echo -e "\e[1;32m  $0 -cp,--copy  ip.txt  \e[0m"
echo -e "\e[1;32m  $0 -c,--cmd  ip.txt 'cmd' and \h \e[0m"
;;
esac
