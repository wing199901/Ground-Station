#ifndef MAINWINDOW_H
#define MAINWINDOW_H

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

protected:
    void timerEvent(QTimerEvent *event);

private slots:
    void updateLogStateChange();
    void brokerDisconnected();

    void on_actionConnect_triggered();
    void on_actionSubscript_triggered();
    void on_actionPause_toggled(bool arg1);
    void on_actionReset_triggered();

private:
    Ui::MainWindow *ui;
    int timerId;
    QMqttClient *m_client;
    QMqttTopicFilter topic;
};
#endif // MAINWINDOW_H
