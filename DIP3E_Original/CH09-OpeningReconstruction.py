#!/bin/env python
#
# 形态学重建 - 开运算
#

import cv2
import numpy as np
import matplotlib.pylab as plt

def reconstruction(bin_im, plot: plt.Axes = None):
    mark_kernel = np.ones((51,1))
    mark_im = cv2.erode(bin_im, mark_kernel)

    dilate_kernel = np.ones((3,3))

def reconstruction_open(bin_im, plot: plt.Axes = None):
    kernel = np.ones((51,1))
    open_im = cv2.morphologyEx(bin_im, cv2.MORPH_OPEN, kernel)
    if plot is not None:
        plot.set_title('open image')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(open_im, cmap='gray')
    return open_im

def reconstruction_mark(bin_im, plot: plt.Axes = None):
    '''图像中字母高度为51个像素, 使用(51,1)的结构元腐蚀原图, 对目标其进行标记'''
    kernel = np.ones((51,1))
    erode_im = cv2.erode(bin_im, kernel)
    if plot is not None:
        plot.set_title('mark image')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(erode_im, cmap='gray')
    return erode_im

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread("CH09_Images/Fig0931(a)(text_image).tif")
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, bin_im = cv2.threshold(gray_im, 128, 255, cv2.THRESH_BINARY)

    # show origin image
    plot = figure.add_subplot(221)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(bin_im, cmap='gray')

    mark_im = reconstruction_mark(bin_im, figure.add_subplot(222))
    open_im = reconstruction_open(bin_im, figure.add_subplot(223))

    plt.show()
