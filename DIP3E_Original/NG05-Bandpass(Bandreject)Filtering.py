#!/usr/bin/env python

# 频率域 - 带通滤波器
# H_bp(u,v) = 1 - H_br(u,v)
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def fft_im(im, plot: plt.Axes = None):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    rows, cols = gray_im.shape[:2]
    M, N = cv2.getOptimalDFTSize(rows), cv2.getOptimalDFTSize(cols)
    print('origin size({},{}) vs padded size({},{})'.format(rows, cols, M, N))
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

def apply_bbp(fft, n, d0, w, plot: plt.Axes):
    '''
    巴特沃斯带通滤波器
    H(u,v) = 1 - 1/(1+(D*W/(D**2-D0**2))**2n)
    '''
    M, N = np.shape(fft)
    uu,vv = int(M/2), int(N/2)
    H = np.ones((M,N))
    for u in range(M):
        for v in range(N):
            powD = (u-uu)**2 + (v-vv)**2
            if powD - d0**2 == 0:
                H[u,v] = 0
            else:
                H[u,v] = 1/(1+(np.sqrt(powD)*w/(powD-d0**2))**(2*n))
    filtered_fft = H * fft

    # H_show = np.uint8(255 * (H - np.min(H)) / (np.max(H) - np.min(H)))
    # print(H_show)
    plot.set_title('applied-spectrum')
    filtered_fft[filtered_fft==0] = 1
    plot.imshow(np.log(np.abs(filtered_fft)), cmap='gray')
    # plot.imshow(H_show, cmap='gray')
    plot.set_xticks([])
    plot.set_yticks([])

    ifft_shift = np.fft.ifftshift(filtered_fft)
    ifft = np.fft.ifft2(ifft_shift)
    # crop = ifft[0:uu,0:vv]
    return np.abs(ifft)

def show_hist(im, plot):
    hist = cv2.calcHist([im], [0], None, [256], [0, 256])
    # plot.set_title("Grayscale Histogram")
    # plot.xlabel("Bins")
    # plot.ylabel("Number of Pixels")
    # plot.imshow(hist, cmap='gray')
    # plot.xlim([0,256])
    return hist    

if __name__ == '__main__':
    # 获取不到一个准确的频谱
    im = cv2.imread('CH05_Images/Fig0516(a)(applo17_boulder_noisy).tif')
    rows, cols = im.shape[:2]
    figure = plt.figure()
    hist = show_hist(im, None)
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.plot(hist)
    plt.xlim([0,256])
    # plot = figure.add_subplot(221)
    # plot.set_title('origin')
    # plot.imshow(im)
    # plot.set_xticks([])
    # plot.set_yticks([])

    # fft = fft_im(im, figure.add_subplot(222))
    # im_back = apply_bbp(fft, 4, 190, 30, figure.add_subplot(223))
    # im_back = im_back[0:rows, 0:cols]

    # plotr = figure.add_subplot(224)
    # plotr.set_title('results')
    # plotr.imshow(im_back, cmap='gray')
    # plotr.set_xticks([])
    # plotr.set_yticks([])

    # ifft_shift = np.fft.ifftshift(fft)
    # ifft = np.fft.ifft2(ifft_shift)
    # crop = ifft[0:im.shape[0], 0:im.shape[1]]
    # plotr = figure.add_subplot(224)
    # plotr.set_title('results')
    # plotr.imshow(np.abs(crop), cmap='gray')
    # plotr.set_xticks([])
    # plotr.set_yticks([])

    # show_hist(im, figure.add_subplot(224))

    plt.show()
