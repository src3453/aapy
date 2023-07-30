import cv2
import numpy as np
from numba import jit

ALGO_FLOYD_STEINBERG = 0
ALGO_BAYER = 1
ALGO_FLOYD_STEINBERG_2D = 2
class binary:
    def __init__(self) -> None:
        pass
    def dither(self,gray:cv2.Mat,algo=ALGO_FLOYD_STEINBERG) -> cv2.Mat:
        height, width = gray.shape # 高さ・幅取得
        if algo == ALGO_FLOYD_STEINBERG:
            thresh = 128 # 閾値
            gosa = 0 # 誤差

            for i in range(height):
                for j in range(width):
                    if gray[i][j] + gosa < thresh:
                        gosa = gray[i][j] + gosa - 0 # 誤差を計算
                        gray[i][j] = 0
                    else:
                        gosa = gray[i][j] + gosa - 255 # 誤差を計算
                        gray[i][j] = 255
            return gray
        if algo == ALGO_BAYER:
            gray=cv2.resize(gray,dsize=None,fx=1,fy=1)
            height, width = gray.shape
            #matrix = [[0, 8, 2, 10],[12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
            matrix = [[1, 3],[4, 2]]
            for i in range(2):
                for j in range(2):
                    matrix[i][j] = matrix[i][j] * 51.2

            for i in range(height):
                for j in range(width):
                    if gray[i][j] < matrix[i % 2][j % 2]: # 4区切りずつ判定する
                        gray[i][j] = 0
                        
                    else:
                        gray[i][j] = 255
            return gray
class multi:
    def __init__(self) -> None:
        odtbl2x2 = [
    [1, 3],
    [4, 2]
]
        odtbl3x3 = [
    [3, 7, 4],
    [6, 1, 9],
    [2, 8, 5]
]
        odtbl3x3_b = [
     [7, 9, 5],
     [2, 1, 4],
     [6, 3, 8]
 ]
        odtbl4x4 = [
    [1, 9, 3, 11],
    [13, 5, 15, 7],
    [4, 12, 2, 10],
    [16, 8, 14, 6]
]
        odtbl8x8 = [
    [1, 33, 9, 41, 3, 35, 11, 43],
    [49, 17, 57, 25, 51, 19, 59, 27],
    [13, 45, 5, 37, 15, 47, 7, 39],
    [61, 29, 53, 21, 63, 31, 55, 23],
    [4, 36, 12, 44, 2, 34, 10, 42],
    [52, 20, 60, 28, 50, 18, 58, 26],
    [16, 48, 8, 40, 14, 46, 6, 38],
    [64, 32, 56, 24, 62, 30, 54, 22]
]
        self.odtbls = {       # MaxK
    "2x2":  [5, odtbl2x2],    # 51.2
    "3x3":  [10, odtbl3x3],   # 25.6
    "3x3_b":[10, odtbl3x3_b], # 25.6
    "4x4":  [17, odtbl4x4],   # 15.05
    "8x8":  [65, odtbl8x8]    #  3.93
}
    
    class InvalidOrderTypeException(BaseException):
        pass
    def get_dither_table(self, odtype, vrange, ofs):
        try:
            d, tbl = self.odtbls[odtype]
        except KeyError:
            raise self.InvalidOrderTypeException("Order type must be '2x2', '3x3', '3x3_b', '4x4', '8x8'.")
        if d >= vrange:
            raise Exception("odtbl out of bounds")
    
        w = len(tbl[0])
        h = len(tbl)
        odtbl = [[0 for i in range(w)] for j in range(h)]
    
        for y in range(h):
            for x in range(w):
                odtbl[y][x] = tbl[y][x] * vrange / d + ofs
    
        return w, h, odtbl
    def dither(self,img,level,algo=ALGO_FLOYD_STEINBERG,order="3x3")->np.ndarray[np.float64]:
        """
        orders: 2x2, 3x3, 3x3_b, 4x4, 8x8
        MaxK:   51.2 25.6 25.6 15.0 3.93"""
        odtype = order
        width, height = img.shape
        dst = np.zeros(img.shape)
        ods = []
        tw, th, _ = self.get_dither_table(odtype, 256, 0)
        for i in range(level):
            v0 = (256 * i) // level
            v1 = (256 * (i + 1)) // level
            vrange = v1 - v0
            if algo==ALGO_FLOYD_STEINBERG:
                ods.append([v0,v1])
            if algo==ALGO_BAYER:
                _, _, od = self.get_dither_table(odtype, vrange, v0)
                ods.append([v0, v1, od])
        #print(v0,v1)
        if algo==ALGO_FLOYD_STEINBERG:
            error = 0
            src = img.copy()
            for v0,v1 in ods:
                for y in range(height):
                    for x in range(width):
                        v = src[x, y]
                        if v0 <= v and v <= v1:
                            if v+error < (v1+v0)//2:
                                error = img[x,y] + error - v0
                                dst[x,y] = v0
                            else:
                                error = img[x,y] + error - v1
                                dst[x,y] = v1
        if algo==ALGO_BAYER:
            src = img.copy()
            for v0,v1,od in ods:
                for y in range(height):
                    dy = y % th
                    for x in range(width):
                        dx = x % tw
                        v = src[x, y]
                        if v0 <= v and v <= v1:
                            if v < od[dy][dx]:
                                dst[x,y] = v0
                            else:
                                dst[x,y] = v1
        return dst
    
    
    
    #@jit(nopython=False)
    