# -*- coding:utf-8 -*-
from math import log10, sqrt
import os
import sys
import pyaudio
import numpy as np
from scipy import signal
import cv2
import time
import ASCIIArtPy.aapy as aa
def _print(*text,sep="\t",end="\n"):
    return sep.join(text)+end
class gray:
    def __init__(self,chars=" .:+*#&%@$") -> None:
        self.chars = chars
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
        out=""
        #out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
        tmp = np.average(img,2)
        tmp=tmp//(256/len(self.chars))
        chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for i in range(chrrepl):    
                    out+=_print(f"{chrs[y,x]}",end="")
            out+=_print()
        return out
class ext:
        def __init__(self,mode=0,char="@") -> None:
            self.char = char
            self.mode = mode
        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
            out=""
                        #colors=["\033[31m","\033[33m","\033[32m","\033[36m","\033[34m","\033[35m","\033[31m"]
            #out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            k=0
            val = np.zeros((img.shape[0],img.shape[1]))
            val[:,:] = ((img[:,:,2]/42.667).astype(np.uint8)*36+(img[:,:,1]/42.667).astype(np.uint8)*6+(img[:,:,0]/42.667))%216
            for y in range(img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(chrrepl):    
                        out+=_print(f"\033[{3+self.mode}8;5;{(16+int(val[y,x]))}m{self.char}",end="")
                        #out+=_print(f"\033[{(int(val[y,x])%100)}m{chr(max(int(val[y,x]%0x80),0x20))}",end="")
                    k+=1
                out+=_print()
            return out

p = pyaudio.PyAudio()
# set prams
try:
    INPUT_DEVICE_INDEX = int(sys.argv[1])
except IndexError:
    INPUT_DEVICE_INDEX = 0
    print(f"Warning: Input has not selected. Fallback to #0.")
CHUNK = 2 ** 10# 4096
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
#RECORD_SECONDS = 1
threshold = -0.6
WIDTH = 400    
HEIGHT = 350             
window = signal.blackman(CHUNK)       

spr = np.zeros((WIDTH,100,3))   # 大きさ400*300の画面を生成
print(f"Input has been selected to #{INPUT_DEVICE_INDEX}.")            # タイトルバーに表示する文字

def to_db(x, base=1):
        y=20*np.log10(x/base)
        return y
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, frames_per_buffer=CHUNK, input=True, output=False)
text = ""
old=0
x=old
auto = False
fftclip = False
fftmax = 0
fftmin = 0
r3p = 0
colormapi = 8
f=None
#os.system("clear")
spr = np.zeros((1,1),np.int16)
termsize = os.get_terminal_size()
spr = cv2.resize(spr,(termsize[0],1))
while stream.is_active():
    
    start = time.time()
    input = stream.read(CHUNK, exception_on_overflow=False)
    #input = stream.read(CHUNK, exception_on_overflow=False)
    #print(type(input))
    # bufferからndarrayに変換
    ndarrayl = np.frombuffer(input, dtype='int16')[0::2]
    ndarrayr = np.frombuffer(input, dtype='int16')[1::2]
    ''' 高速フーリエ変換をして時間領域から周波数領域にする場合は下1行を追加する '''
    #f = np.fft.fft(ndarray)

    # ndarrayからリストに変換
    # Pythonネイティブのint型にして扱いやすくする
    left = [np.array(i) for i in ndarrayl]
    right = [np.array(i) for i in ndarrayr]


    #mx2=max(a)
    #print(mx2)

    # 試しに0番目に入っているものを表示してみる

    l2 = [int(s) for s in left]
    r2 = [int(s) for s in right]

    
   
    wavel = np.array(l2)
    waver = np.array(r2)

    rmsl = np.sqrt(np.mean([elm * elm for elm in wavel]))
    rmsr = np.sqrt(np.mean([elm * elm for elm in waver]))

    #db = to_db(rms)
    val=(rmsr-rmsl)/(rmsr+rmsl)*90
    x += (val-old)/2
    old=x
    lu=np.ceil((rmsr+rmsl)/2)+1

    r = x * np.pi/180
    r2 = (rmsr-rmsl)/(rmsr+rmsl)*90 * np.pi/180
    wave = (wavel+waver)/2
    try:
        snr = (max(wave[wave >= 0])-max(-1*wave[wave <= 0]))/32768
    except ZeroDivisionError:
        snr = 0
    except ValueError:
        snr = 0
    rx = 0
    mx = max(wave) or abs(min(wave))
    
    fft = np.fft.fft(wave*window, n=CHUNK)
    #fft = np.log10(np.fft.fft(wave*window, n=CHUNK))*10
    

    oldf = np.log10(np.sqrt((fft.real * fft.real + fft.imag * fft.imag)))
    if fftclip == False:
        fftmaxn = oldf
        fftmax += (max(fftmaxn) - fftmax) / 1
    try:
        f += (oldf-f)/1
    except TypeError:
        f = oldf
    f=oldf
    
    FONTYOFFSET = 0
    #font = pygame.font.Font(r"\\hinagiku\yatsuka_data\python\8x8.ttf", 10)
    #font30 = pygame.font.Font(r"cv2c\sound\16x10.ttf", 20)

    r3 =  ((log10(lu)*10 * np.pi/180) * 3) - 90 * np.pi/180
    r3p += (r3-r3p)/2
    termsize = os.get_terminal_size()
    spr = cv2.resize(spr,(termsize[0],1))
    fProcessed = f
    w = np.clip((fProcessed/max(fftmax,2)-0.75)*4*255,0,255).astype(np.uint8)
    #print(np.max(w),np.min(w),fftmax,end="\r")
    #print(w)
    mask = (np.tile(np.linspace(1,0,spr.shape[0]),(spr.shape[1],1))).T
    for i in range(termsize[0]-1):
        spr[0,i]=w[i]
    #spr = np.roll(spr,-1,axis=0)
    #spr=spr.astype(float)*mask
    #chars=" .,:;"
    #print(gray().print(cv2.cvtColor(spr.astype(np.uint8),cv2.COLOR_GRAY2BGR),(0,0),1),end="\r")
    print(ext().print(cv2.applyColorMap(spr.astype(np.uint8),cv2.COLORMAP_JET),(0,0),1),end="\r\033[0m")

