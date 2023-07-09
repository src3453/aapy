"""# AAPy
AAPy provides color ASCII art generator."""
import numpy as np
import cv2
from . import dither as dit

CMODE_ONLYONE = True
CMODE_CONTINUOUS = False
def _print(*text,sep="\t",end="\n"):
    return sep.join(text)+end
def getNearestIndex(lst, num):
    idx = np.abs(np.asarray(lst) - list(num)).argmin()
    return idx

class color_full:
    def __init__(self,char:str="@") -> None:
        self.char:str=char
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrmode:bool=CMODE_ONLYONE,chrrepl:int=1) -> None:
        char_tmp = ""
        out=""
        out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
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
                out+=_print(f"\033[38;2;{img[y,x,2]};{img[y,x,1]};{img[y,x,0]}m{char_tmp}\033[0m",end="")
            out+=_print()
        return out

CHARS=" .-:=+*?#&%@$"
CHARS_BIN=" @"

class color_std:
    """Could not used! Under development."""
    def __init__(self) -> None:
        self.chars = CHARS
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
        out=""
        esc=["\033[31m","\033[32m","\033[34m"]
        out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
        tmp = np.mean([img.flatten() for i in range(0,len(img.flatten()),4)])
        tmp=tmp//(256/len(self.chars))
        chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
        k=0
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for i in range(chrrepl):    
                    out+=_print(f"{esc[k%3]}{chrs[y*img.shape[1]+x]}",end="")
                k+=1
            out+=_print()
        return out


class gray:
    def __init__(self) -> None:
        self.chars = CHARS
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
        out=""
        out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
        tmp = np.average(img,2)
        tmp=tmp//(256/len(self.chars))
        chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                for i in range(chrrepl):    
                    out+=_print(f"{chrs[y,x]}",end="")
            out+=_print()
        return out
    class dither_bin:
        def __init__(self,algo=0) -> None:
            self.chars = CHARS_BIN
            self.algo = algo

        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
            out=""
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = np.average(img,2)
            tmp = dit.binary().dither(tmp,self.algo)
            tmp=tmp//(256/len(self.chars))
            chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
            for y in range(0,img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(chrrepl):    
                        out+=_print(f"{chrs[y%chrs.shape[0],x%chrs.shape[1]]}",end="")
                out+=_print()
            return out
    class dither:
        def __init__(self,K=len(CHARS),algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
            self.chars = CHARS
            self.algo = algo
            self.order = order
            self.k = K

        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
            out=""
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = np.average(img,2)
            tmp = dit.multi().dither(tmp,self.k,self.algo,self.order)
            tmp=tmp//(256/len(self.chars))
            chrs = np.array(list(self.chars))[np.clip(tmp.astype(np.int0),0,len(self.chars)-1)]
            for y in range(0,img.shape[0]):
                for x in range(img.shape[1]):
                    for i in range(chrrepl):    
                        out+=_print(f"{chrs[y%chrs.shape[0],x%chrs.shape[1]]}",end="")
                out+=_print()
            return out

