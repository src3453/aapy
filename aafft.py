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
fftmax = 20000
fftmin = 0
r3p = 0
colormapi = 8
f=None
os.system("clear")

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
    lu=np.ceil((rmsr+rmsl)/2)

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
    if fftclip == False:
        fftmaxn = sqrt(max(v.real * v.real + v.imag * v.imag for v in fft))
        fftmax += (fftmaxn - fftmax) / 5

    oldf = np.log10(fft.__abs__())
    
    try:
        f += (oldf-f)/2
    except TypeError:
        f = oldf
    
    FONTYOFFSET = 0
    #font = pygame.font.Font(r"\\hinagiku\yatsuka_data\python\8x8.ttf", 10)
    #font30 = pygame.font.Font(r"cv2c\sound\16x10.ttf", 20)

    r3 =  ((log10(lu)*10 * np.pi/180) * 3) - 90 * np.pi/180
    r3p += (r3-r3p)/2
    termsize = os.get_terminal_size()
    spr = np.zeros((termsize[1]-1,termsize[0]-1),np.int16)
    fProcessed = (f-3.25)*3
    w = (termsize[1]-(fProcessed*(termsize[1]/2/4))).astype(int)
    print(np.max(w),np.min(w),"        ",end="\r")
    #print(w)
    mask = (np.tile(np.linspace(1,0,spr.shape[0]),(spr.shape[1],1))).T
    for i in range(termsize[0]-1):
        spr=cv2.line(spr,(i,spr.shape[0]),(i,int(np.clip(w[i],0,spr.shape[0]))),255)
    #spr=spr.astype(float)*mask
    print(aa.gray(chars=".$").print(cv2.cvtColor(spr.astype(np.uint8),cv2.COLOR_GRAY2BGR),(0,0),1),end="\r")
