#!/usr/bin/env python
# 同态滤波 - 根据图像照射&反射建立模型
# H(u,v) = (gamma_H - gamma_L) * (1-e**(-c*(dist**2/d0**2))) + gamma_L
# f(x,y) -> ln -> DFT -> H(u,v) -> IDFT -> exp -> g(x,y)
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

def apply_homomorphic(fft, gamma_h, gamma_l, c, d0):
    '''
    同态滤波, c: 控制函数边坡的锐利度
    '''
    M, N = np.shape(fft)
    uu, vv = int(M/2), int(N/2)

    H = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            powD = (u-uu)**2 + (v-vv)**2
            H[u,v] = (gamma_h - gamma_l)*(1-np.e**(-c*(powD/d0**2))) + gamma_l
    filter_fft = H * fft
    ifft_shift = np.fft.ifftshift(filter_fft)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:uu, 0:vv]
    return np.abs(crop)

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('DIP3E_Original_Images_CH04/Fig0462(a)(PET_image).tif')

    plot = figure.add_subplot(121)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    fft = fft_im(im, plot)

    im_back = apply_homomorphic(fft, 2, 0.25, 1, 80)

    plot1 = figure.add_subplot(122)
    plot1.set_title('homomorphic')
    plot1.set_xticks([])
    plot1.set_yticks([])
    plot1.imshow(im_back, cmap='gray')

    plt.show()
