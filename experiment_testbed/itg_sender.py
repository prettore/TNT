import os
# reference: http://traffic.comics.unina.it/software/ITG/manual/index.html

os.system('sudo pkill ITGSend')
os.system('sudo ITGSend -Sda 192.168.1.101 -Sdp 9090 -T UDP -a 192.168.110.1 -c 1264 -s 0.123456 -U 1 50 -z 1000 -t 100000000')
