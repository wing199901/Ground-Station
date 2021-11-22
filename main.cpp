#include <QApplication>
#include <QtNetwork>

#include "mainwindow.h"

int main(int argc, char *argv[])
{
    qDebug() << "OpenSSl Support:" << QSslSocket::supportsSsl();

    QApplication a(argc, argv);

    MainWindow w;

    // Set background color
    //    w.setStyleSheet("background-color:#5B686D;");
    w.show();
    return a.exec();
}
