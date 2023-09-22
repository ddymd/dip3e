#ifndef CCAMERA_H
#define CCAMERA_H

#include <QObject>

typedef void(* CameraDataCallBack)(ushort* imageData, ushort imageWidth, ushort imageHeight);

class CCamera : public QObject
{
    Q_OBJECT
public:
    //singleton
    static CCamera* Instance()
    {
        static CCamera camera;
        return &camera;
    }

    // fake code ,suppose to open the camera
    bool OpenCamera() { return true; }

    //fake code, suppose to capture camera image
    void StartCapture(CameraDataCallBack cb) { }

public:
    virtual ~CCamera() { }

private:
    // singleton mode, do not allow create instance outside class
    CCamera(QObject* parent = nullptr):QObject(parent){ }

private:

};

#endif // CCAMERA_H
