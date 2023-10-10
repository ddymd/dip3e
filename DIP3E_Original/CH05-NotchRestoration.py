#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(gray_im, plot: plt.Axes = None):
    rows, cols = gray_im.shape[:2]
    M, N = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    print('origin size({},{}) vs padded size({},{})'.format(rows, cols, M, N))
    # pad image
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

def notch_bandreject(gray_im, plot: plt.Axes, plot_fft: plt.Axes = None):
    '''
    陷波带阻滤波
    '''
    rows, cols = gray_im.shape[:2]
    fft_shift = fft_im(gray_im, plot_fft)

    M, N = fft_shift.shape[:2]
    uu, vv = int(M/2), int(N/2)
    H = np.ones((M, N))
    for v in range(N):
        for u in range(M):
            if v > vv-5 and v < vv+5:
                if u > uu - 20 and u < uu + 20:
                    continue
                else:
                    H[u,v] = 0

    filtered = H * fft_shift
    ifft_shift = np.fft.ifftshift(filtered)
    ifft = np.fft.ifft2(ifft_shift)
    crop = ifft[0:rows, 0:cols]

    filtered[filtered==0] = 1
    plot.set_title('H-spectrum')
    plot.imshow(np.log(np.abs(filtered)), cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    return np.abs(crop)

if __name__ == '__main__':
    fig = plt.figure()

    im = cv2.imread('CH05_Images/Fig0519(a)(florida_satellite_original).tif')
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ploto = fig.add_subplot(221)
    ploto.imshow(im)
    ploto.set_title('results')
    ploto.set_xticks([])
    ploto.set_yticks([])

    im_back = notch_bandreject(gray_im, fig.add_subplot(224), fig.add_subplot(223))
    plotres = fig.add_subplot(222)
    plotres.imshow(im_back, cmap='gray')
    plotres.set_title('results')
    plotres.set_xticks([])
    plotres.set_yticks([])

    plt.show()
