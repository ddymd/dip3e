#!/usr/bin/env python
#
# 高频强调滤波
# g(x,y) = ifft((k1+k2*H(u,v))*F(u,v))
# H(u,v) 为高通滤波器, k1控制距离原点的偏移量, k2控制高频的贡献
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    print('origin size({0},{1}) vs padded size({2},{3})'.format(rows, cols, M, N))
    ext_im = np.zeros((M, N))
    ext_im[0:rows, 0:cols] = gray_im
    # fft and shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)

    # spectrum = np.log(np.abs(fft_shift))
    plot.set_title('origin')
    plot.imshow(gray_im, cmap='gray')

    return fft_shift

def apply_hfe(fft_im, k1, k2, d0):
    '''
    高斯高频强调滤波器
    '''
    M,N = np.shape(fft_im)
    mask = np.zeros((M,N))
    uu,vv = int(M/2), int(N/2)
    for u in range(M):
        for v in range(N):
            dist = np.sqrt((u-uu)**2 + (v-vv)**2)
            mask[u,v] = k1 + k2 * np.e**(-(dist**2)/(2*d0**2))
    filtered_fft = fft_im * mask
    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    return np.abs(ifft)

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('CH04_Images/Fig0459(a)(orig_chest_xray).tif')
    rows, cols = im.shape[:2]
    plot = figure.add_subplot(221)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    fft = fft_im(im, plot)

    res_im = apply_hfe(fft, 0, 1, 40)
    # crop
    res_im = res_im[0:rows,0:cols]
    plot1 = figure.add_subplot(222)
    plot1.set_title('gaussian')
    plot1.set_xticks([])
    plot1.set_yticks([])
    plot1.imshow(res_im, cmap='gray')

    res_im1 = apply_hfe(fft, 0.5, 0.75, 40)
    res_im1 = (res_im1 - np.min(res_im1)) / (np.max(res_im1) - np.min(res_im1))
    res_im1 = np.uint8(res_im1*255)

    plot2 = figure.add_subplot(223)
    plot2.set_title('hf_gaussian')
    plot2.set_xticks([])
    plot2.set_yticks([])
    plot2.imshow(res_im1, cmap='gray')

    # 直方图均衡
    eh_im = cv2.equalizeHist(res_im1)

    plot3 = figure.add_subplot(224)
    plot3.set_title('eh_gaussian')
    plot3.set_xticks([])
    plot3.set_yticks([])
    plot3.imshow(eh_im, cmap='gray')

    plt.show()
