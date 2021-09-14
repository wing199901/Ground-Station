#include "mainwindow.h"

#include <QGeoCoordinate>
#include <QQmlContext>
#include <QQuickItem>
#include <QQuickWidget>
#include <QThread>
#include <QtCore>
#include <QtNetwork>
#include <QtWidgets>

#include "devicetab.h"
#include "ui_mainwindow_copy.h"

//#include <QtMqtt/QMqttClient>

#include "qmqttclient.h"

class Sleeper : public QThread
{
public:
    static void usleep(unsigned long usecs) { QThread::usleep(usecs); }
    static void msleep(unsigned long msecs) { QThread::msleep(msecs); }
    static void sleep(unsigned long secs) { QThread::sleep(secs); }
};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow), timerId(0)
{
    ui->setupUi(this);
    ui->menubar->setNativeMenuBar(true);
    timerId = startTimer(50);

    auto gauge = ui->qmlGauge;
    gauge->setAttribute(Qt::WA_AlwaysStackOnTop);
    gauge->setAttribute(Qt::WA_TranslucentBackground);
    gauge->setClearColor(Qt::transparent);
    gauge->setSource(QUrl("qrc:/qml/qmlGauge.qml"));

    ui->qmlMap->setSource(QUrl("qrc:/qml/qmlMap.qml"));

    m_client = new QMqttClient(this);
    //m_client->setHostname("aerosimmqtt.eastasia.azurecontainer.io");
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
                qDebug() << content;

                QJsonDocument doc = QJsonDocument::fromJson(message);
                QJsonObject json = doc.object();

                DeviceTab *newTab = new DeviceTab(this);
                QBoxLayout *newTabLayout = new QBoxLayout(QBoxLayout::LeftToRight, newTab);
                newTabLayout->addWidget(newTab, Qt::AlignCenter);
                newTab->setObjectName(topic.name().remove(0, 9));

                // Add tab
                if (repeatedTopic(topic.name().remove(0, 9)) == false)
                {
                    ui->deviceTabWidget->addTab(newTab, topic.name().remove(0, 9));
                }

                //                //Engine 1
                //                QJsonValue eng1Value = json.value("eng1");
                //                QJsonObject eng1 = eng1Value.toObject();

                //                ui->graphicsEADI->setAirspeed(json["ias"].toDouble());
                //                ui->graphicsEADI->setAirspeedSel(json["airspeedSel"].toDouble());
                //                ui->graphicsEADI->setAltitude(json["altitude"].toDouble());
                //                ui->graphicsEADI->setAltitudeSel(json["altitudeSel"].toDouble());
                //                ui->graphicsEADI->setClimbRate(json["verticalSpeed"].toDouble() / 1000);
                //                ui->graphicsEADI->setHeading(json["heading"].toDouble());
                //                ui->graphicsEADI->setHeadingSel(json["headingSel"].toDouble());
                //                ui->graphicsEADI->setMachNo(json["mach"].toDouble());
                //                ui->graphicsEADI->setOverspeed(json["overspeed"].toBool() || json["ias"].toDouble() > 255);
                //                ui->graphicsEADI->setPause(json["pause"].toBool());
                //                ui->graphicsEADI->setPitch(json["pitch"].toDouble());
                //                ui->graphicsEADI->setPressure(json["pressure"].toDouble(), qfi_EADI::PressureMode::MB);
                //                ui->graphicsEADI->setRoll(json["roll"].toDouble());
                //                ui->graphicsEADI->setSlipSkid(json["slipskid"].toDouble());
                //                ui->graphicsEADI->setStall(json["stall"].toBool());
                //                ui->graphicsEADI->setTurnRate(json["turnRate"].toDouble() / 1024);

                //                QObject *plane = ui->qmlMap->rootObject()->findChild<QObject *>("qmlPlane1");
                //                if (plane)
                //                {
                //                    plane->setProperty("heading", json["heading"].toDouble());
                //                    plane->setProperty("latitude", json["latitude"].toDouble());
                //                    plane->setProperty("longitude", json["longitude"].toDouble());
                //                    plane->setProperty("pilotName", json["name"].toString());
                //                }

                //                QObject *throttleMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("throttleMeter");
                //                if (throttleMeter)
                //                {
                //                    throttleMeter->setProperty("throttleLever", eng1["throttleLever"].toDouble());
                //                }

                //                QObject *propellerMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("propellerMeter");
                //                if (propellerMeter)
                //                {
                //                    propellerMeter->setProperty("propellerLever", eng1["propellerLever"].toDouble());
                //                }

                //                QObject *mixtureMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("mixtureMeter");
                //                if (mixtureMeter)
                //                {
                //                    mixtureMeter->setProperty("mixtureLever", eng1["mixtureLever"].toDouble());
                //                }

                //                QObject *fuelWeight = ui->qmlGauge->rootObject()->findChild<QObject *>("fuelWeight");
                //                fuelWeight->setProperty("fuelWeight", json["fuelWeight"].toDouble());

                //                QObject *flaps = ui->qmlGauge->rootObject()->findChild<QObject *>("flaps");
                //                flaps->setProperty("flaps", json["flaps"].toDouble());

                //                QObject *elevatorTrim = ui->qmlGauge->rootObject()->findChild<QObject *>("elevatorTrim");
                //                elevatorTrim->setProperty("elevatorTrim", json["elevatorTrim"].toDouble());

                //                QVariant memoCount;
                //                QMetaObject::invokeMethod(
                //                    ui->qmlGauge->rootObject(),
                //                    "countMemo",
                //                    Q_RETURN_ARG(QVariant, memoCount));

                //                for (int i = 0; i < memoCount.toInt(); i++)
                //                {
                //                    QVariant key;
                //                    QMetaObject::invokeMethod(
                //                        ui->qmlGauge->rootObject(),
                //                        "getJsonKey",
                //                        Q_RETURN_ARG(QVariant, key),
                //                        Q_ARG(QVariant, QVariant::fromValue(i)));

                //                    QMetaObject::invokeMethod(
                //                        ui->qmlGauge->rootObject(),
                //                        "setVisible",
                //                        Q_ARG(QVariant, QVariant::fromValue(i)),
                //                        Q_ARG(QVariant, QVariant::fromValue(json[key.toString()].toBool())));
                //                }
            });

    Sleeper::sleep(1);
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

void MainWindow::updateLogStateChange()
{
    const QString content = QDateTime::currentDateTime().toString() +
                            QLatin1String(": State Change") +
                            QString::number(m_client->state()) +
                            QLatin1Char('\n');
    //ui->editLog->insertPlainText(content);
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
