import sys
import subprocess
import time


if __name__ == '__main__':
    
    if sys.platform == 'win32':
        if len(sys.argv) > 1:
            if sys.argv[1] == 'del':
                subprocess.Popen(['del', '*.log'], shell=True)
            elif sys.argv[1] == 'test':
                subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)
            elif sys.argv[1] == 'server':
                subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)
        else:
            subprocess.Popen(['start', 'python', r'.\src\server.py'], shell=True)
            time.sleep(2)
            subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)