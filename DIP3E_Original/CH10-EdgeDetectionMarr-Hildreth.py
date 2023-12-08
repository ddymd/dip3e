#!/bin/env python
#
# 边缘检测Marr-Hildreth
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def laplacian_filter(gray_im, plot: plt.Axes = None):
    '''拉普拉斯变换
    变换之前需要将数据转为float类型
    '''
    laplacian_kernel = np.array([[1,1,1],[1,-8,1],[1,1,1]], dtype=np.float32)
    laplacian_im = cv.filter2D(gray_im, -1, laplacian_kernel)

    if plot is not None:
        plot.set_title('laplacian')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(abs_im, cmap='gray')

    return laplacian_im

def gaussian_filter(gray_im, sigma: int, plot: plt.Axes = None):
    n = 6 * sigma + 1
    blur_im = cv.GaussianBlur(gray_im, (n,n), sigma)

    if plot is not None:
        plot.set_title('gaussian-blur theta: {}'.format(sigma))
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(blur_im, cmap='gray')

    return blur_im

def cross_zero(gray_im, plot: plt.Axes = None):
    ext_im = cv.copyMakeBorder(gray_im, 1, 1, 1, 1, cv.BORDER_REPLICATE)
    th_im = np.zeros_like(gray_im)
    m, n = np.shape(ext_im)
    for i in range(1,m-1):
        for j in range(1,n-1):
            a = np.abs(ext_im[i-1,j-1] - ext_im[i+1,j+1])
            ia_max = np.abs(ext_im[i-1,j-1]) if np.abs(ext_im[i-1,j-1]) > np.abs(ext_im[i+1,j+1]) else np.abs(ext_im[i+1,j+1])
            th_im[i-1,j-1] = a if a > ia_max else 0

            b = np.abs(ext_im[i-1,j] - ext_im[i+1,j])
            ib_max = np.abs(ext_im[i-1,j]) if np.abs(ext_im[i-1,j]) > np.abs(ext_im[i+1,j]) else np.abs(ext_im[i+1,j])
            if b > ib_max:
                th_im[i-1,j-1] = b if b > th_im[i-1,j-1] else th_im[i-1,j-1]

            c = np.abs(ext_im[i,j-1] - ext_im[i,j+1])
            ic_max = np.abs(ext_im[i,j-1]) if np.abs(ext_im[i,j-1]) > np.abs(ext_im[i,j+1]) else np.abs(ext_im[i,j+1])
            if c > ic_max:
                th_im[i-1,j-1] = c if c > th_im[i-1,j-1] else th_im[i-1,j-1]

            d = np.abs(ext_im[i-1,j+1] - ext_im[i+1,j-1])
            id_max = np.abs(ext_im[i-1,j+1]) if np.abs(ext_im[i-1,j+1]) > np.abs(ext_im[i+1,j-1]) else np.abs(ext_im[i+1,j-1])
            if d > id_max:
                th_im[i-1,j-1] = d if d > th_im[i-1,j-1] else th_im[i-1,j-1]
    return th_im

if __name__ == '__main__':
    figure = plt.figure()

    gray_im = cv.imread('CH10_Images/Fig1016(a)(building_original).tif', cv.IMREAD_GRAYSCALE)
    gray_im = gray_im.astype(np.float32)

    oplot = figure.add_subplot(221)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    blur_im = gaussian_filter(gray_im, 6)
    laplacian_im = laplacian_filter(blur_im)

    mhplot = figure.add_subplot(222)
    mhplot.set_title('Marr-Hildreth')
    mhplot.set_xticks([])
    mhplot.set_yticks([])
    mhplot.imshow(laplacian_im, cmap='gray')

    # 过零点如何计算？
    cz_im = cross_zero(laplacian_im)
    cz_thresh = 0
    cz_im0 = np.zeros_like(cz_im)
    cz_im0[cz_im>cz_thresh] = 1

    czplot = figure.add_subplot(223)
    czplot.set_title('cross zero - thresh: 0')
    czplot.set_xticks([])
    czplot.set_yticks([])
    czplot.imshow(cz_im0, cmap='gray')

    thresh_4 = np.max(cz_im) * 0.04
    print(thresh_4)

    cz_im1 = np.zeros_like(cz_im)
    cz_im1[cz_im>thresh_4] = 1

    cz1plot = figure.add_subplot(224)
    cz1plot.set_title('cross zero - thresh: {}'.format(thresh_4))
    cz1plot.set_xticks([])
    cz1plot.set_yticks([])
    cz1plot.imshow(cz_im1, cmap='gray')

    plt.show()

