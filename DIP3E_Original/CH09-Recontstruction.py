#!/bin/env python
#
# 重建开运算
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def grayscale_dilate_reconstruction(F, G, se, i: int = 0):
    '''膨胀形态学重建
    F: 标记图像
    G: 模板图像
    se: 膨胀结构元
    i: 迭代次数
    '''
    dilate_im = cv.dilate(F, se)
    arg_mask = dilate_im > G
    dilate_im[arg_mask] = G[arg_mask]
    i = i + 1
    if (F == dilate_im).all():
        return i, dilate_im
    return grayscale_dilate_reconstruction(dilate_im, G, se, i)

def opening_reconstruction(gray_im, se, plot: plt.Axes = None):
    '''重建开运算
    1. 腐蚀原图获取标记图像
    2. 原图作为模版图像
    3. 对标记图像进行膨胀和模版图像取小, 直到稳定
    '''
    # se = np.ones((1,71))
    F = cv.erode(gray_im, se)
    count, or_im = grayscale_dilate_reconstruction(F, gray_im, np.ones((3,3)))
    if plot is not None:
        plot.set_title('opening reconstruction: {}'.format(count))
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(or_im, cmap='gray')
    return or_im

if __name__ == "__main__":
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0944(a)(calculator).tif', cv.IMREAD_GRAYSCALE)

    # a
    oplot = figure.add_subplot(331)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')
    # b 重建开运算 
    or_im = opening_reconstruction(gray_im, np.ones((1,71)), figure.add_subplot(332))
    # c 开运算
    mo_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, np.ones((1,71)))
    moplot = figure.add_subplot(333)
    moplot.set_title('open')
    moplot.set_xticks([])
    moplot.set_yticks([])
    moplot.imshow(mo_im, cmap='gray')

    # d 重建顶帽运算 - 原图减去重建开运算
    th_im = gray_im - or_im
    thoplot = figure.add_subplot(334)
    thoplot.set_title('top hat reconstruction')
    thoplot.set_xticks([])
    thoplot.set_yticks([])
    thoplot.imshow(th_im, cmap='gray')

    # e 顶帽变换 - 原图减去标准开运算
    tht_im = gray_im - mo_im
    thtoplot = figure.add_subplot(335)
    thtoplot.set_title('top hat transformation')
    thtoplot.set_xticks([])
    thtoplot.set_yticks([])
    thtoplot.imshow(tht_im, cmap='gray')

    # f 去垂直反射
    orr_im = opening_reconstruction(th_im, np.ones((1,11)), figure.add_subplot(336))

    # g 膨胀
    md_im = cv.dilate(orr_im, np.ones((1, 21)))
    mdplot = figure.add_subplot(337)
    mdplot.set_title('dilate')
    mdplot.set_xticks([])
    mdplot.set_yticks([])
    mdplot.imshow(md_im, cmap='gray')

    # h 逐点最小
    arg_min = md_im > th_im
    min_im = md_im.copy()
    min_im[arg_min] = th_im[arg_min]
    mdplot = figure.add_subplot(338)
    mdplot.set_title('min')
    mdplot.set_xticks([])
    mdplot.set_yticks([])
    mdplot.imshow(min_im, cmap='gray')

    # TODO: the mask image is not matched with book!!!
    i, res_im = grayscale_dilate_reconstruction(min_im, th_im, np.ones((3,3)))
    resplot = figure.add_subplot(339)
    resplot.set_title('res: {}'.format(i))
    resplot.set_xticks([])
    resplot.set_yticks([])
    resplot.imshow(res_im, cmap='gray')

    plt.show()
