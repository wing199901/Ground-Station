#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QtCore/QDateTime>
//#include <QtMqtt/QMqttClient>
#include "qmqttclient.h"
#include <QtWidgets/QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , timerId(0)
{
    ui->setupUi(this);
    ui->menubar->setNativeMenuBar(true);
    timerId = startTimer(0);

    m_client = new QMqttClient(this);
    m_client->setHostname("aerosimmqtt.eastasia.azurecontainer.io");
    m_client->setPort(1883);

}

MainWindow::~MainWindow()
{
    killTimer(timerId);
    delete ui;
    qApp->quit();
}

void MainWindow::timerEvent(QTimerEvent *event)
{
    QMainWindow::timerEvent(event);
    ui->graphicsEADI->redraw();
}

void MainWindow::updateMessage(const QMqttMessage &msg)
{
    ui->listWidget->addItem(msg.payload());
}

void MainWindow::on_actionConnect_triggered()
{
    qDebug() << "client is connected";
    topic.setFilter("/Sensor/ModelA");
    auto subscription = m_client->subscribe(topic, 0);
    qDebug() << subscription;

    connect(subscription, &QMqttSubscription::messageReceived, this, &MainWindow::updateMessage);
}

