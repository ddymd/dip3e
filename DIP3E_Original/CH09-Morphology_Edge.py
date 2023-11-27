#!/bin/env python
#
# 边界提取
#

import cv2
import numpy as np
import matplotlib.pylab as plt

def merode(bin_im, kernel: np.array):
    M, N = np.shape(bin_im)
    ext_pixel = kernel.shape[0] // 2
    ext_im = cv2.copyMakeBorder(bin_im, ext_pixel, ext_pixel, ext_pixel, ext_pixel, cv2.BORDER_REPLICATE)
    for m in range(ext_pixel, M):
        for n in range(ext_pixel, N):
            # TODO: complete the algorithm
            pass

def erode(bin_im, plot: plt.Axes):
    '''腐蚀'''
    erode_im = cv2.erode(bin_im, (3,3))
    if plot is not None:
        plot.set_title('erode image')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(erode_im, cmap='gray')
    return erode_im

def edge(bin_im, plot: plt.Axes):
    erode_im = erode(bin_im, None)
    edge_im = bin_im - erode_im
    if plot is not None:
        plot.set_title('edge image')
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(edge_im, cmap='gray')
    return edge_im

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread("CH09_Images/Fig0914(a)(licoln from penny).tif")
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    _, bin_im = cv2.threshold(gray_im, 128, 255, cv2.THRESH_BINARY)
    plot = figure.add_subplot(121)
    plot.set_title('origin')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(bin_im, cmap='gray')
    edge_im = edge(bin_im, figure.add_subplot(122))
    plt.show()
