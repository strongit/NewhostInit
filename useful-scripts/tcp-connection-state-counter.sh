#!/bin/bash
# @Function
# show count of tcp connection stat.
#
# @Usage
#   $ ./tcp-connection-state-counter.sh
#
# @author Strong It

netstat -tna | awk 'NR > 2 {
    s[$NF]++
}

END {
    for(v in s) {
        printf "%-12s%s\n", v, s[v]
    }
}' | sort -nr -k2,2

#netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
