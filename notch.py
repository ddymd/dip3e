#!/usr/bin/env python

import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_gaussian_notch_filter(figure: plt.figure):
    # 生成高斯核
    rows, cols = 256, 256
    row, col = np.int32(rows/2), np.int32(cols/2)
    sigma = 50
    gauss = cv2.getGaussianKernel(cols, sigma)
    gauss = gauss * gauss.T

    # 生成滤波器掩码
    mask = np.zeros(gauss.shape)
    mask[row-30:row+30, col-30:col+30] = 1
    fourier_filter = mask * gauss

    # 傅里叶变化 & 中心化
    fourier_filter_shift = np.fft.fftshift(np.fft.fft2(fourier_filter))

    # spectrum = np.log(cv2.magnitude(fourier_filter_shift[:,:,0], fourier_filter_shift[:,:,1]))
    spectrum = np.log(np.abs(fourier_filter_shift))
    # 可视化
    # plt.imshow(np.log(np.abs(fourier_filter_shift)), cmap='gray')
    # plt.title('Fourier Filter Perspcetive')
    # plt.show()

    ax2 = figure.add_subplot(131)
    ax2.imshow(spectrum, cmap='gray')
    ax2.set_title('Fourier Filter Perspcetive')
    ax2.set_xticks([])
    ax2.set_yticks([])

def show_ideal_notch_filter(figure: plt.figure):
    rows, cols = 256, 256
    H = np.ones((rows, cols))
    r1, r2, c1, c2 = 60, 196, 60, 196
    H[r1:r2, c1:c2] = 0

    H_dft = np.fft.fft2(H)
    H_dft_shift = np.fft.fftshift(H_dft)
    H_spectrum = np.log(np.abs(H_dft_shift))

    ax2 = figure.add_subplot(132)
    ax2.imshow(H_spectrum, cmap='gray')
    ax2.set_title('Ideal Filter Perspective')
    ax2.set_xticks([])
    ax2.set_yticks([])

def show_butterworth_notch_filter(figure: plt.figure):
    # 定义滤波器阶数和截止频率
    n = 2
    cutoff = 0.4
    # 生成巴特沃斯
    rows, cols = 256, 256
    center_r, center_c = rows/2, cols/2
    H = np.zeros((rows, cols))

    for r in range(rows):
        for c in range(cols):
            dist = np.sqrt((r-center_r)**2 + (c-center_c)**2)
            H[r,c] = 1 / (1+(dist/cutoff)**(2*n))

    # 设置阻带区域为0
    r1, r2, c1, c2 = 60, 196, 60, 196
    H[r1:r2, c1:c2] = 0

    # 傅里叶变换 中心化 幅值 对数
    H_dft = np.fft.fft2(H)
    H_dft_shift = np.fft.fftshift(H_dft)
    H_spectrum = np.log(np.abs(H_dft_shift))

    ax3 = figure.add_subplot(133)
    ax3.imshow(H_spectrum, cmap='gray')
    ax3.set_title('Butterworth Band Stop Filter Spectrum')
    ax3.set_xticks([])
    ax3.set_yticks([])

def ideal_filter(rows, cols, figure: plt.figure = None):
    H = np.ones((rows, cols))
    # r1, r2, c1, c2 = 0, rows-1, np.int32(cols/2-1), np.int32(cols/2+1)

    # D0 = 3
    # crow, ccol = rows//2, cols//2
    # for i in range(rows):
    #     for j in range(cols):
    #         dk = np.sqrt(i - crow)

    r1, r2, c1, c2 = np.int32(rows/2), np.int32(rows/2+1), 0, np.int32(cols/2-3)
    H[r1:r2, c1:c2] = 0
    r1, r2, c1 = np.int32(rows/2), np.int32(rows/2+1), np.int32(cols/2+3)
    H[r1:r2, c1] = 0
    H_dft = np.fft.fft2(H)
    h_dft_shift = np.fft.fftshift(H_dft)
    spectrum = np.log(np.abs(h_dft_shift))
    if figure is not None:
        ax = figure.add_subplot(143)
        ax.imshow(spectrum, cmap='gray')
        ax.set_title('mask spectrum')
        ax.set_xticks([])
        ax.set_yticks([])
    return H

def show_im_dft(im, figure: plt.figure):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(gray_im), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    real_part = dft_shift[:,:,0]
    imag_part = dft_shift[:,:,1]
    spectrum = 20 * np.log(cv2.magnitude(real_part, imag_part))
    angle = np.arctan2(imag_part, real_part)

    fft = np.fft.fft2(gray_im)
    fft_shift = np.fft.fftshift(fft)
    # fft_shift = fft
    spectrum1 = 20 * np.log(np.abs(fft_shift))

    ax1 = figure.add_subplot(141)
    ax1.imshow(gray_im, cmap='gray')
    ax1.set_title('origin gray')
    ax1.set_xticks([])
    ax1.set_yticks([])

    ax2 = figure.add_subplot(142)
    ax2.imshow(spectrum1, cmap='gray')
    ax2.set_title('spectrum')
    ax2.set_xticks([])
    ax2.set_yticks([])

    return fft_shift

if __name__ == '__main__':
    fig = plt.figure()
    # show_gaussian_notch_filter(fig)
    # show_ideal_notch_filter(fig)
    # show_butterworth_notch_filter(fig)
    # plt.show()
    # im = cv2.imread('DIP3E_CH05_Original_Images/Fig0519(a)(florida_satellite_original).tif')
    im = cv2.imread('DIP3E_CH05_Original_Images/Fig0520(a)(NASA_Mariner6_Mars).tif')
    rows, cols = im.shape[:2]
    fft = show_im_dft(im,fig)

    mask = ideal_filter(rows, cols, fig)

    # mask = np.ones((rows, cols), np.uint8)
    # mask[np.int32(rows/2-2):np.int32(rows/2+2), 0:np.int32(cols/2-50)] = 0
    # mask[np.int32(rows/2-2):np.int32(rows/2+2), np.int32(cols/2+50):] = 0

    ffft = mask * fft

    # mask_spectrum = np.log(np.abs(ffft))

    ishift = np.fft.ifftshift(ffft)

    # ax1 = fig.add_subplot(144)
    # ax1.imshow(mask_spectrum, cmap='gray')
    # ax1.set_title('mask_spectrum')
    # ax1.set_xticks([])
    # ax1.set_yticks([])

    img_back = np.fft.ifft2(ishift)
    img_back = np.abs(img_back)
    # img_back = np.uint8(img_back)

    ax = fig.add_subplot(144)
    ax.imshow(img_back, cmap='gray')
    ax.set_title('processed image')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()
