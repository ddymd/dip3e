#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ccamera.h"
#include <memory>
#include <thread>
#include <QQueue>
#include <QSemaphore>
#include <QString>
#include <QImage>

struct ImageData {
    std::shared_ptr<unsigned char> data;
    ushort width;
    ushort height;
};

// 缓存图像数据
QQueue<ImageData> g_imageDataQueue;
// 图像数据队列信号量
QSemaphore g_imageDataQueueSemaphore;
// 保存图像数据的线程
std::thread g_saveThread;
// 保存图像数据的索引
ushort g_imageIndex = 0;
// 最大保存图像数据的数量
#define MAX_IMAGE_TO_SAVE (5000)

void CameraImageReceived(ushort * imageData, ushort width, ushort height)
{
    if (g_imageIndex >= MAX_IMAGE_TO_SAVE) return;
    //todo: cache image data in memory, for example "a queue"
    // 缓存图像数据
    std::shared_ptr<unsigned char> pdata = std::make_shared<unsigned char>(width * height * sizeof(ushort));
    memcpy(pdata.get(), imageData, width * height * sizeof(ushort));
    g_imageDataQueue.enqueue({pdata, width, height});
    //todo: there should be another thread, which can get data from the memory and save the raw data in txt file.
    // 通知保存图像数据的线程
    g_imageDataQueueSemaphore.release();
    g_imageIndex++;
    //note: the main thread (ui thread) should not be blocked
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , m_run(true)
{
    ui->setupUi(this);

    connect(ui->pushButton_open_camera, &QPushButton::clicked, this, [=](){
        if(CCamera::Instance()->OpenCamera()) {
            CCamera::Instance()->StartCapture(CameraImageReceived);
        }
    });

    // 图像数据保存线程
    g_saveThread = std::thread([]{
        while(true) {
            g_imageDataQueueSemaphore.acquire();
            if (!m_run) {
                break;
            }
            ImageData data = g_imageDataQueue.dequeue();
            QImage image(data.data.get(), data.width, data.height, QImage::Format_Grayscale16);
            image.save(QString("image_%1.txt").arg(g_imageIndex));
        }
    });
}

MainWindow::~MainWindow()
{
    delete ui;
    // 等待结束图像数据保存线程
    m_run = false;
    g_imageDataQueueSemaphore.release();
    g_saveThread.join();
}

