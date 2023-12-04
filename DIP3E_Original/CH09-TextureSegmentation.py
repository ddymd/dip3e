#!/bin/env python
#
# 纹理分割
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

    gray_im = cv.imread('CH09_Images/Fig0943(a)(dark_blobs_on_light_background).tif', cv.IMREAD_GRAYSCALE)

    oplot = figure.add_subplot(221)
    oplot.set_title('origin')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(gray_im, cmap='gray')

    # 使用半径为30的结构元进行闭运算, 滤除比结构元尺寸小的黑斑点
    size = 2 * 30 + 1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (size,size))
    mc_im = cv.morphologyEx(gray_im, cv.MORPH_CLOSE, se)

    mcplot = figure.add_subplot(222)
    mcplot.set_title('morphological close@ellipse 30')
    mcplot.set_xticks([])
    mcplot.set_yticks([])
    mcplot.imshow(mc_im, cmap='gray')

    # 使用尺寸大于斑点间的距离结构元进行开运算, 删除斑点间的间隙
    size = 2 * 60 + 1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (size,size))
    mo_im = cv.morphologyEx(mc_im, cv.MORPH_OPEN, se)

    moplot = figure.add_subplot(223)
    moplot.set_title('morphological open@ellipse 60')
    moplot.set_xticks([])
    moplot.set_yticks([])
    moplot.imshow(mo_im, cmap='gray')

    # 形态学梯度, 获取边界
    se = np.ones((3,3))
    mg_im = morphology_gradient(mo_im, se)

    res_im = gray_im + mg_im
    res_im[res_im > 255] = 255

    mgplot = figure.add_subplot(224)
    mgplot.set_title('morphological gradient')
    mgplot.set_xticks([])
    mgplot.set_yticks([])
    mgplot.imshow(res_im, cmap='gray')

    plt.show()