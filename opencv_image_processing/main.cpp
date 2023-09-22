#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

#include <iostream>

const int alpha_slider_max = 100;
int alpha_slider;
double alpha;
double beta;

cv::Mat src1;
cv::Mat src2;
cv::Mat dst;

// static void on_trackbar(int, void*) {
//     //cv::imshow("Linear Blend", dst);
// }

// int main() {
//     src1 = cv::imread("LinuxLogo.jpg");
//     src2 = cv::imread("WindowsLogo.jpg");

//     if (src1.empty()) {
//         std::cout << "Error loading src1\n";
//         return -1;
//     }

//     if (src2.empty()) {
//         std::cout << "Error loading src2\n";
//         return -2;
//     }

//     cv::namedWindow("Linear Blend", cv::WINDOW_AUTOSIZE);

//     char TrachbarName[50];
//     snprintf(TrachbarName, sizeof(TrachbarName), "Alpha x %d", alpha_slider_max);
//     cv::createTrackbar(TrachbarName, "Linear Blend", &alpha_slider, alpha_slider_max, on_trackbar);
//     on_trackbar(alpha_slider, 0);
//     cv::waitKey(0);
//     return 0;
// }

int main() {
    cv::Mat test(2, 2, CV_8UC3, cv::Scalar(0, 0, 255));
    std::cout << "M=" << std::endl << test << std::endl << std::endl;
    std::cout << "test step size: " << test.elemSize() << std::endl;

    cv::Mat a(1, 5, CV_32FC1);
    a.forEach<float>([](float& e, const int* pos) {
        std::cout << pos[0] << ", " << pos[1] << std::endl;
        e = pos[1];
    });
    auto b = a * 2;
    auto c = a + b;
    std::cout << "M=" << std::endl << a << std::endl << std::endl;
    std::cout << "M=" << std::endl << b << std::endl << std::endl;
    std::cout << "M=" << std::endl << c << std::endl << std::endl;

    std::cout << a.at<float>(0) << "," << a.at<float>(1) << std::endl;

    std::cout << "a elemSize size: " << a.elemSize() << std::endl;

    return 0;
}
