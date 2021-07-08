#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>

//#include <QtMqtt/QMqttClient>
#include "qmqttclient.h"
#include "mapdialog.h"

QT_BEGIN_NAMESPACE
namespace Ui
{
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

protected:
    void timerEvent(QTimerEvent *event);

private slots:
    void updateLogStateChange();
    void brokerDisconnected();

    void on_actionConnect_triggered();
    void on_actionSubscript_triggered();

    void on_pushButton_OpenMap_clicked();

private:
    Ui::MainWindow *ui;
    int timerId;
    QMqttClient *m_client;
    QMqttTopicFilter topic;

    MapDialog *mapDialog;
};
#endif // MAINWINDOW_H
