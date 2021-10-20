#include <QApplication>
#include <QtNetwork>

#include "mainwindow.h"

int main(int argc, char *argv[])
{
    qDebug() << "OpenSSl Support:" << QSslSocket::supportsSsl();

    QApplication a(argc, argv);
    MainWindow w;

    // Sets background color to
    w.setStyleSheet("background-color:#5B686D;");
    w.show();
    return a.exec();
}
