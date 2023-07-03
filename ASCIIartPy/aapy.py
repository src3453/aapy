"""# AAPy
AAPy provides color ASCII art generator."""
import numpy as np
import cv2
from .dither import binary as dit

CMODE_ONLYONE = True
CMODE_CONTINUOUS = False

def getNearestIndex(lst, num):
    idx = np.abs(np.asarray(lst) - list(num)).argmin()
    return idx

class color_full:
    def __init__(self,char:str="@") -> None:
        self.char:str=char
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrmode:bool=CMODE_ONLYONE,chrrepl:int=1) -> None:
        char_tmp = ""
        print(f"\033[{loc[0]};{loc[1]}H",end="")
        i=0
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                #global char_tmp
                if chrmode:
                    char_tmp = self.char
                else:
                    char_tmp=""
                    for j in range(chrrepl):
                        char_tmp += self.char[i%len(self.char)]
                        i+=1
                print(f"\033[38;2;{img[y,x,2]};{img[y,x,1]};{img[y,x,0]}m{char_tmp}\033[0m",end="")
            print()

CHARS=" .-:=+*?#&%@$"
CHARS_BIN=" @"

class color_std:
    """Could not used! Under development."""
    def __init__(self) -> None:
        self.chars = CHARS
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
        esc=["\033[31m","\033[32m","\033[34m"]
        print(f"\033[{loc[0]};{loc[1]}H",end="")
        tmp = np.mean([img.flatten() for i in range(0,len(img.flatten()),4)])
        tmp=tmp//(256/len(self.chars))
        chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
        k=0
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for i in range(chrrepl):    
                    print(f"{esc[k%3]}{chrs[y*img.shape[1]+x]}",end="")
                k+=1
            print()


class gray:
    def __init__(self) -> None:
        self.chars = CHARS
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
        print(f"\033[{loc[0]};{loc[1]}H",end="")
        tmp = np.average(img,2)
        tmp=tmp//(256/len(self.chars))
        chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for i in range(chrrepl):    
                    print(f"{chrs[y,x]}",end="")
            print()
    class dither_bin:
        def __init__(self,algo=0) -> None:
            self.chars = CHARS_BIN
            self.algo = algo

        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
            print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = np.average(img,2)
            tmp = dit().dither(tmp,self.algo)
            tmp=tmp//(256/len(self.chars))
            chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
            for y in range(0,img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(chrrepl):    
                        print(f"{chrs[y%chrs.shape[0],x%chrs.shape[1]]}",end="")
                print()

