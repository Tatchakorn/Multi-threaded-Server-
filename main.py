import sys
import subprocess
import time
import os
from glob import glob

if __name__ == '__main__':
    
    if sys.platform == 'win32':
        if len(sys.argv) > 1:
            if sys.argv[1] == 'del':
                subprocess.Popen(['del', '*.log'], shell=True)
            elif sys.argv[1] == 'test':
                subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)
            elif sys.argv[1] == 'server':
                subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)
            elif sys.argv[1] == 'mul':
                subprocess.Popen(['start', 'python', r'.\src\multicast.py'], shell=True)
        else:
            subprocess.Popen(['start', 'python', r'.\src\server.py'], shell=True)
            time.sleep(2)
            subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)
    
    elif sys.platform == 'linux': # Ubuntu
        if len(sys.argv) > 1:
            if sys.argv[1] == 'del':
                for f in glob('*.log'): 
                    os.remove(f)
            elif sys.argv[1] == 'test':
                cmd = 'gnome-terminal -- python3 ./src/test.py'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            elif sys.argv[1] == 'server':
                cmd = 'gnome-terminal -- python3 ./src/server.py'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            elif sys.argv[1] == 'mul':
                cmd = 'gnome-terminal -- python3 ./src/multicast.py'
                subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        else:
            cmd = 'gnome-terminal -- python3 ./src/server.py'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            time.sleep(2)
            cmd = 'gnome-terminal -- python3 ./src/test.py'
            subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)