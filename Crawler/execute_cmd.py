import datetime
import os
import subprocess
import time
import sys

project_lib_of_commit = sys.argv[1]
jar_path = sys.argv[2]
api_path = sys.argv[3]
project_dir = sys.argv[4]
api_call_output = sys.argv[5]

timeout = 900

def execute():
    file_list = os.listdir(os.getcwd())
    for file in file_list:
        if not file.endswith(".sh"):
            continue
        print("+++++++++++++++++ " + file)
        lines = read_file(os.path.join(os.getcwd(), file))
        for cmd in lines:
            # cmd = cmd.replace("apicallupdate.jar","C:/Users/yw/Desktop/api_call_update/apicallupdate.jar")
            cmd = cmd.replace(" $a $b $c $d $e", "") + " " + project_lib_of_commit + " " + jar_path + " " + api_path + " " + project_dir + " " + api_call_output
            print("++++++++++++++++ cmd : "+cmd)
            start = datetime.datetime.now()
            process = subprocess.Popen(cmd)
            while process.poll() is None:
                time.sleep(0.2)
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                    append_file("unsolved_cmd.txt",cmd)
                    os.popen('taskkill /pid '+str(process.pid)+' -f')
                    # os.kill(process.pid, signal.SIGKILL)
                    # os.waitpid(-1, os.WNOHANG)
                    break

def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
    return lines

def append_file(file_path,content):
    with open(file_path, "a") as f:
        f.write(content + "\n")
    f.close()

execute()

