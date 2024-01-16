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
    # 直方图
    hk = np.asarray(hist).ravel()
    # 概率密度
    pk = hk / hk.sum()
    # 累计概率密度
    ck = pk.cumsum()
    # 黄金比例点确定分割阈值
    xm = ck[ck <= 0.618].argmax()
    # print(xm)
    # 分割的子图像1
    x1 = x.copy()
    x1[x1 > xm] = 0
    # 分割的子图像2
    x2 = x.copy()
    x2[x2 <= xm] = 0

    # 曝光度E - 图像的曝光水平
    E = (pk * np.arange(256)).sum() / 256
    alpha = E if E <= 0.5 else 1 - E
    print('E={}, alpha={}'.format(E, alpha))

    # 对子图像进行自适应加权校正
    # h_max, h_min = np.max(hk), np.min(hk)
    # print('hk max={}, min={}'.format(h_max, h_min))

    x1_w1 = 1 - xm/L
    x1_w2 = 1
    x1_w3 = 1 + xm/L

    hk1 = np.asarray(cv.calcHist([x1], [0], None, [256], [0, 256])).ravel()
    h_max, h_min = np.max(hk1), np.min(hk1)
    x1_k = (hk1 - h_min) / (h_max-h_min)
    x1_hck = (h_max * np.float_power(x1_k, alpha * x1_w1) +
            h_max * np.float_power(x1_k, alpha * x1_w2) +
            h_max * np.float_power(x1_k, alpha * x1_w3)) / 3

    pc1_k = x1_hck / x1_hck.sum()
    cc1_k = pc1_k.cumsum()

    f1_k = xm * (cc1_k - 0.5 * pc1_k)

    # print('x1_k:\n{}'.format(x1_k))
    # print('pc1_k:\n{}'.format(pc1_k))
    # print('cc1_k:\n{}'.format(cc1_k))
    # print(f1_k)

    x2_w1 = 1 - (L-xm)/L
    x2_w2 = 1
    x2_w3 = 1 + (L-xm)/L

    hk2 = np.asarray(cv.calcHist([x2], [0], None, [256], [0, 256])).ravel()
    h_max, h_min = np.max(hk2), np.min(hk2)
    x2_k = (hk2 - h_min) / (h_max-h_min)
    x2_hck = (h_max * np.float_power(x2_k, alpha * x2_w1) +
            h_max * np.float_power(x2_k, alpha * x2_w2) +
            h_max * np.float_power(x2_k, alpha * x2_w3)) / 3

    pc2_k = x2_hck / x2_hck.sum()
    cc2_k = pc2_k.cumsum()

    f2_k = xm + 1 + (L - xm - 2)*(cc2_k - 0.5 * pc2_k)
    # print('x2_k:\n{}'.format(x2_k))
    # print('pc2_k:\n{}'.format(pc2_k))
    # print('cc2_k:\n{}'.format(cc2_k))
    # print(f2_k)

    res = im.copy()
    rows, cols = im.shape[:2]
    for r in range(rows):
        for c in range(cols):
            gv = x[r,c]
            if gv <= xm:
                res[r,c] = f1_k[gv]
            else:
                res[r,c] = f2_k[gv]


    x1plot = figure.add_subplot(223)
    x1plot.set_title('x1')
    x1plot.set_xticks([])
    x1plot.set_yticks([])
    x1plot.imshow(res, cmap='gray')

    # x2plot = figure.add_subplot(224)
    # x2plot.set_title('x2')
    # x2plot.set_xticks([])
    # x2plot.set_yticks([])
    # x2plot.imshow(f2_k, cmap='gray')

    plt.show()

if __name__ == '__main__':
    main()
