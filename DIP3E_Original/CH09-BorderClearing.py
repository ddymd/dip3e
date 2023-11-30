#!/bin/env python
#
# 心态学重建 - 边界清除
#

import cv2 as cv
import numpy as np
import matplotlib.pylab as plt

def dilate_reconstruction(G_arg, F, Se, i: int = 0):
    i = i + 1
    dilate_im = cv.dilate(F, Se)
    dilate_im[G_arg] = 0
    if (F == dilate_im).all():
        return i, F
    return dilate_reconstruction(G_arg, dilate_im, Se, i)

def border_clear(bin_im):
    '''
    边界填充 - 使用膨胀重建
    模版图像G: 原图I
    标记图像F: I(x,y) @ 图像边界
              0 @ 其他
    '''
    Se = np.ones((3,3))
    F = bin_im.copy()
    F[1:-2, 1:-2] = 0
    # 膨胀形态学重建
    i, x = dilate_reconstruction(bin_im==0, F, Se)

    return i, x, bin_im - x

if __name__ == '__main__':
    figure = plt.figure()
    im = cv.imread('CH09_Images/Fig0931(a)(text_image).tif')
    gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    _, bin_im = cv.threshold(gray_im, 127, 1, cv.THRESH_BINARY)

    plot = figure.add_subplot(131)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    loop_count, border_im, res_im = border_clear(bin_im)

    bplot = figure.add_subplot(132)
    bplot.set_title('border')
    bplot.set_xticks([])
    bplot.set_yticks([])
    bplot.imshow(border_im, cmap='gray')

    rplot = figure.add_subplot(133)
    rplot.set_title('result: {}'.format(loop_count))
    rplot.set_xticks([])
    rplot.set_yticks([])
    rplot.imshow(res_im, cmap='gray')

    plt.show()
