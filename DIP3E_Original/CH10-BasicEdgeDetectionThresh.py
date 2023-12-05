#!/bin/env python
#
# 基本边缘检测
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

if __name__ == '__main__':
    figure = plt.figure()

    gray_im = cv.imread('CH10_Images/Fig1016(a)(building_original).tif', cv.IMREAD_GRAYSCALE)
    gray_im = gray_im.astype(np.float32)
    # cv.normalize(gray_im, gray_im, 0, 1, cv.NORM_MINMAX)

    oplot = figure.add_subplot(221)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    # x和y方向上的梯度
    g_sx = sobel_x(gray_im)
    g_sy = sobel_y(gray_im)
    # 梯度图
    gradient_im = g_sx + g_sy
    thresh_g = np.max(gradient_im) * 0.33
    thresh_im = np.zeros_like(gradient_im)
    thresh_im[gradient_im>thresh_g] = 1

    gplot = figure.add_subplot(223)
    gplot.set_title('thresh by 33%')
    gplot.set_xticks([])
    gplot.set_yticks([])
    gplot.imshow(thresh_im, cmap='gray')

    blur_im = cv.medianBlur(gray_im, 5)

    bplot = figure.add_subplot(222)
    bplot.set_title('blurred origin')
    bplot.set_xticks([])
    bplot.set_yticks([])
    bplot.imshow(blur_im, cmap='gray')

    # x和y方向上的梯度
    g_sx_blur = sobel_x(blur_im)
    g_sy_blur = sobel_y(blur_im)
    # 梯度图
    blur_gradient_im = g_sx_blur + g_sy_blur
    thresh_bg = np.max(blur_gradient_im) * 0.33
    blur_thresh_im = np.zeros_like(blur_gradient_im)
    blur_thresh_im[blur_gradient_im>thresh_bg] = 1

    bgplot = figure.add_subplot(224)
    bgplot.set_title('blurred - thresh by 33%')
    bgplot.set_xticks([])
    bgplot.set_yticks([])
    bgplot.imshow(blur_thresh_im, cmap='gray')

    plt.show()

