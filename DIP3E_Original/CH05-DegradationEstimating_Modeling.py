#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes=None):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    # pad image
    M, N = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    print('origin size({0},{1}) vs padded size({2},{3})'.format(rows, cols, M, N))
    ext_im = np.zeros((M, N))
    ext_im[0:rows, 0:cols] = gray_im
    # fft and shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)

    if plot is not None:
        spectrum = np.log(np.abs(fft_shift))
        plot.set_title('spectrum')
        plot.imshow(spectrum, cmap='gray')
        plot.set_xticks([])
        plot.set_yticks([])

    return fft_shift

def hs_degradation(im, figure: plt.figure, num: int, k: np.float32):
    # 大气湍流退化模型 H(u,v) = e**(-k(u**2+v**2)**(5/6))
    rows, cols = im.shape[:2]
    # 傅里叶变换
    fft_shift = fft_im(im)

    M, N = fft_shift.shape[:2]
    cm, cn = int(M/2), int(N/2)
    mask = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            mask[u,v] = np.e ** (-k*(((u-cm)**2+(v-cn)**2)**(5/6)))
    degradation = fft_shift * mask

    ifft_shift = np.fft.ifftshift(degradation)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:rows, 0:cols]
    im_back = np.abs(crop)

    plot_r = figure.add_subplot(num)
    plot_r.imshow(im_back, cmap='gray')
    plot_r.set_title('res_k'+str(k))
    plot_r.set_xticks([])
    plot_r.set_yticks([])
    num = num + 1

    return im_back

def mv_degradation(im, figure: plt.figure, a:float=0.1, b:float=0.1, T:float=1):
    # 运动退化模型 H(u,v) = (T/PI(ua+vb))sin(PI(ua+vb))e**(-jPI(ua+vb))
    rows, cols = im.shape[:2]

    # 傅里叶变换
    fft_shift = fft_im(im)
    M, N = fft_shift.shape[:2]
    cm, cn = int(M/2), int(N/2)

    mask = np.ones((M, N), dtype=np.complex64)
    for u in range(M):
        for v in range(N):
            tmp = np.pi*(a*(u-cm)+b*(v-cn))
            if tmp == 0:
                continue
            mask[u,v] = T/(tmp)*np.sin(tmp)*np.e**(-1j*tmp)
    degradation = fft_shift * mask

    ifft_shift = np.fft.ifftshift(degradation)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:rows, 0:cols]
    im_back = np.abs(crop)

    plot_r = figure.add_subplot(122)
    plot_r.imshow(im_back, cmap='gray')
    plot_r.set_title('res_a{a}_b{b}_T{T}'.format(a=a, b=b, T=T))
    plot_r.set_xticks([])
    plot_r.set_yticks([])

    return im_back

if __name__ == '__main__':
    figure = plt.figure()

    # ------------- Part One
    # im_hs = cv2.imread('CH05_Images/Fig0525(a)(aerial_view_no_turb).tif')

    # plot = figure.add_subplot(221)
    # plot.imshow(im_hs, cmap='gray')
    # plot.set_title('origin')
    # plot.set_xticks([])
    # plot.set_yticks([])

    # hs_degradation(im_hs, figure, 222, 0.0025)
    # hs_degradation(im_hs, figure, 223, 0.001)
    # hs_degradation(im_hs, figure, 224, 0.00025)

    # ------------- Part Two
    im_mv = cv2.imread('CH05_Images/Fig0526(a)(original_DIP).tif')

    plot = figure.add_subplot(121)
    plot.imshow(im_mv, cmap='gray')
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])

    mv_degradation(im_mv, figure)

    plt.show()
