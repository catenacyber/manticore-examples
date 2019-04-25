#/bin/sh
cat prof.txt | awk '{print "cd "$1"; python3 -m cProfile " $2 ">cprof.txt; cd .."}' | sh
find . -name "cprof.txt" | while read i; do grep -a "ncalls  tottime" $i -A100000 > "$i"2 ; done
find . -name "cprof.txt" | while read i; do mv "$i"2 "$i"; done


#multiple-styles win.py ok added
#ais3_crackme win.py ok
#google2016_unbreakable win.py ok
#hxp2018_angrme solve.py ok
#internetwache15-re60 solve.py ok
#pwnable_collision win.py ok

#RPISEC_MBE fail Invalid memory access
#exploit_generation_example fail python2
#manticore_challenge fail 'objdump -d manticore_challenge | grep exit' returned non-zero exit status 1.
#polyswarm_challenge fail manticore stacktrace
