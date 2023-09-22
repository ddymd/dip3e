#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def hs_degradation(im, figure: plt.figure, num: int, k: np.float32):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    plot_o = figure.add_subplot(num)
    plot_o.imshow(gray_im, cmap='gray')
    plot_o.set_title('origin gray')
    plot_o.set_xticks([])
    plot_o.set_yticks([])

    # fft
    fft = np.fft.fft2(gray_im)
    fft_shift = np.fft.fftshift(fft)
    # spectrum = np.log(np.abs(fft_shift))

    # plot = figure.add_subplot(num+1)
    # plot.imshow(spectrum, cmap='gray')
    # plot.set_title('spectrum')
    # plot.set_xticks([])
    # plot.set_yticks([])

    h, w = im.shape[:2]
    mask = np.zeros((h,w), dtype=np.float32)
    for v in range(h):
        for u in range(w):
            mask[u,v] = np.e ** (-k*((u**2+v**2)**(5/6)))
    degradation = fft_shift * mask

    ifft_shift = np.fft.ifftshift(degradation)
    ifft = np.fft.ifft2(ifft_shift)
    im_back = np.abs(ifft)
    # im_back = (im_back - np.max(im_back)) / (np.max(im_back)-np.min(im_back))
    return im_back

def mv_degradation(im, figure: plt.figure, a:float=0.1, b:float=0.1, T:float=1):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = im.shape[:2]
    print(rows, cols)

    # 傅里叶变换
    fft = np.fft.fft2(gray_im)
    fft_shift = np.fft.fftshift(fft)
    # 频谱(功率)
    # spectrum = np.log(np.abs(fft_shift))

    mask = np.ones((rows, cols), dtype=np.complex64)
    for v in range(cols):
        for u in range(rows):
            tmp = np.pi*(a*u+b*v)
            if tmp == 0:
                continue
            mask[u,v] = T/(tmp)*np.sin(tmp)*np.e**(-1j*tmp)
    degradation = fft_shift * mask

    ifft_shift = np.fft.ifftshift(degradation)
    ifft = np.fft.ifft2(ifft_shift)
    return np.abs(ifft)

if __name__ == '__main__':
    im_hs = cv2.imread('DIP3E_CH05_Original_Images/Fig0525(a)(aerial_view_no_turb).tif')
    im_mv = cv2.imread('DIP3E_CH05_Original_Images/Fig0526(a)(original_DIP).tif')

    figure = plt.figure()

    im_hs_back = hs_degradation(im_hs, figure, 131, 0.00005)

    plot = figure.add_subplot(133)
    plot.imshow(im_hs_back, cmap='gray')
    plot.set_title('degradation')
    plot.set_xticks([])
    plot.set_yticks([])

    # im_mv_back = mv_degradation(im_mv, figure)

    # plot = figure.add_subplot(111)
    # plot.imshow(im_mv_back, cmap='gray')
    # plot.set_title('degradation')
    # plot.set_xticks([])
    # plot.set_yticks([])

    plt.show()
