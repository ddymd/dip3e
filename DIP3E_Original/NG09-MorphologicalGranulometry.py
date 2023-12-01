#!/bin/env python
#
# 形态学粒度测定
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def smoothing(gray_im, plot: plt.Axes = None):
    '''形态学平滑图像 - 先开运算再闭运算'''
    # 半径为5的圆盘结构元
    r = 5
    w = h = 2 * r + 1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (w,h))
    mo_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, se)
    mc_im = cv.morphologyEx(mo_im, cv.MORPH_CLOSE, se)

    if plot is not None:
        plot.set_title('morphological smoothing')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(mc_im, cmap='gray')

    return mc_im

if __name__ == '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0941(a)(wood_dowels).tif', cv.IMREAD_GRAYSCALE)

    init_sum = np.sum(np.asarray(gray_im))
    pixel_sum_list = [init_sum]

    show_id = 231
    plot = figure.add_subplot(show_id)
    show_id = show_id + 1
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap = 'gray')

    s_im = smoothing(gray_im, figure.add_subplot(show_id))
    show_id = show_id + 1

    show_list = [10, 20, 25, 30]
    for r in range(1, 36):
        w = h = 2 * r + 1
        se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (w,h))
        mo_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, se)
        pixel_sum_list.append(np.sum(np.asarray(mo_im)))
        if r in show_list:
            splot = figure.add_subplot(show_id)
            show_id = show_id + 1
            splot.set_title('morphological open-{}'.format(r))
            splot.set_xticks([])
            splot.set_yticks([])
            splot.imshow(mo_im, cmap = 'gray')

    opt_list = [init_sum]
    opt_list.extend(pixel_sum_list[:-1])
    diff_array = np.asarray(opt_list, dtype=np.int32)-np.asarray(pixel_sum_list, dtype=np.int32)
    print(diff_array)
    print(np.max(diff_array))
    print(pixel_sum_list)
    print(opt_list)
    plt.show()