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

    spectrum = np.log(np.abs(fft_shift))
    # test = np.ones((M,N))
    # test[spectrum>10] = 0
    # test[rows-130:rows+130,cols-130:cols+130] = 1
    plot.set_title('spectrum')
    plot.imshow(spectrum, cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    return fft_shift

def apply_bbp(fft, n, d0, w, plot: plt.Axes):
    '''
    巴特沃斯带通滤波器
    H(u,v) = 1 - 1/(1+(D*W/(D**2-D0**2))**2n)
    '''
    M, N = np.shape(fft)
    uu,vv = int(M/2), int(N/2)
    H = np.ones((M,N))
    for u in range(M):
        for v in range(N):
            powD = (u-uu)**2 + (v-vv)**2
            H[u,v] = 1/(1+(np.sqrt(powD)*w/(powD-d0**2))**(2*n))
    filtered_fft = H * fft

    # H_show = np.uint8(255 * (H - np.min(H)) / (np.max(H) - np.min(H)))
    # print(H_show)
    plot.set_title('applied-spectrum')
    plot.imshow(np.log(np.abs(filtered_fft)), cmap='gray')
    # plot.imshow(H_show, cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:uu,0:vv]
    return np.abs(crop)

if __name__ == '__main__':
    # 获取不到一个准确的频谱
    im = cv2.imread('DIP3E_CH05_Original_Images/Fig0516(a)(applo17_boulder_noisy).tif')
    figure = plt.figure()
    plot = figure.add_subplot(221)
    plot.set_title('origin')
    plot.imshow(im)
    plot.set_xticks([])
    plot.set_yticks([])

    fft = fft_im(im, figure.add_subplot(222))
    im_back = apply_bbp(fft, 4, 350, 50, figure.add_subplot(223))

    plotr = figure.add_subplot(224)
    plotr.set_title('results')
    plotr.imshow(im_back, cmap='gray')
    plotr.set_xticks([])
    plotr.set_yticks([])

    # ifft_shift = np.fft.ifftshift(fft)
    # ifft = np.fft.ifft2(ifft_shift)
    # crop = ifft[0:im.shape[0], 0:im.shape[1]]
    # plotr = figure.add_subplot(224)
    # plotr.set_title('results')
    # plotr.imshow(np.abs(crop), cmap='gray')
    # plotr.set_xticks([])
    # plotr.set_yticks([])

    plt.show()
