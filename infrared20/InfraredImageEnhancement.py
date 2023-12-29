#!/bin/env python

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def main():
    figure = plt.figure()
    im = cv.imread('05.png', cv.IMREAD_GRAYSCALE)
    oplot = figure.add_subplot(221)
    oplot.set_title('Original')
    oplot.set_xticks([])
    oplot.set_yticks([])
    oplot.imshow(im, cmap='gray')

    x = np.asarray(im)

    min, max = np.min(im), np.max(im)
    hist = cv.calcHist([im], [0], None, [256], [0, 256])

    plot = figure.add_subplot(222)
    plot.set_title('Histogram')
    plot.set_xlabel('Bins')
    plot.set_ylabel('Number of Pixels')
    plot.set_xlim([min,max])
    plot.plot(hist)

    L = 256

    hk = np.asarray(hist).ravel()

    pk = hk / hk.sum()
    ck = pk.cumsum()

    xm = ck[ck <= 0.618].argmax()
    # print(xm)

    x1 = x.copy()
    x1[x1 > xm] = 0
    x2 = x.copy()
    x2[x2 <= xm] = 0

    # xx = x1 + x2

    # x1plot = figure.add_subplot(223)
    # x1plot.set_title('x1')
    # x1plot.set_xticks([])
    # x1plot.set_yticks([])
    # x1plot.imshow(x1, cmap='gray')

    # x2plot = figure.add_subplot(224)
    # x2plot.set_title('x2')
    # x2plot.set_xticks([])
    # x2plot.set_yticks([])
    # x2plot.imshow(x2, cmap='gray')

    E = (pk * np.arange(256)).sum() / 256
    alpha = E if E <= 0.5 else 1 - E

    print('E={}, alpha={}'.format(E, alpha))

    h_max, h_min = np.max(hk), np.min(hk)

    x1_w1 = 1 - xm/L
    x1_w2 = 1
    x1_w3 = 1 + xm/L

    x1_k = (hk[x1!=0] - h_min) / (h_max-h_min)
    x1_hck = (h_max * np.pow(x1_k, alpha * x1_w1) + h_max * np.pow(x1_k, alpha * x1_w2) + h_max * np.pow(x1_k, alpha * x1_w3)) / 3

    pc1_k = x1_hck / x1_hck.sum()
    cc1_k = pc1_k.cumsum()

    f1_k = xm * (cc1_k - 0.5 * pc1_k)

    x2_w1 = 1 - (L-xm)/L
    x2_w2 = 1
    x2_w3 = 1 + (L-xm)/L

    x2_k = (hk[x2!=0] - h_min) / (h_max-h_min)
    x2_hck = (h_max * np.pow(x2_k, alpha * x2_w1) + h_max * np.pow(x2_k, alpha * x2_w2) + h_max * np.pow(x2_k, alpha * x2_w3)) / 3

    pc2_k = x2_hck / x2_hck.sum()
    cc2_k = pc2_k.cumsum()

    f2_k = xm + 1 + (L - xm - 2)*(cc2_k - 0.5 * pc2_k)


    x1plot = figure.add_subplot(223)
    x1plot.set_title('x1')
    x1plot.set_xticks([])
    x1plot.set_yticks([])
    x1plot.imshow(f1_k, cmap='gray')

    x2plot = figure.add_subplot(224)
    x2plot.set_title('x2')
    x2plot.set_xticks([])
    x2plot.set_yticks([])
    x2plot.imshow(f2_k, cmap='gray')

    plt.show()

if __name__ == '__main__':
    main()
