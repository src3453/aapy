import cv2
import numpy as np
ALGO_FLOYD_STEINBERG = 0
ALGO_BAYER = 1
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
            matrix = [[0, 8, 2, 10],[12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
            for i in range(4):
                for j in range(4):
                    matrix[i][j] = matrix[i][j] * 16

            for i in range(height):
                for j in range(width):
                    if gray[i][j] < matrix[i % 4][j % 4]: # 4区切りずつ判定する
                        gray[i][j] = 0
                        
                    else:
                        gray[i][j] = 255
            return gray
class multi:
    def __init__(self) -> None:
        pass
    def dither(self,img, level):
        width, height = img.shape
        dst = np.zeros_like(img)
        ods = []
        for i in range(level):
            v0 = (256 * i) // level
            v1 = (256 * (i + 1)) // level
            vrange = v1 - v0
            ods.append([v0,v1])
        #print(v0,v1)
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
    
        return dst