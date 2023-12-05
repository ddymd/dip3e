#!/bin/env python
#
# 基本边缘检测 - 去噪
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def sobel_x(gray_im, plot: plt.Axes = None):
    sx_kernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    gx_im = cv.filter2D(gray_im, -1, sx_kernel)

    abs_gx_im = np.abs(gx_im)

    if plot is not None:
        plot.set_title('Sobel-X abs gradient')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(abs_gx_im, cmap='gray')
    return abs_gx_im

def sobel_y(gray_im, plot: plt.Axes = None):
    sy_kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    gy_im = cv.filter2D(gray_im, -1, sy_kernel)

    abs_gy_im = np.abs(gy_im)

    if plot is not None:
        plot.set_title('Sobel-Y abs gradient')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(abs_gy_im, cmap='gray')
    return abs_gy_im

def kirsh_nw(gray_im, plot: plt.Axes = None):
    kernel = np.array([[-3,5,5],[-3,0,5],[-3,-3,-3]])
    gradient_im = np.abs(cv.filter2D(gray_im, -1, kernel))

    if plot is not None:
        plot.set_title('kirsh NW gradient')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(gradient_im, cmap='gray')
    return gradient_im

def kirsh_sw(gray_im, plot: plt.Axes = None):
    kernel = np.array([[5,5,-1],[5,0,-3],[-3,-3,-3]])
    gradient_im = np.abs(cv.filter2D(gray_im, -1, kernel))

    if plot is not None:
        plot.set_title('kirsh SW gradient')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(gradient_im, cmap='gray')
    return gradient_im

if __name__ == '__main__':
    figure = plt.figure()

    gray_im = cv.imread('CH10_Images/Fig1016(a)(building_original).tif', cv.IMREAD_GRAYSCALE)
    gray_im = cv.medianBlur(gray_im, 5)
    gray_im = gray_im.astype(np.float32)
    cv.normalize(gray_im, gray_im, 0, 1, cv.NORM_MINMAX)

    oplot = figure.add_subplot(321)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    # x和y方向上的梯度
    g_sx = sobel_x(gray_im, figure.add_subplot(322))
    g_sy = sobel_y(gray_im, figure.add_subplot(323))

    # 梯度图
    gradient_im = g_sx + g_sy

    gplot = figure.add_subplot(324)
    gplot.set_title('sobel gradient')
    gplot.set_xticks([])
    gplot.set_yticks([])
    gplot.imshow(gradient_im, cmap='gray')

    knw_im = kirsh_nw(gray_im, figure.add_subplot(325))
    ksw_im = kirsh_sw(gray_im, figure.add_subplot(326))

    plt.show()

