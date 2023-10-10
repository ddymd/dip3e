#!/usr/bin/env python
#
# 椒盐噪声 - 逆谐波滤波器滤除椒盐噪声
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def pepper_noise(im, p: float):
    rows, cols = im.shape[:2]
    ret = im.copy()
    # cv2.copyTo(im, ret)
    for u in range(rows):
        for v in range(cols):
            r = np.random.random()
            if r < p:
                ret[u,v] = 0
    return ret

def solt_noise(im, p: float):
    rows, cols = im.shape[:2]
    ret = im.copy()
    # ret = np.zeros_like(im)
    # cv2.copyTo(im, ret)
    for u in range(rows):
        for v in range(cols):
            r = np.random.random()
            if r < p:
                ret[u,v] = 255
    return ret

def contraharmonic_mean_filter(im, Q: float, kernel):
    """
    逆谐波均值滤波器
    """
    im[im==0] = 1
    numerator = np.power(im, Q+1)
    denominator = np.power(im, Q)
    k = np.ones(kernel)
    knumerator = cv2.filter2D(numerator, -1, k)
    kdenominator = cv2.filter2D(denominator, -1, k)
    kdenominator[kdenominator==0] = 1
    return knumerator / kdenominator

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('CH05_Images/Fig0507(a)(ckt-board-orig).tif')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    pim = pepper_noise(im, 0.1)
    sim = solt_noise(im, 0.1)

    ploto = figure.add_subplot(231)
    ploto.imshow(im, cmap='gray')
    ploto.set_title('origin')
    ploto.set_xticks([])
    ploto.set_yticks([])

    plotp = figure.add_subplot(232)
    plotp.imshow(pim, cmap='gray')
    plotp.set_title('pepper noise')
    plotp.set_xticks([])
    plotp.set_yticks([])


    plots = figure.add_subplot(233)
    plots.imshow(sim, cmap='gray')
    plots.set_title('solt noise')
    plots.set_xticks([])
    plots.set_yticks([])

    r1 = contraharmonic_mean_filter(pim, 1.5, (3,3))

    plotr1 = figure.add_subplot(235)
    plotr1.imshow(r1, cmap='gray')
    plotr1.set_title('filtering on pepper noise')
    plotr1.set_xticks([])
    plotr1.set_yticks([])

    r2 = contraharmonic_mean_filter(sim, -1.5, (3,3))

    plotr2 = figure.add_subplot(236)
    plotr2.imshow(r2, cmap='gray')
    plotr2.set_title('filtering on slot noise')
    plotr2.set_xticks([])
    plotr2.set_yticks([])

    figure.set_label('Contraharmonic mean spatial filtering')

    plt.show()
