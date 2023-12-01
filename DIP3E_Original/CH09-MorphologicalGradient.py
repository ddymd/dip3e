#!/bin/env python
#
# 形态学梯度
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def morphology_gradient(gray_im, se, figure: plt.Figure = None):
    '''形态学梯度: 膨胀图像减去腐蚀图像'''
    md_im = cv.dilate(gray_im, se)
    me_im = cv.erode(gray_im, se)
    gradient_im = md_im - me_im

    if figure is not None:
        dplot = figure.add_subplot(222)
        dplot.set_title('dilate')
        dplot.set_xticks([])
        dplot.set_yticks([])
        dplot.imshow(md_im, cmap='gray')

        eplot = figure.add_subplot(223)
        eplot.set_title('erode')
        eplot.set_xticks([])
        eplot.set_yticks([])
        eplot.imshow(me_im, cmap='gray')

        gplot = figure.add_subplot(224)
        gplot.set_title('gradient')
        gplot.set_xticks([])
        gplot.set_yticks([])
        gplot.imshow(gradient_im, cmap='gray')

    return gradient_im

if __name__ == '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0939(a)(headCT-Vandy).tif', cv.IMREAD_GRAYSCALE)

    plot = figure.add_subplot(221)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    morphology_gradient(gray_im, np.ones((3,3)), figure)

    plt.show()