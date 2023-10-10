#!/usr/bin/env python

# 选择性滤波器 - 陷波滤波器
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
    plot.set_title('spectrum')
    plot.imshow(spectrum, cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])
    return fft_shift

def apply_notch(fft, d0, n, plot: plt.Axes):
    M, N = np.shape(fft)
    uu, vv = int(M/2), int(N/2)
    H = np.zeros((M,N))
    # 陷波对1位置
    vk1, uk1 = 59, 76
    # 陷波对2位置
    vk2, uk2 = 59, 158
    # 陷波对3位置
    vk3, uk3 = -54, 84
    # 陷波对4位置
    vk4, uk4 = -55, 165
    for u in range(M):
        for v in range(N):
            dk1 = np.sqrt((u-uu-uk1)**2+(v-vv-vk1)**2)
            if dk1 == 0:
                dk1 = 1
            rdk1 = np.sqrt((u-uu+uk1)**2+(v-vv+vk1)**2)
            if rdk1 == 0:
                rdk1 = 1

            dk2 = np.sqrt((u-uu-uk2)**2+(v-vv-vk2)**2)
            if dk2 == 0:
                dk2 = 1
            rdk2 = np.sqrt((u-uu+uk2)**2+(v-vv+vk2)**2)
            if rdk2 == 0:
                rdk2 = 1

            dk3 = np.sqrt((u-uu-uk3)**2+(v-vv-vk3)**2)
            if dk3 == 0:
                dk3 = 1
            rdk3 = np.sqrt((u-uu+uk3)**2+(v-vv+vk3)**2)
            if rdk3 == 0:
                rdk3 = 1

            dk4 = np.sqrt((u-uu-uk4)**2+(v-vv-vk4)**2)
            if dk4 == 0:
                dk4 = 1
            rdk4 = np.sqrt((u-uu+uk4)**2+(v-vv+vk4)**2)
            if rdk4 == 0:
                rdk4 = 1
            H[u,v] =          (1/(1+(d0/dk1)**(2*n))) * (1/(1+(d0/rdk1)**(2*n)))
            H[u,v] = H[u,v] * (1/(1+(d0/dk2)**(2*n))) * (1/(1+(d0/rdk2)**(2*n)))
            H[u,v] = H[u,v] * (1/(1+(d0/dk3)**(2*n))) * (1/(1+(d0/rdk3)**(2*n)))
            H[u,v] = H[u,v] * (1/(1+(d0/dk4)**(2*n))) * (1/(1+(d0/rdk4)**(2*n)))

    filtered_fft = H * fft
    plot.set_title('filtering spectrum')
    plot.imshow(np.log(np.abs(filtered_fft)), cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:uu, 0:vv]
    return np.abs(crop)

def apply_rect_notch(fft, plot: plt.Axes):
    M, N = np.shape(fft)
    uu, vv = int(M/2), int(N/2)
    H = np.ones((M,N))
    for v in range(N):
        for u in range(M):
            if v > vv-5 and v < vv+5:
                if u > uu - 10 and u < uu + 10:
                    continue
                else:
                    H[u,v] = 0
    filtered_fft = H * fft

    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:uu, 0:vv]

    plot.set_title('filtering spectrum')
    plot.imshow(np.log(np.abs(filtered_fft)), cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    return np.abs(crop)

def main_notch():
    im = cv2.imread('DIP3E_Original_Images_CH04/Fig0464(a)(car_75DPI_Moire).tif')
    # im = cv2.imread('d:\Algorithms\TEM\AMSImage5.jpg')
    figure = plt.figure()
    ploto = figure.add_subplot(221)
    ploto.imshow(im)
    ploto.set_title('origin')
    ploto.set_xticks([])
    ploto.set_yticks([])
    fft = fft_im(im, figure.add_subplot(222))

    im_back = apply_notch(fft, 25, 4, figure.add_subplot(223))

    plotres = figure.add_subplot(224)
    plotres.imshow(im_back, cmap='gray')
    plotres.set_title('results')
    plotres.set_xticks([])
    plotres.set_yticks([])
    plt.show()

def main_rect():
    im = cv2.imread('DIP3E_Original_Images_CH04/Fig0465(a)(cassini).tif')
    figure = plt.figure()
    ploto = figure.add_subplot(221)
    ploto.imshow(im)
    ploto.set_title('origin')
    ploto.set_xticks([])
    ploto.set_yticks([])
    fft = fft_im(im, figure.add_subplot(222))

    im_back = apply_rect_notch(fft, figure.add_subplot(223))

    plotres = figure.add_subplot(224)
    plotres.imshow(im_back, cmap='gray')
    plotres.set_title('results')
    plotres.set_xticks([])
    plotres.set_yticks([])

    plt.show()

if __name__ == '__main__':
    # main_notch()
    main_rect()
