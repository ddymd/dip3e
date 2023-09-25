#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft(im, plot: plt.Axes, plot1: plt.Axes):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = rows*2, cols*2
    ext_im = np.zeros((M, N))
    ext_im[0:rows, 0:cols] = gray_im
    fft = np.fft.fft2(gray_im)
    fft_shift = np.fft.fftshift(fft)

    spectrum = np.log(np.abs(fft_shift))
    plot.imshow(spectrum, cmap='gray')
    plot.set_title('spectrum')
    plot.set_xticks([])
    plot.set_yticks([])

    # mask = np.ones((rows, cols))
    # mask[int(rows/2), int(cols/2)] = 0
    # filter_fft = fft_shift * mask

    fft_shift[int(rows/2), int(cols/2)] = 0
    ifft_shift = np.fft.ifftshift(fft_shift)
    ifft = np.fft.ifft2(ifft_shift)
    im_back = np.abs(ifft)

    ext_fft = np.fft.fft2(ext_im)
    ext_fft_shift = np.fft.fftshift(ext_fft)
    ext_spectrum = np.log(np.abs(ext_fft_shift))
    plot1.imshow(im_back, cmap='gray')
    plot1.set_title('ext-spectrum')
    plot1.set_xticks([])
    plot1.set_yticks([])


if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread('DIP3E_Original_Images_CH04/Fig0429(a)(blown_ic).tif')

    origin_plot = figure.add_subplot(131)
    origin_plot.imshow(im)
    origin_plot.set_title('origin')
    origin_plot.set_xticks([])
    origin_plot.set_yticks([])

    fft_plot = figure.add_subplot(132)
    fft_plot1 = figure.add_subplot(133)
    fft(im, fft_plot, fft_plot1)

    plt.show()
