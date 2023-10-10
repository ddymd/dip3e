#!/usr/bin/env python

# inverse filtering - 逆滤波

import cv2
import numpy as np
import matplotlib.pyplot as plt

def reverse_filter(M: np.int32, N: np.int32, k: np.float32, D: np.float32)->np.array:
    mask = np.zeros((M, N), dtype=np.float32)
    for u in range(M):
        for v in range(N):
            uu = np.abs(u-M/2)
            vv = np.abs(v-N/2)
            dist = np.sqrt(uu**2 + vv**2)
            if dist > D:
                mask[u, v] = 0
            else:
                mask[u, v] = np.e ** (-k * ((u+M/2)**2 + (v-N/2)**2)**(5/6))
    return mask

def reverse_filtering(im, mask: np.array):
    gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # fft
    fft = np.fft.fft2(gray_im)
    # shift
    fft_shift = np.fft.fftshift(fft)

    # apply mask
    processed = fft_shift * mask

    # ifft shift
    ifft_shift = np.fft.ifftshift(processed)
    # ifft
    ifft = np.fft.ifft2(ifft_shift)

    # back image
    return np.abs(ifft)

if __name__ == '__main__':
    im = cv2.imread('DIP3E_CH05_Original_Images/Fig0525(b)(aerial_view_turb_c_0pt0025).tif')
    M, N = im.shape[:2]
    # print(M, N)
    mask = reverse_filter(M, N, 0.0025, 500)

    processed_im = reverse_filtering(im, mask)
    plt.imshow(processed_im, cmap='gray')
    plt.show()
