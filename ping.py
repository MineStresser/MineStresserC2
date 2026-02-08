from socket import *
import argparse
import time
parser = argparse.ArgumentParser(description="MCPE Checker Ping Tool Credit: MineGamerST")
parser.add_argument('dns', help='domain or ip of the server/service')
parser.add_argument('-p', dest='port', help='port')
parser.add_argument('--timeout', dest='tm', help='timeout')
parser.add_argument('--coldown', dest='cd', help='the coldown of the pings')
args = parser.parse_args()
green = '\033[0;32m'
red = '\033[0;31m'
violet = '\033[0;33m'
off = '\033[0m'
print(f'Copyright MineStresserC2 2026\n\nConnecting To {green}{args.dns}{off} ON {green}UDP {args.port}{off}:\n')
enviadas = 0
falhas = 0
accepted = 0
master_latency = 0
lower_latency = 0
medium_latency = 0
if args.tm:
    timeout = float(args.tm)
else:   
    timeout = 1
if args.cd:
    coldown = float(args.tm)
else:
    coldown = 1
sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(timeout)
payload = bytes.fromhex("01" + "0000000000000000" + "00ffff00fefefefefdfdfdfd12345678" + "0000000000000000")
try:
    while True:
        try:
            sock.connect((args.dns, int(args.port)))
            start_time = time.time()
            sock.send(payload)
            response = sock.recv(300)
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            latency = str(latency).split('.')[0]
            latency0 = float(latency)
            print(f'Server has Connected! {green}{args.dns}{off}: Time={green}{latency}ms{off} Protocol={green}UDP{off} Port={green}{args.port}{off}')
            accepted += 1
            enviadas += 1
            if latency0>=master_latency:
                master_latency = latency0
            elif latency0<master_latency:
                if lower_latency == 0:
                    lower_latency = latency0
                else:
                    if latency0>lower_latency:
                        medium_latency = latency0
                    else:
                        lower_latency = latency0
        except TimeoutError:
            print('\033[0;31mConnection Time out\033[0m')
            falhas += 1
            enviadas += 1
        except Exception as e:
            print('\033[0;31mConnection refused.\033[0m\n\n')

        time.sleep(coldown)
except KeyboardInterrupt:
    print(f'''\nConnection statistics:
    Attempted = {violet}{enviadas}{off}, Connected = {violet}{accepted}{off}, Failed = {violet}{falhas}{off}''')
    print(f'''\nConnection graphic:
    lower latency = {violet}{lower_latency}ms{off}, medium latency = {violet}{medium_latency}ms{off}, average latency = {violet}{master_latency}ms{off}''')
