#!/bin/env python
#
# 形态学平滑
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def morphology_smoothing(gray_im, se, plot: plt.Axes = None):
    '''形态学平滑: 先开运算再闭运算'''
    mopen_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, se)
    mclose_im = cv.morphologyEx(mopen_im, cv.MORPH_CLOSE, se)

    if plot is not None:
        plot.set_title('morphology smoothing')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(mclose_im, cmap='gray')
    return mclose_im


if __name__ == '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0938(a)(cygnusloop_Xray_original).tif', cv.IMREAD_GRAYSCALE)

    oplot = figure.add_subplot(221)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    # 半径为1的圆盘结构元，w=h=2*r+1 => 3
    se1 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
    morphology_smoothing(gray_im, se1, figure.add_subplot(222))

    # 半径为3的圆盘结构元，w=h=2*r+1 => 7
    se3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    morphology_smoothing(gray_im, se3, figure.add_subplot(223))

    # 半径为5的圆盘结构元，w=h=2*r+1 => 11
    se5 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11,11))
    morphology_smoothing(gray_im, se5, figure.add_subplot(224))

    plt.show()