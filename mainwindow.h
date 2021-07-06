#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTcpSocket>
//#include <QtMqtt/QMqttClient>
#include "qmqttclient.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void updateMessage(const QMqttMessage &msg);

protected:
    void timerEvent(QTimerEvent *event);

private slots:
    void on_actionConnect_triggered();

private:
    Ui::MainWindow *ui;
    int timerId;
    QMqttClient *m_client;
    QMqttTopicFilter topic;
};
#endif // MAINWINDOW_H
