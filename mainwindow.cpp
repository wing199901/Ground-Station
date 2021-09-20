#include "mainwindow.h"

#include <QGeoCoordinate>
#include <QQmlContext>
#include <QQuickItem>
#include <QQuickWidget>
#include <QtCore>
#include <QtNetwork>
#include <QtWidgets>

#include "devicetab.h"
#include "ui_mainwindow_copy.h"

//#include <QtMqtt/QMqttClient>

#include "qmqttclient.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) /*, timerId(0)*/
{
    ui->setupUi(this);
    ui->menubar->setNativeMenuBar(true);
    //    timerId = startTimer(50);

    //    auto gauge = ui->qmlGauge;
    //    gauge->setAttribute(Qt::WA_AlwaysStackOnTop);
    //    gauge->setAttribute(Qt::WA_TranslucentBackground);
    //    gauge->setClearColor(Qt::transparent);
    //    gauge->setSource(QUrl("qrc:/qml/qmlGauge.qml"));

    ui->qmlMap->setSource(QUrl("qrc:/qml/qmlMap.qml"));

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

                //ui->editLog->insertPlainText(content);
                //qDebug() << content;

                QJsonDocument doc = QJsonDocument::fromJson(message);
                QJsonObject json = doc.object();

                // Device name
                QString newDeviceName = topic.name().remove(0, 9);

                if (repeatedTopic(topic.name().remove(0, 9)) == false)
                {
                    //newTab
                    DeviceTab *newTab = new DeviceTab();
                    newTab->setObjectName(newDeviceName);

                    //Apple align center to newTab
                    QBoxLayout *newTabLayout = new QBoxLayout(QBoxLayout::LeftToRight, newTab);
                    newTabLayout->addWidget(newTab, Qt::AlignCenter);

                    //Add newTab to deviceYTabWidget
                    ui->deviceTabWidget->addTab(newTab, newDeviceName);

                    //Make connection between newTab and device json
                    connect(this, SIGNAL(sendJson(QJsonObject)), newTab, SLOT(recieveJson(QJsonObject)));

                    //Create plane
                    QVariant plane;
                    QMetaObject::invokeMethod(
                        ui->qmlMap->rootObject(),
                        "addPlane",
                        Q_RETURN_ARG(QVariant, plane),
                        Q_ARG(QVariant, QVariant::fromValue(json["heading"].toDouble())),
                        Q_ARG(QVariant, QVariant::fromValue(json["latitude"].toDouble())),
                        Q_ARG(QVariant, QVariant::fromValue(json["longitude"].toDouble())),
                        Q_ARG(QVariant, QVariant::fromValue(newDeviceName + "Plane")));
                }
                //Send json to newTab
                emitSendJson(json);
            });
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
    obj.insert("reset", QJsonValue::Type::Null);

    QJsonDocument doc(obj);
    QByteArray data = doc.toJson();

    m_client->publish(QMqttTopicName("/Sensors/ModelA/Command"), data, 2, false);
}

void MainWindow::on_actionReset_triggered()
{
    QJsonObject obj;
    obj.insert("pause", false);
    obj.insert("reset", true);

    QJsonDocument doc(obj);
    QByteArray data = doc.toJson();

    m_client->publish(QMqttTopicName("/Sensors/ModelA/Command"), data, 2, false);

    ui->actionPause->setChecked(false);
}

void MainWindow::on_actionTest_triggered()
{
    ui->deviceTabWidget->setTabText(0, "Testing");
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
