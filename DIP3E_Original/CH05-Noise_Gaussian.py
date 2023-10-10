#!/usr/bin/env python
#
# 高斯噪声
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

def gaussian_noise(im, mean: float, standard_deviation: float):
    '''
    m: mean
    v: variance
    '''
    gauss = np.random.normal(mean, standard_deviation, im.shape)
    return gauss + im

if __name__ == '__main__':
    figure = plt.figure()

    im = cv2.imread('CH05_Images/Fig0507(a)(ckt-board-orig).tif')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # 将图像添加均值为0, 方差为1000的高斯噪声
    gim = gaussian_noise(im, 0, np.sqrt(1000))

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
