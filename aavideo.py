import argparse
import sys
import ASCIIArtPy.aapy as aa
import cv2
import numpy as np
import os
from datetime import datetime
import ASCIIArtPy.dither

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る
parser.add_argument('-p',"--path", help='', default=0)    # 必須の引数を追加
parser.add_argument('-m',"--method", help='', default="aa.gray.dither_bin()")  
parser.add_argument('-c',"--chars", help='', default=" .-:=+*#%@")    # 必須の引数を追加
parser.add_argument('-x',"--width", help='', default=1, type=int)    # 必須の引数を追加
parser.add_argument('-y',"--height", help='', default=1, type=int)
args = parser.parse_args()
# Webカメラを使うときはこちら
cap = cv2.VideoCapture(args.path)

os.system("clear")
est=0
printer = eval(args.method)
    
printer.chars = args.chars
    # ░▒▓█ 
    # ▘▖▝▗▀▄▚▞▐▋▛▙▜▟█ /  ▘▀▚▛█
    # ▁▂▃▄▅▆▇█
    # .-:=+*#%@
    # ▏▎▍▌▋▊▉█
    # ▖▖▚▚▜▜█
    #  ⡀⠈⡐⠡⡘⡙⡛⣾⣿▒▓█
    # ´-²;º=\LzïY[j1kéñü6Søq©AKÈRNÒÂÕ¶ / Latin-1

#printer.chars=["▓ ▓ ","▓▒▒▓","▓▒▓▒","▓▒▓▓","▓▓▓▓","▓▓▓▓","█▓█▓","▓█▓█","██▓█","████"]


while True:
    # 1フレームずつ取得する。
    ret, frame = cap.read()
    if not ret:
        break
#Place code here
    REPL = 2
    termsize = os.get_terminal_size()
    dst = cv2.resize(frame,(termsize[0]//len(" ")*args.width,(min(int(termsize[0]/(16/9)/REPL),termsize[1])-1)*args.height),interpolation=cv2.INTER_NEAREST)
    
    print(f"{est}fps",end="\033[0m\r")
    pre = datetime.now()
    print(printer.print(dst,chrrepl=1)+"\033[0m",end="")
    est = int(1/(datetime.now()-pre).total_seconds())
    #cv2.imshow("Main", dst)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
