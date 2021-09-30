import telnetlib
from datetime import datetime
import time

HOST = "192.168.1.1"
user = "admin"
password = 'admin'

def base_read():
    tn = telnetlib.Telnet(HOST)
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    time.sleep(1)
    return tn

tn = base_read()

def read_SNR():
    log = ""


    tn.write(b"show wan adsl linedata near\n")
    time.sleep(1.05)
    s = tn.read_very_eager().decode('ascii')
    if s.find("noise margin downstream: ") != -1 :
        k = s.find("relative capacity occupation: ")+ len("relative capacity occupation: ")
        rel = s[k:s.find("%")+1]
        i = s.find("noise margin downstream: ")
        DoSNR = s[i+25:i+29]
        log = DoSNR +">" + "<" +rel
    else : 
        log = s



    tn.write(b"show wan adsl linedata far\n")
    time.sleep(1.05)
    us = tn.read_very_eager().decode('ascii')
    if us.find("noise margin upstream: ") != -1:
        j = us.find("noise margin upstream: ")+len("noise margin upstream: ")
        UpSNR = us[j:j+4]
        log =log[:log.find(">")+1]+UpSNR+log[log.find("<"):]
    else:
        log = log +"-"+us
    return log

    
    
    

def write_file(tim,log):
    current_date = datetime.now().strftime("%Y_%m_%d")
    name = "Log_"+current_date+".txt"
    f = open(name,'a')
    f.write(tim+";"+log+"\n")
    f.close

 
print("app started")


for i in range(0,6250):
    now = datetime.now().strftime("%H:%M:%S")
    log = read_SNR()
    write_file(now,log)
    print(now+";"+log)
    time.sleep(12.8)
print("end of app")
tn.close