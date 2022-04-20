import os
import sys


if __name__ == '__main__':

    if sys.argv[1] == "-close":
        close_arg = sys.argv[2]
        # Setting the Receiver data-flow
        os.system('sudo pkill ITGRecv')
        if close_arg == 'False':
            os.system('sudo ITGRecv -Si eth0.104 -Sp 9090 -a 192.168.110.1')
        else:
            os.system('sudo pkill ITGRecv')
