#!/bin/env python
#
# 孤立点检测 - 二阶导数(拉普拉斯变换)
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def laplacian_filter(gray_im, plot: plt.Axes = None):
    '''拉普拉斯变换
    变换之前需要将数据转为float类型
    '''
    laplacian_kernel = np.array([[1,1,1],[1,-8,1],[1,1,1]], dtype=np.float32)
    gray_im = gray_im.astype(np.float32)
    laplacian_im = cv.filter2D(gray_im, -1, laplacian_kernel)
    # cvlaplacian_im = cv.Laplacian(gray_im, -1, ksize=3)
    # norm_im = np.zeros_like(laplacian_im)
    # cv.normalize(laplacian_im, norm_im, 0, 255, norm_type=cv.NORM_MINMAX)

    abs_im = np.abs(laplacian_im)

    if plot is not None:
        plot.set_title('laplacian-abs')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(abs_im, cmap='gray')

    max_v = np.max(abs_im)
    return max_v, abs_im

if __name__== '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH10_Images/Fig1004(b)(turbine_blade_black_dot).tif', cv.IMREAD_GRAYSCALE)

    oplot = figure.add_subplot(131)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    max_v, lap_im = laplacian_filter(gray_im, figure.add_subplot(132))

    g_im = np.zeros_like(gray_im)
    g_im[lap_im>(max_v*0.9)] = 255

    gplot = figure.add_subplot(133)
    gplot.set_title('result')
    gplot.set_xticks([])
    gplot.set_yticks([])
    gplot.imshow(g_im, cmap='gray')

    plt.show()
