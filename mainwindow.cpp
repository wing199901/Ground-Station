#include "mainwindow.h"

#include <QGeoCoordinate>
#include <QMessageBox>
#include <QQmlContext>
#include <QQuickItem>
#include <QQuickWidget>
#include <QWidget>
#include <QtCore>
#include <QtNetwork>

#include "devicetab.h"
#include "ui_mainwindow_copy.h"

//#include <QtMqtt/QMqttClient>

#include "qmqttclient.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    ui->menubar->setNativeMenuBar(true);

    ui->qmlMap->setSource(QUrl("qrc:/qml/qmlMap.qml"));
    ui->qmlMap->setObjectName("qmlMap");

    m_client = new QMqttClient(this);
    //    m_client->setHostname("aerosimmqtt.eastasia.azurecontainer.io");
    m_client->setHostname("192.168.0.128");
    m_client->setPort(1883);

    connect(m_client, &QMqttClient::stateChanged, this,
            &MainWindow::updateLogStateChange);

    connect(m_client, &QMqttClient::disconnected, this,
            &MainWindow::brokerDisconnected);

    connect(m_client, &QMqttClient::messageReceived, this, [this](const QByteArray &message, const QMqttTopicName &topic)
            {
                const QString content = QDateTime::currentDateTime().toString() +
                                        QLatin1String(" Received Topic: ") +
                                        topic.name() + QLatin1String(" Message: ") +
                                        message + QLatin1Char('\n');

                // ui->editLog->insertPlainText(content);
                // qDebug() << content;

                QJsonDocument doc = QJsonDocument::fromJson(message);
                QJsonObject json = doc.object();

                // Device name
                QString newDeviceName = topic.name().remove(0, 9);

                if (repeatedTopic(newDeviceName) == false)
                {
                    // newTab
                    DeviceTab *newTab = new DeviceTab();
                    newTab->setObjectName(newDeviceName);

                    // Apple align center to newTab
                    QBoxLayout *newTabLayout = new QBoxLayout(QBoxLayout::LeftToRight, newTab);
                    newTabLayout->addWidget(newTab, Qt::AlignCenter);

                    // Add newTab to deviceYTabWidget
                    ui->deviceTabWidget->insertTab(ui->deviceTabWidget->currentIndex() + 1, newTab, newDeviceName);

                    ui->deviceTabWidget->setCurrentIndex(ui->deviceTabWidget->indexOf(newTab));

                    // Connection between newTab and device json
                    connect(this, SIGNAL(sendJson(QJsonObject)), newTab, SLOT(recieveJson(QJsonObject)));

                    // Create plane connection
                    connect(this, SIGNAL(createPlaneSignal()), newTab, SLOT(createPlaneSlot()));

                    // Create Plane
                    emit createPlaneSignal();

                    connect(this, SIGNAL(selectTab(QString)), newTab, SLOT(tabSelected(QString)));
                }
                // Send json to newTab
                emitSendJson(json); });
}

MainWindow::~MainWindow()
{
    delete ui;
    qApp->quit();
}

void MainWindow::updateLogStateChange()
{
    const QString content = QDateTime::currentDateTime().toString() +
                            QLatin1String(": State Change") +
                            QString::number(m_client->state()) +
                            QLatin1Char('\n');
    qDebug() << content;
}

void MainWindow::brokerDisconnected()
{
    QMessageBox::critical(
        this, QLatin1String("Error"),
        QLatin1String("Broker disconnected."));
    QApplication::quit();
}

void MainWindow::on_actionConnect_triggered()
{
    m_client->connectToHost();
}

void MainWindow::on_actionSubscript_triggered()
{
    auto subscription = m_client->subscribe(QMqttTopicFilter("/Devices/+"), 0);
    if (!subscription)
    {
        QMessageBox::critical(
            this, QLatin1String("Error"),
            QLatin1String("Could not subscribe. Is there a valid connection?"));
        return;
    }
}

void MainWindow::on_actionPause_toggled(bool arg1)
{
    QJsonObject obj;
    obj.insert("pause", arg1);
    obj.insert("reset", false);

    QJsonDocument doc(obj);
    QByteArray data = doc.toJson();

    m_client->publish(QMqttTopicName("/Devices/" + getCurrentDeviceName() + "/Command"), data, 2, false);
}

void MainWindow::on_actionReset_triggered()
{
    ui->actionPause->setChecked(false);

    QJsonObject obj;
    obj.insert("pause", false);
    obj.insert("reset", true);

    QJsonDocument doc(obj);
    QByteArray data = doc.toJson();

    m_client->publish(QMqttTopicName("/Devices/" + getCurrentDeviceName() + "/Command"), data, 2, false);
}

bool MainWindow::repeatedTopic(QString topic)
{
    for (int i = 0; i < ui->deviceTabWidget->count(); i++)
    {
        if (ui->deviceTabWidget->tabText(i) == topic)
            return true;
    }
    return false;
}

void MainWindow::emitSendJson(QJsonObject m_Json)
{
    emit sendJson(m_Json);
}

QString MainWindow::getCurrentDeviceName()
{
    return ui->deviceTabWidget->currentWidget()->objectName();
}

// Send the current widget object name
void MainWindow::on_deviceTabWidget_currentChanged(int index)
{
    emit selectTab(ui->deviceTabWidget->widget(index)->objectName());

    // Disable Map center
    QMetaObject::invokeMethod(
        ui->qmlMap->rootObject(),
        "stopTimer");
}

void MainWindow::on_actionCenter_Map_by_Planes_triggered()
{
    QMetaObject::invokeMethod(
        ui->qmlMap->rootObject(),
        "startTimer");
}
