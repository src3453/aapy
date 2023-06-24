"""# AAPy
AAPy provides color ASCII art generator."""
import numpy as np

CMODE_ONLYONE = True
CMODE_CONTINUOUS = False

class color:
    def __init__(self) -> None:
        pass
    def print(self,img:np.ndarray,loc:tuple[int,int]=(0,0),char:str="██",chrmode:bool=CMODE_ONLYONE,chrrepl:int=2) -> None:
        char_tmp = ""
        print(f"\033[{loc[0]};{loc[1]}H",end="")
        i=0
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                #global char_tmp
                if chrmode:
                    char_tmp = char
                else:
                    char_tmp=""
                    for j in range(chrrepl):
                        char_tmp += char[i%len(char)]
                        i+=1
                print(f"\033[38;2;{img[y,x,2]};{img[y,x,1]};{img[y,x,0]}m{char_tmp}\033[0m",end="")
            print()
class gray:
    def __init__(self) -> None:
        self.chars=" .,:;+*?%$#@"
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