#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QJsonObject>
#include <QMainWindow>

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

    void emitSendJson(QJsonObject);

    //protected:
    //    void timerEvent(QTimerEvent *event);

private slots:
    void updateLogStateChange();
    void brokerDisconnected();

    void on_actionConnect_triggered();
    void on_actionSubscript_triggered();
    void on_actionPause_toggled(bool arg1);
    void on_actionReset_triggered();
    void on_actionTest_triggered();

    bool repeatedTopic(QString topic);

signals:
    void sendJson(QJsonObject);

private:
    Ui::MainWindow *ui;
    //    int timerId;
    QMqttClient *m_client;
    //    QMqttTopicFilter *topic;
    //    QString *newTabObjectName;
};
#endif // MAINWINDOW_H
