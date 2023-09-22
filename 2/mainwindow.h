#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QSerialPort>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QSerialPort *serialA;
    QSerialPort *serialB;
    // 转盘A目标位置
    uint8_t targetA {0};
    // 转盘B目标位置
    uint8_t targetB {0};
};
#endif // MAINWINDOW_H
