#!/bin/env python
#
# 形态学重建 - 重建开运算(Opening by Reconstruction)
#

import cv2
import numpy as np
import matplotlib.pylab as plt

def obrc(bin_im, zero_arg, i: int = 0):
    '''重建开运算 Opening By Reconstruction'''
    dilate_kernel = np.ones((3,3))
    dilate_im = cv2.dilate(bin_im, dilate_kernel)
    dilate_im[zero_arg] = 0
    i = i + 1
    if (bin_im == dilate_im).all():
        return i, dilate_im
    return obrc(dilate_im, zero_arg, i)

def reconstruction(bin_im, plot: plt.Axes = None):
    # 获取锚点
    mark_kernel = np.ones((51,1))
    mark_im = cv2.erode(bin_im, mark_kernel)
    # 重建开运算
    loop_count, recons_im = obrc(mark_im, bin_im == 0)

    if plot is not None:
        plot.set_title('reconstruction: {}'.format(loop_count))
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(recons_im, cmap='gray')
    return recons_im

def reconstruction_open(bin_im, plot: plt.Axes = None):
    '''开运算: 先腐蚀再膨胀'''
    kernel = np.ones((51,1))
    open_im = cv2.morphologyEx(bin_im, cv2.MORPH_OPEN, kernel)
    if plot is not None:
        plot.set_title('mark by open(erode+dilate)')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(open_im, cmap='gray')
    return open_im

def reconstruction_mark(bin_im, plot: plt.Axes = None):
    '''图像中字母高度为51个像素, 使用(51,1)的结构元腐蚀原图, 对目标其进行标记'''
    kernel = np.ones((51,1))
    erode_im = cv2.erode(bin_im, kernel)
    if plot is not None:
        plot.set_title('mark by erode')
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

    reconstruction(bin_im, figure.add_subplot(224))

    plt.show()
