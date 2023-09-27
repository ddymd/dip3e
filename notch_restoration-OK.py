#!/usr/bin/env python

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

def notch_bandreject(fft, plot: plt.Axes):
    '''
    陷波带阻滤波
    '''
    M, N = np.shape(fft)
    uu, vv = int(M/2), int(N/2)
    H = np.ones((M, N))
    for v in range(N):
        for u in range(M):
            if v > vv-5 and v < vv+5:
                if u > uu - 20 and u < uu + 20:
                    continue
                else:
                    H[u,v] = 0
    filtered = H * fft
    ifft_shift = np.fft.ifftshift(filtered)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:uu, 0:vv]

    plot.set_title('H-spectrum')
    plot.imshow(np.log(np.abs(filtered)), cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    return np.abs(crop)

if __name__ == '__main__':
    fig = plt.figure()

    im = cv2.imread('DIP3E_CH05_Original_Images/Fig0519(a)(florida_satellite_original).tif')

    ploto = fig.add_subplot(221)
    ploto.imshow(im)
    ploto.set_title('results')
    ploto.set_xticks([])
    ploto.set_yticks([])

    fft = fft_im(im, fig.add_subplot(223))

    im_back = notch_bandreject(fft, fig.add_subplot(224))
    plotres = fig.add_subplot(222)
    plotres.imshow(im_back, cmap='gray')
    plotres.set_title('results')
    plotres.set_xticks([])
    plotres.set_yticks([])

    plt.show()
