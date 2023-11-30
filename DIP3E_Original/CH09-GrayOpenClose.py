#!/bin/env python
#
# 灰度级形态学开闭运算
#

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def morphology_dilate(gray_im, plot: plt.Axes = None):
    # 高度为1，半径为2个像素的结构圆 - w=h=2*r+1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    md_im = cv.dilate(gray_im, se)
    if plot is not None:
        plot.set_title('morphology dilate')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(md_im, cmap='gray')

def morphology_erode(gray_im, plot: plt.Axes = None):
    # 高度为1，半径为2个像素的结构圆 - w=h=2*r+1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))
    me_im = cv.erode(gray_im, se)
    if plot is not None:
        plot.set_title('morphology erode')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(me_im, cmap='gray')

def morphology_open(gray_im, plot: plt.Axes = None):
    # 高度为1，半径为3个像素的结构圆 - w=h=2*r+1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    # print('open se: {}'.format(se))
    mo_im = cv.morphologyEx(gray_im, cv.MORPH_OPEN, se)
    if plot is not None:
        plot.set_title('morphology open')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(mo_im, cmap='gray')

def morphology_close(gray_im, plot: plt.Axes = None):
    # 高度为1，半径为5个像素的结构圆 - w=h=2*r+1
    se = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11,11))
    # print('close se: {}'.format(se))
    mc_im = cv.morphologyEx(gray_im, cv.MORPH_CLOSE, se)
    if plot is not None:
        plot.set_title('morphology close')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(mc_im, cmap='gray')

if __name__ == '__main__':
    figure = plt.figure()
    gray_im = cv.imread('CH09_Images/Fig0935(a)(ckt_board_section).tif', cv.IMREAD_GRAYSCALE)

    plot = figure.add_subplot(231)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    morphology_erode(gray_im, figure.add_subplot(232))
    morphology_dilate(gray_im, figure.add_subplot(233))

    morphology_open(gray_im, figure.add_subplot(235))
    morphology_close(gray_im, figure.add_subplot(236))

    plt.show()
