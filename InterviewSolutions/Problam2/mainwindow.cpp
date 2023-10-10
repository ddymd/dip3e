#include "mainwindow.h"
#include "./ui_mainwindow.h"

#include <QSerialPort>
#include <QDebug>
#include <QString>

#define CMD_SIZE 10

// 查询转盘位置指令
uint8_t acquire_location[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x84, 0x10, 0x03, 0x01, 0x00, 0x00, 0x9E};
// 转动指令：1号位
uint8_t rotate1[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x83, 0x10, 0x03, 0x01, 0x00, 0x01, 0x9E};
// 转动指令：2号位
uint8_t rotate2[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x83, 0x10, 0x03, 0x01, 0x00, 0x02, 0x9F};
// 转动指令：3号位
uint8_t rotate3[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x83, 0x10, 0x03, 0x01, 0x00, 0x03, 0xA0};
// 转动指令：4号位
uint8_t rotate4[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x83, 0x10, 0x03, 0x01, 0x00, 0x04, 0xA1};
// 转动指令：5号位
uint8_t rotate5[CMD_SIZE] = {0x5A, 0xA5, 0x06, 0x83, 0x10, 0x03, 0x01, 0x00, 0x05, 0xA2};
// 查询转盘位置回复指令的前缀
QString acquire_result_prefix("5AA506834F4B");

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // 创建两个新的串口对象
    serialA = new QSerialPort(this);
    serialB = new QSerialPort(this);

    // 连接串口A接收数据的信号
    connect(serialA, &QSerialPort::readyRead, this, [=]{
        // 这里假设串口数据读取都是正常的，一次能读取完整的指令
        QByteArray data = serialA->readAll();
        if (targetA == 0) {
            ui->statusRotate->setText(tr("转盘A没有目标位置"));
            return;
        }
        QString strData = data.toHex();
        ui->statusRotate->setText("串口A数据："+strData);

        QString tgtData = acquire_result_prefix;
        char* rotate_cmd;
        switch (targetA) {
        case 1:
            // 转盘目标1号位
            tgtData += "01";
            // 将位置1设置为B转盘转动指令和目标位置
            rotate_cmd = (char*)rotate1;
            targetB = 1;
            break;
        case 2:
            // 转盘目标2号位
            tgtData += "02";
            // 将位置2设置为B转盘转动指令和目标位置
            rotate_cmd = (char*)rotate2;
            targetB = 2;
            break;
        case 3:
            // 转盘目标3号位
            tgtData += "03";
            // 将位置3设置为B转盘转动指令和目标位置
            rotate_cmd = (char*)rotate3;
            targetB = 3;
            break;
        case 4:
            // 转盘目标4号位
            tgtData += "04";
            // 将位置4设置为B转盘转动指令和目标位置
            rotate_cmd = (char*)rotate4;
            targetB = 4;
            break;
        case 5:
            // 转盘目标5号位
            tgtData += "05";
            // 将位置5设置为B转盘转动指令和目标位置
            rotate_cmd = (char*)rotate5;
            targetB = 5;
            break;
        default:
            break;
        }
        if (strData == tgtData) {
            // 转盘A到达目标位置，启动转盘B
            serialB->write(rotate_cmd, CMD_SIZE);
            // 开始查询转盘B位置
            serialB->write((const char*)acquire_location, CMD_SIZE);
        } else {
            // 转盘A未到目标位置，继续查询转盘A位置
            serialA->write((const char*)acquire_location, CMD_SIZE);
        }
    });

    // 连接串口B接收数据的信号
    connect(serialB, &QSerialPort::readyRead, this, [=]{
        // 这里假设串口数据读取都是正常的，一次能读取完整的指令
        QByteArray data = serialB->readAll();
        if (targetB == 0) {
            ui->statusRotate->setText(tr("转盘B 没有目标位置"));
            return;
        }
        ui->statusRotate->clear();
        QString strData = data.toHex();
        ui->statusRotate->setText("串口A数据："+strData);
        QString tgtData = acquire_result_prefix;
        char* rotate_cmd;
        switch (targetB) {
        case 1:
            // B转盘目标1号位
            tgtData += "01";
            // 将位置2设置为A转盘转动指令和目标位置
            rotate_cmd = (char*)rotate2;
            targetA = 2;
            break;
        case 2:
            // B转盘目标2号位
            tgtData += "02";
            // 将位置3设置为A转盘转动指令和目标位置
            rotate_cmd = (char*)rotate3;
            targetA = 3;
            break;
        case 3:
            // B转盘目标3号位
            tgtData += "03";
            // 将位置4设置为A转盘转动指令和目标位置
            rotate_cmd = (char*)rotate4;
            targetA = 4;
            break;
        case 4:
            // B转盘目标4号位
            tgtData += "04";
            // 将位置5设置为A转盘转动指令和目标位置
            rotate_cmd = (char*)rotate5;
            targetA = 5;
            break;
        case 5:
            // B转盘目标5号位
            tgtData += "05";
            // 将位置1设置为A转盘转动指令和目标位置
            rotate_cmd = (char*)rotate1;
            targetA = 1;
            // 如果转盘B到5号位就停止，则设置targetA和targetB的目标位置为0，然后这里直接return即可
            break;
        default:
            break;
        }
        if (strData == tgtData) {
            // 转盘B到达目标位置，启动转盘A
            serialA->write(rotate_cmd, CMD_SIZE);
        } else {
            // 转盘B未到目标位置，继续查询转盘B位置
            serialB->write((const char*)acquire_location, CMD_SIZE);
        }
    });
    // 串口A打开按钮
    connect(ui->openButtonA, &QPushButton::clicked, this, [=]{
        ui->statusLabelA->setText(tr("无法打开串口A"));
        // 设置串口A参数
        serialA->setPortName(ui->portComboBoxA->currentText());
        serialA->setBaudRate(ui->baudComboBoxA->currentText().toInt());
        serialA->setDataBits(QSerialPort::Data8);
        serialA->setParity(QSerialPort::NoParity);
        serialA->setStopBits(QSerialPort::OneStop);

        // 打开串口A
        if (serialA->open(QIODevice::ReadWrite)) {
            ui->statusLabelA->setText(tr("串口A已打开"));
            ui->openButtonA->setEnabled(false);
            ui->closeButtonA->setEnabled(true);
        } else {
            ui->statusLabelA->setText(tr("无法打开串口A"));
        }
    });
    // 串口A关闭按钮
    connect(ui->closeButtonA, &QPushButton::clicked, this, [=]{
        // 关闭串口A
        serialA->close();
        ui->statusLabelA->setText(tr("串口A已关闭"));

        ui->openButtonA->setEnabled(true);
        ui->closeButtonA->setEnabled(false);
    });

    // 串口B打开按钮
    connect(ui->openButtonB, &QPushButton::clicked, this, [=]{
        ui->statusLabelB->setText(tr("正在打开串口B"));
        // 设置串口B参数
        serialB->setPortName(ui->portComboBoxB->currentText());
        serialB->setBaudRate(ui->baudComboBoxB->currentText().toInt());
        serialB->setDataBits(QSerialPort::Data8);
        serialB->setParity(QSerialPort::NoParity);
        serialB->setStopBits(QSerialPort::OneStop);

        // 打开串口B
        if (serialB->open(QIODevice::ReadWrite)) {
            ui->statusLabelB->setText(tr("串口B已打开"));
            ui->openButtonB->setEnabled(false);
            ui->closeButtonB->setEnabled(true);
        } else {
            ui->statusLabelB->setText(tr("无法打开串口B"));
        }
    });
    // 串口B关闭按钮
    connect(ui->closeButtonB, &QPushButton::clicked, this, [=]{
        // 关闭串口B
        serialB->close();
        ui->statusLabelB->setText(tr("串口B已关闭"));

        ui->openButtonB->setEnabled(true);
        ui->closeButtonB->setEnabled(false);
    });

    // 开始转动按钮
    connect(ui->rotateStartButton, &QPushButton::clicked, this, [=]{
        if (serialA->isOpen() && serialB->isOpen()) {
            // 转盘A启动，目标1号位
            serialA->write((const char*)rotate1, CMD_SIZE);
            // 设置转盘A目标1号位
            targetA = 1;
            // 开始查询转盘A位置
            serialA->write((const char*)acquire_location, CMD_SIZE);
            ui->rotateStartButton->setEnabled(false);
        } else {
            ui->statusRotate->setText(tr("串口未全部打开，启动转动失败"));
        }
    });

    // 停止转动按钮
    connect(ui->rotateStopButton, &QPushButton::clicked, this, [=]{
        targetA = 0;
        targetB = 0;
        ui->rotateStartButton->setEnabled(true);
    });
}

MainWindow::~MainWindow()
{
    delete ui;
}
