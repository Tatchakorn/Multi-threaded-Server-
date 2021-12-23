import time
import subprocess

from pathlib import Path

shared_msg_folder = Path('./shared_msg') 
message_board_file = shared_msg_folder.joinpath('message_board.py')
shr_file = shared_msg_folder.joinpath('shr.py')



if __name__ == '__main__':
    # for _ in range(3):
    #     subprocess.Popen(['start', 'python', shr_file], shell=True)
    # time.sleep(3)
    subprocess.Popen(['start', 'python', message_board_file], shell=True)
    # subprocess.Popen(['start', 'python', shr_file], shell=True)