import subprocess
import re
import logging
import time
try:
    import paramiko
except Exception as e:
    print(e,"unable to import paramiko run the below command\n pip install paramiko")

Username =  "testUser"
Password =  "Test@pass"
Remote_IP ="172.18.4.33" 

logging.basicConfig(filename='monitorcopyRmtf.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s',level = logging.INFO)

def check_script():
    s = subprocess.Popen("ps -ef | grep CopyRmtFile.sh ",shell= True,stdout=subprocess.PIPE)
    res = s.stdout.read()
    # breakpoint()
    if re.search("/copyRmtFile.sh\n",res.decode("utf-8")):
        logging.info("{} :- copyRmtFile.sh running without any issues".format(time.ctime()))
    else:
        if check_server(Remote_IP,Username,Password):
            p = subprocess.Popen("nohup ./copyRmtFile.sh &",shell=True)
            if p.poll() == 0:
                logging.info("{} process started again".format(time.ctime()))
            else:
                logging.error("{} process failed to start".format(time.ctime()))

        else:
            logging.error("{} unnable to access IP :-{} username:-{} ,Error code E500".format(time.ctime(),Remote_IP,Username,Password))


def check_server(ip,username,password):
    try :
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(ip, username=username, password=password,timeout=10)

        stdin, stdout, stderr = ssh.exec_command('exit')
        ssh.close()
        return True
    except Exception as e:
        logging.error("Error occured {}".format(e))
        return False


if __name__ == "__main__":
    check_script()
    

