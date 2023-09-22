#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def add_pepper_salt(im):
    pp = 0.01
    sp = 0.01
    rows, cols = im.shape[:2]
    print(im.shape)
    num_pepper = np.ceil(pp * im.size)
    coords_pepper = [np.random.randint(0, i, int(num_pepper)) for i in im.shape[:2]]
    print(np.max(coords_pepper))

    num_salt = np.ceil(sp * im.size)
    coords_salt = [np.random.randint(0, i, int(num_salt)) for i in im.shape[:2]]
    print(np.max(coords_salt))

    im[coords_pepper] = 255
    im[coords_salt] = 0
    return im

def histo_im():
    im = cv2.imread('AMSImage5.jpg')
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([gray_im], [0], None, [256], [0, 256])

    plt.figure()
    plt.title('Histogram')
    plt.xlabel('Bins')
    plt.ylabel('Number of Pixels')
    plt.plot(hist)
    plt.xlim([0,256])
    plt.show()


def show_fft(im):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(gray_im), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    real_part = dft_shift[:,:,0]
    imag_part = dft_shift[:,:,1]
    magnitude_spectrum = 1 + np.log(cv2.magnitude(real_part, imag_part))
    angle = np.arctan2(imag_part, real_part)

    hist = cv2.calcHist([gray_im], [0], None, [256], [0, 256])

    fig = plt.figure()
    # plt.xticks([])
    # plt.yticks([])
    ax1 = fig.add_subplot(334)
    ax1.imshow(magnitude_spectrum, cmap='gray')
    ax1.set_title('Magnitude Spectrum')
    ax1.set_xticks([])
    ax1.set_yticks([])

    ax2 = fig.add_subplot(336)
    ax2.imshow(angle, cmap='gray')
    ax2.set_title('Phase Angle')
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax3 = fig.add_subplot(338)
    ax3.set_title('Histogram')
    ax3.set_xlabel('Bins')
    ax3.set_ylabel('Number of Pixels')
    ax3.set_xlim([0,256])
    ax3.plot(hist, '|')

    ax4 = fig.add_subplot(332)
    ax4.imshow(gray_im, cmap='gray')
    ax4.set_title('Origin gray')
    ax4.set_xticks([])
    ax4.set_yticks([])

    # plt.imshow(magnitude_spectrum, cmap='gray')
    # plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    # plt.show()

    # plt.imshow(angle, cmap='gray')
    # plt.title('Phase Angle'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == '__main__':
    # plt.plot(range(10))
    # plt.show()

    im_file = "DIP3E_CH05_Original_Images/Fig0504(a)(gaussian-noise).tif"
    im = cv2.imread(im_file)
    # ps_im = add_pepper_salt(im)
    # cv2.imshow('ps_im', ps_im)
    show_fft(im)
    cv2.waitKey()
