#! /bin/bash
home=/data/log/
cd $home
if [`pwd` == $home];then
a="1 1000 2000 3000 4000 5000 6000 7000 8000 9000"
for b in $a
  do
    c=`expr $b + 1000`
    for loop in `sed -n "$b,$c"p $1`
      do
        path=`echo $loop | awk -F "/" '{print $1"/"$2"/"$3"/"$4}'`
        mkdir -p $path
        mv $loop -P $path
        echo $loop >> $1.log
      done
  done
fi
