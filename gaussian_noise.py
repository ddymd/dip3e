#!/usr/bin/env python
#
# 高斯噪声
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def gaussian_noise(im, m: float, v: float):
    '''
    m: mean
    v: variance
    '''
    gauss = np.random.normal(m, v, im.shape)
    print(gauss)
    return gauss + im

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('DIP3E_CH05_Original_Images/Fig0507(a)(ckt-board-orig).tif')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    gim = gaussian_noise(im, 0, 100)

    ploto = figure.add_subplot(121)
    ploto.imshow(im, cmap='gray')
    ploto.set_title('origin')
    ploto.set_xticks([])
    ploto.set_yticks([])

    plotg = figure.add_subplot(122)
    plotg.imshow(gim, cmap='gray')
    plotg.set_title('gaussian noise')
    plotg.set_xticks([])
    plotg.set_yticks([])

    plt.show()
