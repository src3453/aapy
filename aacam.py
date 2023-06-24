import aapy as aa
import cv2
import numpy as np
import os
from datetime import datetime

# Webカメラを使うときはこちら
cap = cv2.VideoCapture(0)
avg = None

os.system("clear")
est=0
while True:
    # 1フレームずつ取得する。
    ret, frame = cap.read()
    if not ret:
        break
#Place code here
    REPL=2
    termsize = os.get_terminal_size()
    dst = cv2.resize(frame,(termsize[0]//REPL,min(int(termsize[0]/(16/9)/REPL),termsize[1])-1),interpolation=cv2.INTER_NEAREST)
    printer = aa.gray()
    printer.chars = " ▁▂▃▄▅▆▇█"# ░▒▓█  ▁▂▃▄▅▆▇█
    print(f"{est}fps",end="\r")
    pre = datetime.now()
    printer.print(dst,chrrepl=REPL)
    est = int(1/(datetime.now()-pre).total_seconds())
    #cv2.imshow("Main", dst)
    key = cv2.waitKey(10)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
