import os

if __name__ == '__main__':

    #os.system('sudo kill $(sudo lsof -t -i:2020)')
    os.system('sudo pkill -f "python2 - -t"')
    os.system('sudo pkill -f "python - -t"')