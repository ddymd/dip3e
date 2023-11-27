#!/bin/env python
#
# 开闭运算
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def erode(bin_im, plot: plt.Axes):
    '''
    腐蚀
    '''
    # _, bin_im = cv2.threshold(im, 135, 255, cv2.THRESH_BINARY)
    erode_im = cv2.erode(bin_im, (3, 3))
    if plot is not None:
        plot.set_title("erode image")
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(erode_im, cmap='gray')
    return erode_im

def dilate(bin_im, plot: plt.Axes):
    '''
    膨胀
    '''
    dilate_im = cv2.dilate(bin_im, (3, 3))
    if plot is not None:
        plot.set_title("dilate image")
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(dilate_im, cmap='gray')
    return dilate_im

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread('CH09_Images/Fig0911(a)(noisy_fingerprint).tif')
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, bin_im = cv2.threshold(im, 135, 255, cv2.THRESH_BINARY)

    plot = figure.add_subplot(231)
    plot.set_title('origin gray')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    # 1 erode
    erode_im = erode(bin_im, None)
    erode_plot = figure.add_subplot(232)
    erode_plot.set_title('1-erode')
    erode_plot.set_xticks([])
    erode_plot.set_yticks([])
    erode_plot.imshow(erode_im, cmap='gray')

    # 2 erode+dilate
    dilate_im = dilate(erode_im, None)
    dilate_plot = figure.add_subplot(233)
    dilate_plot.set_title('2-erode&dilate(open)')
    dilate_plot.set_xticks([])
    dilate_plot.set_yticks([])
    dilate_plot.imshow(dilate_im, cmap='gray')

    # 3 open+dilate
    odilate_im = dilate(dilate_im, None)
    odilate_plot = figure.add_subplot(234)
    odilate_plot.set_title('3-open+dilate')
    odilate_plot.set_xticks([])
    odilate_plot.set_yticks([])
    odilate_plot.imshow(odilate_im, cmap='gray')

    # 4 open+dilate+erode (close)
    oclose_im = erode(odilate_im, None)
    oclose_plot = figure.add_subplot(235)
    oclose_plot.set_title('4-oclose')
    oclose_plot.set_xticks([])
    oclose_plot.set_yticks([])
    oclose_plot.imshow(oclose_im, cmap='gray')

    plt.show()
