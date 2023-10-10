#!/usr/bin/env python

# 拉普拉斯频率域
# H(u,v) = -4*pi**2*dist**2
# delta_f = ifft(H(u,v)*F(u,v))
# res_f = f - c*delta_f
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes = None):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    print('origin size({},{}) vs padded size({},{})'.format(rows, cols, M, N))

    # normal
    normal_im = np.zeros_like(gray_im)
    cv2.normalize(gray_im, normal_im, norm_type=cv2.NORM_MINMAX)

    # pad image
    ext_im = np.zeros((M, N), dtype=np.float32)
    ext_im[0:rows, 0:cols] = normal_im
    # fft and shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)
    if plot is not None:
        spectrum = np.log(np.abs(fft_shift))
        plot.set_title('spectrum')
        plot.imshow(gray_im, cmap='gray')
        plot.set_xticks([])
        plot.set_yticks([])
    return fft_shift

def apply_laps(fft):
    M, N = np.shape(fft)
    cm, cn = int(M/2), int(N/2)
    H = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            H[u,v] = -4*(np.pi**2)*((u-cm)**2+(v-cn)**2)
    filtered_im = fft * H
    ifft_shift = np.fft.ifftshift(filtered_im)
    ifft = np.fft.ifft2(ifft_shift)
    return np.abs(ifft)

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('CH04_Images/Fig0458(a)(blurry_moon).tif')
    rows, cols = im.shape[:2]
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    fft = fft_im(im, figure.add_subplot(121))

    delta_f = np.exp(np.log(apply_laps(fft)))
    # crop
    delta_f = delta_f[0:rows, 0:cols]
    print(delta_f, np.max(delta_f), np.min(delta_f))

    # normal
    # normal_im = np.zeros_like(gray_im)
    # cv2.normalize(gray_im, normal_im, norm_type=cv2.NORM_MINMAX)

    res = gray_im - delta_f
    print(res)
    plotr = figure.add_subplot(122)
    plotr.imshow(res, cmap='gray')
    plotr.set_title('result')
    plotr.set_xticks([])
    plotr.set_yticks([])

    plt.show()

