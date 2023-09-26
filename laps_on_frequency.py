#!/usr/bin/env python

# 拉普拉斯频率域
# H(u,v) = -4*pi**2*dist**2
# delta_f = ifft(H(u,v)*F(u,v))
# res_f = f - c*delta_f
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = rows*2, cols*2
    ext_im = np.zeros((M, N), dtype=np.float32)
    ext_im[0:rows, 0:cols] = gray_im
    # fft and shift
    fft = np.fft.fft2(ext_im)
    fft_shift = np.fft.fftshift(fft)

    # spectrum = np.log(np.abs(fft_shift))
    plot.set_title('origin')
    plot.imshow(gray_im, cmap='gray')

    return fft_shift, ext_im[0:rows, 0:cols]

def apply_laps(fft):
    M, N = np.shape(fft)
    rows, cols = int(M/2), int(N/2)
    mask = np.zeros((M,N))
    for u in range(M):
        for v in range(N):
            mask[u,v] = -4*np.pi**2*((u-rows)**2+(v-cols)**2)
    filtered_im = fft * mask
    ifft_shift = np.fft.ifftshift(filtered_im)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:rows, 0:cols]
    # delta = np.abs(crop)
    return crop

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('DIP3E_Original_Images_CH04/Fig0458(a)(blurry_moon).tif')
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    plot = figure.add_subplot(121)
    plot.set_xticks([])
    plot.set_yticks([])
    fft, uim = fft_im(im, plot)

    delta_f = apply_laps(fft)

    delta = delta_f.real
    delta = delta / (np.max(delta) - np.min(delta))
    res = gray_im - delta
    # res = (res - np.min(res)) / (np.max(res) - np.min(res)) * 255
    print(res)
    plotr = figure.add_subplot(122)
    plotr.imshow(res, cmap='gray')
    plotr.set_xticks([])
    plotr.set_yticks([])

    plt.show()

