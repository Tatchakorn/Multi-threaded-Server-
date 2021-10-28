import sys
import subprocess
import time


if __name__ == '__main__':
    
    if sys.platform == 'win32':
        if len(sys.argv) > 1:
            subprocess.Popen(['del', '*.log'], shell=True)
        else:
            subprocess.Popen(['start', 'python', r'.\src\server.py'], shell=True)
            time.sleep(2)
            subprocess.Popen(['start', 'python', r'.\src\test.py'], shell=True)