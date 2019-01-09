import datetime
import json
import os
import subprocess
import time
import sys

batch_path = sys.argv[1]
num1 = int(sys.argv[2])
num2 = int(sys.argv[3])

timeout = 900


def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data


def read_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip('\n')
    return lines


def append_file(file_path, content):
    with open(file_path, "a") as f:
        f.write(content + "\n")
    f.close()

def generate_batch():
    path = "12.24.1000-5000+.txt"
    json_data = read_json(path)
    length = len(json_data)
    # print()
    for i in range(0,length):
        cmd = "python3 -u crawl_library.py d " + str(i) + " " + str(i+1) + " 12.24.1000-5000+.txt y"
        append_file("12.24.1000-5000+.sh", cmd)


# def execute():
#     file_list = os.listdir(os.getcwd())
#     for file in file_list:
#         if not file.endswith(".sh"):
#             continue
#         print("+++++++++++++++++ " + file)
#         lines = read_file(os.path.join(os.getcwd(), file))
#         for cmd in lines:
#             # cmd = cmd.replace("apicallupdate.jar","C:/Users/yw/Desktop/api_call_update/apicallupdate.jar")
#             cmd = cmd.replace(" $a $b $c $d $e", "") + " " + project_lib_of_commit + " " + jar_path + " " + api_path + " " + project_dir + " " + api_call_output
#             print("++++++++++++++++ cmd : "+cmd)
#             start = datetime.datetime.now()
#             process = subprocess.Popen(cmd)
#             while process.poll() is None:
#                 time.sleep(0.2)
#                 now = datetime.datetime.now()
#                 if (now - start).seconds > timeout:
#                     append_file("unsolved_cmd.txt",cmd)
#                     os.popen('taskkill /pid '+str(process.pid)+' -f')
#                     # os.kill(process.pid, signal.SIGKILL)
#                     # os.waitpid(-1, os.WNOHANG)
#                     break

def execute():
    lines = read_file(batch_path)
    # for cmd in lines:
    for i in range(num1, num2):
        cmd = lines[i]
        timeout = 900
        print("++++++++++++++++ cmd : "+cmd)
        start = datetime.datetime.now()
        process = subprocess.Popen(cmd.split(" "))
        while process.poll() is None:
            time.sleep(0.2)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                append_file("unsolved_cmd.txt",cmd)
                os.popen('taskkill /pid '+str(process.pid)+' -f')
                break

execute()
# generate_batch()
