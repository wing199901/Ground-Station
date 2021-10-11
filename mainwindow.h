#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QJsonObject>
#include <QMainWindow>
#include <QWidget>

//#include <QtMqtt/QMqttClient>
#include "qmqttclient.h"

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

signals:
    void sendJson(QJsonObject);
    void createPlaneSignal();
    void selectTab(QString);

private:
    Ui::MainWindow *ui;
    QMqttClient *m_client;

    QString getCurrentDeviceName();
    bool repeatedTopic(QString topic);

    void emitSendJson(QJsonObject);

private slots:
    void updateLogStateChange();
    void brokerDisconnected();

    void on_actionConnect_triggered();
    void on_actionSubscript_triggered();
    void on_actionPause_toggled(bool arg1);
    void on_actionReset_triggered();
    void on_deviceTabWidget_currentChanged(int index);
    void on_actionCenter_Map_by_Planes_triggered(bool checked);
};
#endif // MAINWINDOW_H
