#include <QApplication>
#include <QtNetwork>

#include "mainwindow.h"

int main(int argc, char *argv[])
{
    qDebug() << "OpenSSl Support:" << QSslSocket::supportsSsl();

    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
