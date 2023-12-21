import sys
import ASCIIArtPy.aapy as aa
import cv2
import numpy as np
import os
from datetime import datetime
import psutil
import argparse

parser = argparse.ArgumentParser(description='')    # 2. パーサを作る
parser.add_argument('-i',"--interval", help='', default=0.05,type=float)    # 必須の引数を追加

args = parser.parse_args()

# Webカメラを使うときはこちら

est=0
printer = aa.color.full(mode=1,char=" ")
printer.chars = " ░▒▓█"
    # ░▒▓█ 
    # ▘▖▝▗▀▄▚▞▐▋▛▙▜▟█ /  ▘▀▚▛█
    # ▁▂▃▄▅▆▇█
    # .-:=+*#%@
    # ▏▎▍▌▋▊▉█
    # ▖▖▚▚▜▜█
    #  ⡀⠈⡐⠡⡘⡙⡛⣾⣿▒▓█
    # ´-²;º=\LzïY[j1kéñü6Søq©AKÈRNÒÂÕ¶ / Latin-1

#printer.chars=["▓ ▓ ","▓▒▒▓","▓▒▓▒","▓▒▓▓","▓▓▓▓","▓▓▓▓","█▓█▓","▓█▓█","██▓█","████"]
termsize = os.get_terminal_size()
cpu_percent = psutil.cpu_percent(percpu=True)
frame = np.zeros((len(cpu_percent),termsize[0],3),np.uint8)

while True:
    # 1フレームずつ取得する。
#Place code here
    REPL = 2
    termsize = os.get_terminal_size()
    pids = [[] for i in cpu_percent]
    cpus = [[] for i in cpu_percent]
    for proc in psutil.process_iter():
        pids[proc.cpu_num()].append(proc)
        try:
            cpus[proc.cpu_num()].append(proc.cpu_percent())
        except psutil.NoSuchProcess:
            cpus[proc.cpu_num()].append(0.0)
    frag=[]
    os.system("clear")
    
    for v,i in enumerate(pids):
        ind = np.argsort(np.array(cpus[v]))[::-1]
        try:
            print("".join([f"\033[48;2;{int(cpus[v][ind[vv]]*25.5)};0;0m{j.name()[:1]:<1}\033[0m" for vv,j in enumerate(np.array(i)[ind])]))
        except psutil.NoSuchProcess:
            print("----")
        except IndexError:
            print("----")
    pre = datetime.now()
    #print(printer.print(frame,chrrepl=1)+"\033[0m",end="")

    #for i,j in enumerate(frag):
        #print(f"\033[32;1m{i:>2}\033[0m{j:>8}")
    est = int(1/(datetime.now()-pre).total_seconds())
    #cv2.imshow("Main", dst)
    key = cv2.waitKey(10)
    if key == 27:
        break
