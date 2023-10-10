#!/usr/bin/env python

# 频率域 - 理想低通滤波器
# H(u,v) = 1 while D(u,v) <= D0
# H(u,v) = 0 while D(u,v) > D0
# D(u,v) = ((u-M/2)**2+(v-N/2)**2)**(1/2)
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

def apply_ilpf(fft, r):
    '''
    理想低通滤波器
    '''
    M, N = np.shape(fft)
    mask = np.zeros((M, N))
    uu = int(M/2)
    vv = int(N/2)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-uu)**2+(v-vv)**2)
            if D < r:
                mask[u,v] = 1
    filtered = fft * mask
    ifft_shift = np.fft.ifftshift(filtered)
    ifft = np.fft.ifft2(ifft_shift)
    return np.abs(ifft)

def apply_ihpf(fft, r):
    '''
    理想高通滤波器
    '''
    M, N = np.shape(fft)
    mask = np.ones((M, N))
    uu = int(M/2)
    vv = int(N/2)
    for u in range(M):
        for v in range(N):
            D = np.sqrt((u-uu)**2+(v-vv)**2)
            if D < r:
                mask[u,v] = 0
    filtered = fft * mask
    ifft_shift = np.fft.ifftshift(filtered)
    ifft = np.fft.ifft2(ifft_shift)
    return np.abs(ifft)

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread('CH04_Images/Fig0441(a)(characters_test_pattern).tif')
    rows, cols = im.shape[:2]

    # plot_id = 231
    plot_id = 221
    ploto = figure.add_subplot(plot_id)
    ploto.set_xticks([])
    ploto.set_yticks([])
    plot_id = plot_id + 1
    fft = fft_im(im, ploto)
    M, N = np.shape(fft)
    # 低通滤波
    # for r in [10,30,60,160,460]:
    #     res = apply_ilpf(fft, r)
    #     # crop
    #     res = res[0:rows, 0:cols]
    #     plot = figure.add_subplot(plot_id)
    #     plot_id = plot_id + 1
    #     plot.imshow(res, cmap='gray')
    #     plot.set_title(str(r))
    #     plot.set_xticks([])
    #     plot.set_yticks([])

    # 高通滤波
    for r in [30,60,160]:
        res = apply_ihpf(fft, r)
        # crop
        res = res[0:rows, 0:cols]
        plot = figure.add_subplot(plot_id)
        plot_id = plot_id + 1
        plot.imshow(res, cmap='gray')
        plot.set_title(str(r))
        plot.set_xticks([])
        plot.set_yticks([])

    plt.show()
