#!/bin/bash
# @Function
# show some time of nginx source ip info.
#
# @Usage
#   $ ./nginx-state-counter.sh start end 10
#
# @author Strong It

PROG=`basename $0`

usage() {
    cat <<EOF
Usage: ${PROG} [OPTION]... PATTERN
Show date1 to date2 head 10(default) ip access info
Example: ${PROG} -s 28/Feb/2017:15 -e 28/Feb/2017:15:28 -h 10

Options:
    -f, --file            the/path/to/logfile
    -s, --startime        start time
    -e, --endtime         end time
    -c, --count           head ip count
    -h, --help            display this help and exit
EOF
    exit $1
}

ARGS=`getopt -a -o f:s:e:c:h -l file:,startime:,end:,count:,help -- "$@"`
[ $? -ne 0 ] && usage 1
eval set -- "${ARGS}"

while true; do
    case "$1" in
    -f|--file)
        file="$2"
        ;;
    -h|--help)
        usage
        ;;
    --)
        shift
        break
        ;;
    esac
    case "$3" in
    -s|--start)
        startime="$4"
        ;;
    -h|--help)
        usage
        ;;
    --)
        shift
        break
        ;;
    esac
    case "$5" in
    -e|--end)
        endtime="$6"
        ;;
    -h|--help)
        usage
        ;;
    --)
        shift
        break
        ;;
    esac
    case "$7" in
    -c|--count)
        count="$8"
        shift 2
        ;;
    -h|--help)
        usage
        ;;
    --)
        shift
        break
        ;;
    esac
done

[ -z "$1" ] && { echo No find file pattern! ; usage 1; }
startime=${startime}
file=${file}
endtime=${endtime}
count=${count}
echo $file,$startime,$endtime,$count

awk "\$4>=\"[${startime}\" && \$4<=\"[${endtime}\"" /data/python/Django/Dfcenv/logs/nginx-access.log|uniq -c | sort -rn|head -$count
echo "awk '\$4>="[${startime}" && \$4<="[${endtime}"' /data/python/Django/Dfcenv/logs/nginx-access.log|uniq -c | sort -rn|head -$count"
