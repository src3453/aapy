"""# AAPy
AAPy provides color ASCII art generator."""
import numpy as np
import cv2
from . import dither as dit

CMODE_ONLYONE = True
CMODE_CONTINUOUS = False
CHARS=" .-:=+*?#&%@$"
CHARS_BIN=" @"
def _print(*text,sep="\t",end="\n"):
    return sep.join(text)+end
def getNearestIndex(lst, num):
    idx = np.abs(np.asarray(lst) - list(num)).argmin()
    return idx

class color:
    class full:
        def __init__(self,mode=0,char:str="@") -> None:
            self.char:str=char
            self.mode:int=mode
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
                    out+=_print(f"\033[{3+self.mode}8;2;{img[y,x,2]};{img[y,x,1]};{img[y,x,0]}m{char_tmp}\033[0m",end="")
                out+=_print()
            return out
    class std:
        """Could not used! Under development."""
        def __init__(self,chars=CHARS,algo=0,order="3x3") -> None:
            self.chars = chars
            self.algo = algo
            self.order = order
        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
            out=""
            img=cv2.cvtColor(img,cv2.COLOR_BGR2HLS_FULL)
            colors=np.array(list("132645"))
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = img[:,:,1]
            tmp=tmp//(256/len(self.chars))
            chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
            k=0
            img[:,:,0] = dit.multi().dither(img[:,:,0],6,order=self.order,algo=self.algo)
            img[:,:,1] = dit.multi().dither(img[:,:,1].astype(np.uint8),1,order=self.order,algo=self.algo)
            colors2 = colors[((((img[:,:,0])/int(256/6))%6).astype(np.uint8))]
            for y in range(img.shape[0]):
                for x in range(img.shape[1]):
                    if img[y,x,1] == 0:
                        ext="\033[0m"
                    else:
                        ext=""
                    for i in range(chrrepl):    
                        out+=_print(f"\033[3{colors2[y,x]};1m{ext}{chrs[y,x]}",end="")
                        #out+=_print(f"\033[3{colors2[y,x]};1m{ext}$",end="")
                    k+=1
                out+=_print()
            return out
    class ext:
        def __init__(self,mode=0,char="@") -> None:
            self.char = char
            self.mode = mode
        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
            out=""
                        #colors=["\033[31m","\033[33m","\033[32m","\033[36m","\033[34m","\033[35m","\033[31m"]
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
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
        class dither:
            def __init__(self,mode=0,char="@",algo=0,order="3x3") -> None:
                self.char = char
                self.mode = mode
                self.algo = algo
                self.order = order
            def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
                out=""
                            #colors=["\033[31m","\033[33m","\033[32m","\033[36m","\033[34m","\033[35m","\033[31m"]
                out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
                k=0
                val = np.zeros((img.shape[0],img.shape[1]))
                for i in range(3):
                    img[:,:,i] = dit.multi().dither(img[:,:,i]*(5/6),6,order=self.order,algo=self.algo)*(5/6)
                val[:,:] = (np.ceil(img[:,:,2]/42.667)*36+np.ceil(img[:,:,1]/42.667)*6+np.ceil(img[:,:,0]/42.667))%216
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        for i in range(chrrepl):    
                            out+=_print(f"\033[{3+self.mode}8;5;{(16+int(val[y,x]))}m{self.char}",end="")
                            #out+=_print(f"\033[{(int(val[y,x])%100)}m{chr(max(int(val[y,x]%0x80),0x20))}",end="")
                        k+=1
                    out+=_print()
                return out
        class LasC:
            def __init__(self,chars=CHARS) -> None:
                self.chars = chars
            def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
                out=""
                img_hls=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                tmp = img_hls[:,:,2]
                tmp=tmp//(256/len(self.chars))
                chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
                out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
                k=0
                img_hls[:,:,2]=255
                img=cv2.cvtColor(img_hls,cv2.COLOR_HSV2BGR)
                val = np.zeros((img.shape[0],img.shape[1]))
                val[:,:] = ((img[:,:,2]/42.667).astype(np.uint8)*36+(img[:,:,1]/42.667).astype(np.uint8)*6+(img[:,:,0]/42.667))%216
                for y in range(img.shape[0]):
                    for x in range(img.shape[1]):
                        for i in range(chrrepl):    
                            out+=_print(f"\033[38;5;{(16+int(val[y,x]))}m{chrs[y,x]}",end="")
                            #out+=_print(f"\033[{(int(val[y,x])%100)}m{chr(max(int(val[y,x]%0x80),0x20))}",end="")
                        k+=1
                    out+=_print()
                return out
            class braille:
                def bin2dot(self,bins):
                    if np.sum(bins) == 0:
                        return " "
                    ans = np.array([[2**0, 2**3],
                                    [2**1, 2**4],
                                    [2**2, 2**5],
                                    [2**6, 2**7]
                                    ])
                
                    tem_bin = np.sum(ans*bins)
                    a = 0b10100000000000
                    return chr(a+tem_bin)

                def __init__(self,algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
                    self.algo = algo
                    self.order = order

                def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
                    out=""
                    img_hls=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                    tmp = img_hls[:,:,2]
                    out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
                    tmp = dit.multi().dither(tmp,1,self.algo,self.order)
                    chrs = tmp.astype(np.uint8)//255
                    img_hls[:,:,2]=255
                    img=cv2.cvtColor(img_hls,cv2.COLOR_HSV2BGR)
                    val = np.zeros((img.shape[0],img.shape[1]))
                    val[::4,::2] = ((img[::4,::2,2]/42.667).astype(np.uint8)*36+(img[::4,::2,1]/42.667).astype(np.uint8)*6+(img[::4,::2,0]/42.667))%216
                    for y in range(0,img.shape[0],4):
                        for x in range(0,img.shape[1],2):
                            out+=_print(f"\033[38;5;{(16+int(val[y,x]))}m{self.bin2dot(chrs[y%chrs.shape[0]:(y+4)%chrs.shape[0],x%chrs.shape[1]:(x+2)%chrs.shape[1]])}",end="")
                        out+=_print()
                    return out
            class block:
                def bin2dot(self,bins):
                    ans = np.array([[2**1, 2**3],
                                    [2**0, 2**2],
                                    ])
                
                    tem_bin = np.sum(ans*bins)
                    return " ▖▘▌▗▄▚▙▝▞▀▛▐▟▜█"[tem_bin]

                def __init__(self,algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
                    self.algo = algo
                    self.order = order

                def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
                    out=""
                    img_hls=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                    tmp = img_hls[:,:,2]
                    out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
                    tmp = dit.multi().dither(tmp,1,self.algo,self.order)
                    chrs = tmp.astype(np.uint8)//255
                    img_hls[:,:,2]=255
                    img=cv2.cvtColor(img_hls,cv2.COLOR_HSV2BGR)
                    val = np.zeros((img.shape[0],img.shape[1]))
                    val[::2,::2] = ((img[::2,::2,2]/42.667).astype(np.uint8)*36+(img[::2,::2,1]/42.667).astype(np.uint8)*6+(img[::2,::2,0]/42.667))%216
                    for y in range(0,img.shape[0]-2,2):
                        for x in range(0,img.shape[1]-2,2):
                            out+=_print(f"\033[38;5;{(16+int(val[y,x]))}m{self.bin2dot(chrs[y%chrs.shape[0]:(y+2)%chrs.shape[0],x%chrs.shape[1]:(x+2)%chrs.shape[1]])}",end="")
                        out+=_print()
                    return out
            class dither:
                def __init__(self,chars=CHARS,K=len(CHARS),algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
                    self.chars = chars
                    self.algo = algo
                    self.order = order
                    self.k = K

                def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
                    out=""
                    out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
                    img_hls=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                    tmp = img_hls[:,:,2]
                    tmp = dit.multi().dither(tmp,self.k,self.algo,self.order)
                    tmp=tmp//(256/len(self.chars))
                    chrs = np.array(list(self.chars))[tmp.astype(np.int0)]
                    img_hls[:,:,2]=255
                    img=cv2.cvtColor(img_hls,cv2.COLOR_HSV2BGR)
                    val = np.zeros((img.shape[0],img.shape[1]))
                    val[:,:] = ((img[:,:,2]/42.667).astype(np.uint8)*36+(img[:,:,1]/42.667).astype(np.uint8)*6+(img[:,:,0]/42.667))%216
                    for y in range(0,img.shape[0]):
                        for x in range(img.shape[1]):
                            for i in range(chrrepl):    
                                out+=_print(f"\033[38;5;{(16+int(val[y,x]))}m{chrs[y%chrs.shape[0],x%chrs.shape[1]]}",end="")
                        out+=_print()
                    return out
    class glitch:
        def __init__(self,mode=0,char="@") -> None:
            self.char = char
            self.mode = mode
        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=1):
            out=""
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            k=0
            for y in range(img.shape[0]):
                for x in range(img.shape[1]):
                    #out+=_print(f"\033[{3+self.mode}8;5;{(16+int(val[y,x]))}m{chr(max(int(val[y,x]%0x80),0x20))}",end="")
                    #out+=_print(f"\033[{(int(val[y,x])%100)}m{chr(int(val[y,x]%0x60)+0x20)}",end="")
                    out+=_print(f"\033[{(int(np.sum(img[y,x]))%256)}m{chr(int(np.sum(img[y,x]))%0x60+0x20)}",end="")
                    #out+=_print(f"\033[{(int(np.sum(img[y,x]))%256)}m{chr(int((img[y,x,0]//5)*32*64+(img[y,x,1]//6)*64+img[y,x,2]//5)).encode('utf-8','replace').decode('utf-8','replace')}",end="")
                    k+=1
                out+=_print()
            return out






class gray:
    def __init__(self,chars=CHARS) -> None:
        self.chars = chars
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
        def __init__(self,chars=CHARS_BIN,algo=0) -> None:
            self.chars = chars
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
        def __init__(self,chars=CHARS,K=len(CHARS),algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
            self.chars = chars
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
    class braille:
        def bin2dot(self,bins):
            if np.sum(bins) == 0:
                return " "
            ans = np.array([[2**0, 2**3],
                            [2**1, 2**4],
                            [2**2, 2**5],
                            [2**6, 2**7]
                            ])
        
            tem_bin = np.sum(ans*bins)
            a = 0b10100000000000
            return chr(a+tem_bin)

        def __init__(self,algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
            self.algo = algo
            self.order = order

        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
            out=""
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = np.average(img,2)
            tmp = dit.multi().dither(tmp,1,self.algo,self.order)
            tmp=np.round(tmp/255)
            chrs = np.clip(tmp.astype(np.int0),0,1)
            for y in range(0,img.shape[0],4):
                for x in range(0,img.shape[1],2):
                    out+=_print(f"{self.bin2dot(chrs[y%chrs.shape[0]:(y+4)%chrs.shape[0],x%chrs.shape[1]:(x+2)%chrs.shape[1]])}",end="")
                out+=_print()
            return out
    class block:
        def bin2dot(self,bins):
            ans = np.array([[2**1, 2**3],
                            [2**0, 2**2],
                            ])
        
            tem_bin = np.sum(ans*bins)
            return " ▖▘▌▗▄▚▙▝▞▀▛▐▟▜█"[tem_bin]

        def __init__(self,algo=dit.ALGO_FLOYD_STEINBERG,order="3x3") -> None:
            self.algo = algo
            self.order = order

        def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),chrrepl:int=2):
            out=""
            out+=_print(f"\033[{loc[0]};{loc[1]}H",end="")
            tmp = np.average(img,2)
            tmp = dit.multi().dither(tmp,1,self.algo,self.order)
            tmp=np.round(tmp/255)
            chrs = np.clip(tmp.astype(np.int0),0,1)
            for y in range(0,img.shape[0]-2,2):
                for x in range(0,img.shape[1]-2,2):
                    out+=_print(f"{self.bin2dot(chrs[y%chrs.shape[0]:(y+2)%chrs.shape[0],x%chrs.shape[1]:(x+2)%chrs.shape[1]])}",end="")
                out+=_print()
            return out


