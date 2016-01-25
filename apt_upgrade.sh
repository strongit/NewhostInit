#!/bin/sh
echo "update system and upgrade programe:"

cat >/etc/apt/sources.list<<EFF
deb http://mirrors.aliyun.com/ubuntu trusty main restricted
deb http://mirrors.aliyuncs.com/ubuntu trusty main restricted
deb-src http://mirrors.aliyun.com/ubuntu trusty main restricted
deb-src http://mirrors.aliyuncs.com/ubuntu trusty main restricted
deb http://mirrors.aliyun.com/ubuntu trusty-updates main restricted
deb http://mirrors.aliyuncs.com/ubuntu trusty-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates main restricted
deb-src http://mirrors.aliyuncs.com/ubuntu trusty-updates main restricted
deb http://mirrors.aliyun.com/ubuntu trusty universe
deb http://mirrors.aliyuncs.com/ubuntu trusty universe
deb-src http://mirrors.aliyun.com/ubuntu trusty universe
deb-src http://mirrors.aliyuncs.com/ubuntu trusty universe
deb http://mirrors.aliyun.com/ubuntu trusty-updates universe
deb http://mirrors.aliyuncs.com/ubuntu trusty-updates universe
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates universe
deb-src http://mirrors.aliyuncs.com/ubuntu trusty-updates universe
deb http://mirrors.aliyun.com/ubuntu trusty multiverse
deb http://mirrors.aliyuncs.com/ubuntu trusty multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty multiverse
deb-src http://mirrors.aliyuncs.com/ubuntu trusty multiverse
deb http://mirrors.aliyun.com/ubuntu trusty-updates multiverse
deb http://mirrors.aliyuncs.com/ubuntu trusty-updates multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty-updates multiverse
deb-src http://mirrors.aliyuncs.com/ubuntu trusty-updates multiverse
deb http://mirrors.aliyun.com/ubuntu trusty-backports main restricted universe multiverse
deb http://mirrors.aliyuncs.com/ubuntu trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyuncs.com/ubuntu trusty-backports main restricted universe multiverse
EFF
apt-get update && apt-get upgrade  
