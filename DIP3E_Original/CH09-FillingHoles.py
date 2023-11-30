#!/bin/env python
#
# 形态学重建 - 孔洞填充
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def dreconstruction(G_arg, F, Se, i: int = 0):
    '''
    膨胀形态学重建
    G: 模版图像
    F: 标记图像
    SE: 结构元
    '''
    i = i + 1
    dilate_im = cv.dilate(F, Se)
    dilate_im[G_arg] = 0
    if (F == dilate_im).all():
        return i, 1-F
    return dreconstruction(G_arg, dilate_im, Se, i)


def fill_holes(bin_im, plot: plt.Axes = None):
    '''
    孔洞填充
    模版图像: 原图I的补集Ic
    标记图像: 1-I(x,y) @图像边界
            0 @ 其他
    '''
    # 标记图像
    F = 1 - bin_im
    F[1:-2,1:-2] = 0
    # 模版图像
    Ic = 1 - bin_im
    # 结构元
    Se = np.ones((3,3))
    i, fill_im = dreconstruction(Ic==0, F, Se)

    if plot is not None:
        plot.set_title('Filling holes: {}'.format(i))
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(fill_im, cmap='gray')
    return F, Ic, fill_im

if __name__ == '__main__':
    figure = plt.figure()

    im = cv.imread('CH09_Images/Fig0931(a)(text_image).tif')
    gray_im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
    _, bin_im = cv.threshold(gray_im, 127, 1, cv.THRESH_BINARY)

    plot = figure.add_subplot(221)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(bin_im, cmap='gray')

    F, G, _ = fill_holes(bin_im, figure.add_subplot(224))

    # 展示模版图像
    gplot = figure.add_subplot(222)
    gplot.set_title('G')
    gplot.set_xticks([])
    gplot.set_yticks([])
    gplot.imshow(G, cmap='gray')
    # 展示标记图像
    fplot = figure.add_subplot(223)
    fplot.set_title('F')
    fplot.set_xticks([])
    fplot.set_yticks([])
    fplot.imshow(F, cmap='gray')

    plt.show()
