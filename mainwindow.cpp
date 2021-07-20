#include "mainwindow.h"

#include <QQmlContext>
#include <QQuickWidget>
#include <QThread>
#include <QtCore>
#include <QtNetwork>
#include <QtWidgets>

#include "ui_mainwindow.h"

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

    ui->quickWidget->rootContext()->setContextProperty("longitude", 22.3035);
    ui->quickWidget->rootContext()->setContextProperty("latitude", 114.2021);
    ui->quickWidget->setSource(QUrl("qrc:/qmlMap.qml"));
    ui->quickWidget->setResizeMode(QQuickWidget::SizeRootObjectToView);

    m_client = new QMqttClient(this);
    //m_client->setHostname("aerosimmqtt.eastasia.azurecontainer.io");
    m_client->setHostname("192.168.0.129");
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

                QJsonDocument doc = QJsonDocument::fromJson(message);
                QJsonObject json = doc.object();

                ui->graphicsEADI->setAirspeed(json["IAS"].toDouble());
                ui->graphicsEADI->setAirspeedSel(json["AirspeedSel"].toDouble());
                ui->graphicsEADI->setAltitude(json["Altitude"].toDouble());
                ui->graphicsEADI->setAltitudeSel(json["AltitudeSel"].toDouble());
                ui->graphicsEADI->setClimbRate(json["Vertical Speed"].toDouble() / 1000);
                ui->graphicsEADI->setHeading(json["Heading"].toDouble());
                ui->graphicsEADI->setHeadingSel(json["HeadingSel"].toDouble());
                ui->graphicsEADI->setMachNo(json["Mach"].toDouble());
                ui->graphicsEADI->setPitch(json["Pitch"].toDouble());
                ui->graphicsEADI->setPressure(json["Pressure"].toDouble(), qfi_EADI::PressureMode::MB);
                ui->graphicsEADI->setRoll(json["Roll"].toDouble());
                ui->graphicsEADI->setSlipSkid(json["Slip Skid"].toDouble());
                ui->graphicsEADI->setStall(json["Stall"].toBool());
                ui->graphicsEADI->setTurnRate(json["Turn Rate"].toDouble() / 1024);
                ui->quickWidget->rootContext()->setContextProperty("longitude", json["Longitude"].toDouble());
                ui->quickWidget->rootContext()->setContextProperty("latitude", json["Latitude"].toDouble());

                qDebug() << json["AOA"].toDouble();
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
    auto subscription = m_client->subscribe(QMqttTopicFilter("/Sensor/ModelA"), 0);
    if (!subscription)
    {
        QMessageBox::critical(
            this, QLatin1String("Error"),
            QLatin1String("Could not subscribe. Is there a valid connection?"));
        return;
    }
}
