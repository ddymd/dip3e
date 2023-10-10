#!/usr/bin/env python

# 频率域 - 高斯低通滤波器
# H(u,v) = e**(-(dist**2)/(2*D0**2))
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
    ext_im = np.zeros((M,N))
    ext_im[0:rows, 0:cols] = gray_im

    # fft & shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)

    # spectrum = np.log(np.abs(fft_shift))
    plot.set_title('origin')
    plot.imshow(gray_im, cmap='gray')

    return fft_shift

def apply_glpf(fft_im, d0):
    '''
    高斯低通滤波器
    '''
    M,N = np.shape(fft_im)
    mask = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            dist = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            mask[u,v] = np.e**(-(dist**2)/(2*d0**2))
    filtered_fft = fft_im * mask
    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    # crop = ifft[0:int(M/2), 0:int(N/2)]
    return np.abs(ifft)

def apply_ghpf(fft_im, d0):
    '''
    高斯高通滤波器
    '''
    M,N = np.shape(fft_im)
    mask = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            dist = np.sqrt((u-M/2)**2 + (v-N/2)**2)
            mask[u,v] = 1 - np.e**(-(dist**2)/(2*d0**2))
    filtered_fft = fft_im * mask
    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    # crop = ifft[0:int(M/2), 0:int(N/2)]
    return np.abs(ifft)

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread('CH04_Images/Fig0445(a)(characters_test_pattern).tif') #1
    # im = cv2.imread('CH04_Images/Fig0451(a)(satellite_original).tif')      #2
    # im = cv2.imread('CH04_Images/Fig0450(a)(woman_original).tif')            #3

    rows, cols = im.shape[:2]

    # plot_id = 231   # 1
    # plot_id = 131   # 2, 3
    plot_id = 221

    plot_spectrum = figure.add_subplot(plot_id)
    plot_id = plot_id + 1
    plot_spectrum.set_xticks([])
    plot_spectrum.set_yticks([])
    fft = fft_im(im, plot_spectrum)

    # 低通滤波
    # for r in [10,30,60,160,460]:      # 1
    # # for r in [50,20]:                 # 2
    # # for r in [100,80]:                # 3
    #     res_im = apply_glpf(fft, r)
    #     res_im = res_im[0:rows, 0:cols]
    #     plot = figure.add_subplot(plot_id)
    #     plot_id = plot_id + 1
    #     plot.imshow(res_im, cmap='gray')
    #     plot.set_title(str(r))
    #     plot.set_xticks([])
    #     plot.set_yticks([])

    # 高通滤波
    for r in [30,60,160]:
        res_im = apply_ghpf(fft, r)
        res_im = res_im[0:rows, 0:cols]
        plot = figure.add_subplot(plot_id)
        plot_id = plot_id + 1
        plot.imshow(res_im, cmap='gray')
        plot.set_title(str(r))
        plot.set_xticks([])
        plot.set_yticks([])

    plt.show()
