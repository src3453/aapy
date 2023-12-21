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
os.system("clear")
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
    cpu_percent = psutil.cpu_percent(interval=args.interval,percpu=True)
    frame = cv2.hconcat([frame,cv2.applyColorMap((np.reshape(np.array(cpu_percent)*2.55,(len(cpu_percent),1))).astype(np.uint8),cv2.COLORMAP_VIRIDIS)])
    frame = frame[:,1:,:]
    print('\033[0m\r')
    pre = datetime.now()
    print(printer.print(frame,chrrepl=1)+"\033[0m",end="")
    print(f"\033[0;0H",end="")
    for i,j in enumerate(cpu_percent):
        print(f"\033[32;1m{i:>2}\033[0m{j:>5}")
    est = int(1/(datetime.now()-pre).total_seconds())
    #cv2.imshow("Main", dst)
    key = cv2.waitKey(10)
    if key == 27:
        break
