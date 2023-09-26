#!/usr/bin/env python

# 频率域 - 带通滤波器
# H_bp(u,v) = 1 - H_br(u,v)
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = rows*2, cols*2
    ext_im = np.zeros((M, N))
    ext_im[0:rows, 0:cols] = gray_im
    # fft and shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)

    # spectrum = np.log(np.abs(fft_shift))
    plot.set_title('origin')
    plot.imshow(gray_im, cmap='gray')

    return fft_shift

def apply_bbp(fft, n, d0, w):
    '''
    巴特沃斯带通滤波器
    H(u,v) = 1 - 1/(1+(D*W/(D**2-D0**2)))**2n
    '''
    M, N = np.shape(fft)
    uu,vv = int(M/2), int(N/2)
    H = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            powD = (u-uu)**2 + (v-vv)**2
            H[u,v] = 1-1/(1+(np.sqrt(powD)*w/(powD-d0**2)))**(2*n)
    filtered_fft = H * fft
    
