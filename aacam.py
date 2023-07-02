import sys
import aapy as aa
import cv2
import numpy as np
import os
from datetime import datetime
import dither


# Webカメラを使うときはこちら
cap = cv2.VideoCapture(0)
avg = None

os.system("clear")
est=0
printer = eval(sys.argv[1])
#printer.chars = r" ░▒▓█"
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
    dst = cv2.resize(frame,(termsize[0]//len(" "),min(int(termsize[0]/(16/9)/REPL),termsize[1])-1),interpolation=cv2.INTER_NEAREST)
    
    print(f"{est}fps",end="\r")
    pre = datetime.now()
    printer.print(dst,chrrepl=1)
    est = int(1/(datetime.now()-pre).total_seconds())
    #cv2.imshow("Main", dst)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
