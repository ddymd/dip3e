#!/bin/env python
#
# 膨胀 dilate
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def dilate(im, plot: plt.Axes):
    _, bin_im = cv2.threshold(im, 135, 255, cv2.THRESH_BINARY)
    dilate_im = cv2.dilate(bin_im, (3, 3))
    if plot is not None:
        plot.set_title("dilate image")
        plot.set_xticks([])
        plot.set_yticks([])
        plot.imshow(dilate_im, cmap='gray')
    return dilate_im

if __name__ == '__main__':
    figure = plt.figure()
    im = cv2.imread('CH09_Images/Fig0907(a)(text_gaps_1_and_2_pixels).tif')
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    plot = figure.add_subplot(121)
    plot.set_title('origin gray')
    plot.set_xticks([])
    plot.set_yticks([])
    plot.imshow(gray_im, cmap='gray')

    dilate_im = dilate(gray_im, figure.add_subplot(122))
    plt.show()
