#!/bin/env python
#
# 形态学 顶帽变换和底帽变换
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def tophat_transformation(gray_im, se, plot: plt.Axes = None):
    '''顶帽变换
    使用较大的结构元对图像进行开运算, 以得到图像的背景
    原图减去背景, 以均匀化图像光照亮度
    '''
    mopen_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, se)
    if plot is not None:
        plot.set_title('morphology open')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(mopen_im, cmap='gray')

    tophat_im = gray_im - mopen_im

    return tophat_im


if __name__ == '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0940(a)(rice_image_with_intensity_gradient).tif', cv.IMREAD_GRAYSCALE)

    plot = figure.add_subplot(231)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    _, bin_im = cv.threshold(gray_im, -1, 1, cv.THRESH_OTSU)

    bplot = figure.add_subplot(232)
    bplot.set_title('otsu bin')
    bplot.set_xticks([])
    bplot.set_yticks([])
    bplot.imshow(bin_im, cmap='gray')

    # 半径为40的圆盘形结构元 w=h=2*r+1 = 81
    r = 40
    w = h = 2 * r + 1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (w,h))
    tophat_im = tophat_transformation(gray_im, se, figure.add_subplot(233))

    tpplot = figure.add_subplot(234)
    tpplot.set_title('tophat')
    tpplot.set_xticks([])
    tpplot.set_yticks([])
    tpplot.imshow(tophat_im, cmap='gray')

    _, th_bin_im = cv.threshold(tophat_im, -1, 1, cv.THRESH_OTSU)

    tpbplot = figure.add_subplot(235)
    tpbplot.set_title('tophat otsu bin')
    tpbplot.set_xticks([])
    tpbplot.set_yticks([])
    tpbplot.imshow(th_bin_im, cmap='gray')

    tophat_cv = cv.morphologyEx(gray_im, cv.MORPH_TOPHAT, se)
    cvplot = figure.add_subplot(236)
    cvplot.set_title('tophat-cv')
    cvplot.set_xticks([])
    cvplot.set_yticks([])
    cvplot.imshow(tophat_cv, cmap='gray')

    plt.show()
