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

def gaussian_filter(gray_im, theta: int, plot: plt.Axes = None):
    n = 6 * theta + 1
    blur_im = cv.GaussianBlur(gray_im, (n,n), -1)

    if plot is not None:
        plot.set_title('gaussian-blur theta: {}'.format(theta))
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(blur_im, cmap='gray')

    return blur_im

def cross_zero(gray_im, plot: plt.Axes = None):
    kernel = np.array([[-1,-1,-1],[-1,0,1],[1,1,1]])
    cz_im = cv.filter2D(gray_im, -1, kernel)

    return cz_im

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
    cz_mark = cross_zero(laplacian_im)
    cz_thresh = 0
    cz_im = np.zeros_like(cz_mark)
    cz_im[cz_mark>0] = 1

    czplot = figure.add_subplot(223)
    czplot.set_title('cross zero')
    czplot.set_xticks([])
    czplot.set_yticks([])
    czplot.imshow(cz_mark, cmap='gray')

    plt.show()

