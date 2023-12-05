#!/bin/env python
#
# 线检测 - 特定方向
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def laplacian_filter(gray_im, plot: plt.Axes = None):
    # 水平
    # laplacian_kernel = np.array([[-1,-1,-1],[2,2,2],[-1,-1,-1]], dtype=np.float32)
    # +45°
    laplacian_kernel = np.array([[2,-1,-1],[-1,2,-1],[-1,-1,2]], dtype=np.float32)
    # 垂直
    # laplacian_kernel = np.array([[-1,2,-1],[-1,2,-1],[-1,2,-1]], dtype=np.float32)
    # -45°
    # laplacian_kernel = np.array([[-1,-1,2],[-1,2,-1],[2,-1,-1]], dtype=np.float32)
    gray_im = gray_im.astype(np.float32)
    laplacian_im = cv.filter2D(gray_im, -1, laplacian_kernel)

    if plot is not None:
        plot.set_title('laplacian-45°')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(laplacian_im, cmap='gray')
    return laplacian_im

if __name__ == '__main__':
    figure = plt.figure()

    gray_im = cv.imread('CH10_Images/Fig1005(a)(wirebond_mask).tif', cv.IMREAD_GRAYSCALE)

    oplot = figure.add_subplot(221)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    lap_im = laplacian_filter(gray_im, figure.add_subplot(222))

    # abs_lap_im = np.abs(lap_im)
    negative_zero_im = lap_im.copy()
    negative_zero_im[negative_zero_im < 0] = 0

    absplot = figure.add_subplot(223)
    absplot.set_title('negative-zero-laplacian')
    absplot.set_xticks([])
    absplot.set_yticks([])
    absplot.imshow(negative_zero_im, cmap='gray')

    T = np.max(np.abs(lap_im)) - 1
    thresh_im = np.zeros_like(lap_im)
    thresh_im[lap_im > T] = 1

    posplot = figure.add_subplot(224)
    posplot.set_title('thresh-laplacian')
    posplot.set_xticks([])
    posplot.set_yticks([])
    posplot.imshow(thresh_im, cmap='gray')

    plt.show()
