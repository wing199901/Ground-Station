#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QtCore>
//#include <QtMqtt/QMqttClient>
#include "qmqttclient.h"
#include <QtWidgets/QMessageBox>

#include <QThread>

class Sleeper : public QThread
{
public:
    static void usleep(unsigned long usecs){QThread::usleep(usecs);}
    static void msleep(unsigned long msecs){QThread::msleep(msecs);}
    static void sleep(unsigned long secs){QThread::sleep(secs);}
};

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , timerId(0)
{
    ui->setupUi(this);
    ui->menubar->setNativeMenuBar(true);
    timerId = startTimer(50);

    m_client = new QMqttClient(this);
    m_client->setHostname("aerosimmqtt.eastasia.azurecontainer.io");
    m_client->setPort(1883);

    connect(m_client, &QMqttClient::stateChanged, this, &MainWindow::updateLogStateChange);
    connect(m_client, &QMqttClient::disconnected, this, &MainWindow::brokerDisconnected);

    connect(m_client, &QMqttClient::messageReceived, this, [this](const QByteArray &message, const QMqttTopicName &topic) {
            const QString content = QDateTime::currentDateTime().toString()
                        + QLatin1String(" Received Topic: ")
                        + topic.name()
                        + QLatin1String(" Message: ")
                        + message
                        + QLatin1Char('\n');
            ui->editLog->insertPlainText(content);

            QJsonDocument doc = QJsonDocument::fromJson(message);
            QJsonObject jsonObj = doc.object();

            ui->graphicsEADI->setAirspeed(jsonObj["IAS"].toDouble());
            ui->graphicsEADI->setAltitude(jsonObj["Altitude"].toDouble());
            ui->graphicsEADI->setClimbRate(jsonObj["Vertical Speed"].toDouble() / 100);
            ui->graphicsEADI->setHeading(jsonObj["Heading"].toDouble());
            ui->graphicsEADI->setPitch(jsonObj["Pitch"].toDouble());
            ui->graphicsEADI->setRoll(jsonObj["Roll"].toDouble());
            ui->graphicsEADI->setTurnRate(jsonObj["Turn Rate"].toDouble());
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
    const QString content = QDateTime::currentDateTime().toString()
                    + QLatin1String(": State Change")
                    + QString::number(m_client->state())
                    + QLatin1Char('\n');
    ui->editLog->insertPlainText(content);
}

void MainWindow::brokerDisconnected()
{
    QApplication::quit();
}


void MainWindow::on_actionConnect_triggered()
{
    m_client->connectToHost();
}


void MainWindow::on_actionSubscript_triggered()
{
    auto subscription = m_client->subscribe(QMqttTopicFilter("/Sensor/ModelA"),0);
        if (!subscription) {
            QMessageBox::critical(this, QLatin1String("Error"), QLatin1String("Could not subscribe. Is there a valid connection?"));
            return;
        }
}

