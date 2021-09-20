#include "devicetab.h"

#include <QQuickItem>
#include <QThread>

#include "ui_devicetab.h"

class Sleeper : public QThread
{
public:
    static void usleep(unsigned long usecs) { QThread::usleep(usecs); }
    static void msleep(unsigned long msecs) { QThread::msleep(msecs); }
    static void sleep(unsigned long secs) { QThread::sleep(secs); }
};

DeviceTab::DeviceTab(QWidget *parent)
    : QWidget(parent), ui(new Ui::DeviceTab), timerId(0)
{
    ui->setupUi(this);
    timerId = startTimer(50);

    auto gauge = ui->qmlGauge;
    gauge->setAttribute(Qt::WA_AlwaysStackOnTop);
    gauge->setAttribute(Qt::WA_TranslucentBackground);
    gauge->setClearColor(Qt::transparent);
    gauge->setSource(QUrl("qrc:/qml/qmlGauge.qml"));
}

DeviceTab::~DeviceTab()
{
    killTimer(timerId);
    delete ui;
}

void DeviceTab::timerEvent(QTimerEvent *event)
{
    QWidget::timerEvent(event);
    ui->graphicsEADI->redraw();
}

void DeviceTab::recieveJson(QJsonObject m_Json)
{
    if (m_Json["name"] == objectName())
    {
        json = m_Json;
    }

    //EADI
    ui->graphicsEADI->setAirspeed(json["ias"].toDouble());
    ui->graphicsEADI->setAirspeedSel(json["airspeedSel"].toDouble());
    ui->graphicsEADI->setAltitude(json["altitude"].toDouble());
    ui->graphicsEADI->setAltitudeSel(json["altitudeSel"].toDouble());
    ui->graphicsEADI->setClimbRate(json["verticalSpeed"].toDouble() / 1000);
    ui->graphicsEADI->setHeading(json["heading"].toDouble());
    ui->graphicsEADI->setHeadingSel(json["headingSel"].toDouble());
    ui->graphicsEADI->setMachNo(json["mach"].toDouble());
    ui->graphicsEADI->setOverspeed(json["overspeed"].toBool() || json["ias"].toDouble() > 255);
    ui->graphicsEADI->setPause(json["pause"].toBool());
    ui->graphicsEADI->setPitch(json["pitch"].toDouble());
    ui->graphicsEADI->setPressure(json["pressure"].toDouble(), qfi_EADI::PressureMode::MB);
    ui->graphicsEADI->setRoll(json["roll"].toDouble());
    ui->graphicsEADI->setSlipSkid(json["slipskid"].toDouble());
    ui->graphicsEADI->setStall(json["stall"].toBool());
    ui->graphicsEADI->setTurnRate(json["turnRate"].toDouble() / 1024);

    //ECAM

    //Engine 1
    QJsonValue eng1Value = json.value("eng1");
    QJsonObject eng1 = eng1Value.toObject();

    QObject *throttleMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("throttleMeter");
    throttleMeter->setProperty("throttleLever", eng1["throttleLever"].toDouble());

    QObject *propellerMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("propellerMeter");
    propellerMeter->setProperty("propellerLever", eng1["propellerLever"].toDouble());

    QObject *mixtureMeter = ui->qmlGauge->rootObject()->findChild<QObject *>("mixtureMeter");
    mixtureMeter->setProperty("mixtureLever", eng1["mixtureLever"].toDouble());

    QObject *fuelWeight = ui->qmlGauge->rootObject()->findChild<QObject *>("fuelWeight");
    fuelWeight->setProperty("fuelWeight", json["fuelWeight"].toDouble());

    QObject *flaps = ui->qmlGauge->rootObject()->findChild<QObject *>("flaps");
    flaps->setProperty("flaps", json["flaps"].toDouble());

    QObject *elevatorTrim = ui->qmlGauge->rootObject()->findChild<QObject *>("elevatorTrim");
    elevatorTrim->setProperty("elevatorTrim", json["elevatorTrim"].toDouble());

    QVariant memoCount;

    QMetaObject::invokeMethod(
        ui->qmlGauge->rootObject(),
        "countMemo",
        Q_RETURN_ARG(QVariant, memoCount));

    for (int i = 0; i < memoCount.toInt(); i++)
    {
        QVariant key;
        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "getJsonKey",
            Q_RETURN_ARG(QVariant, key),
            Q_ARG(QVariant, QVariant::fromValue(i)));

        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "setVisible",
            Q_ARG(QVariant, QVariant::fromValue(i)),
            Q_ARG(QVariant, QVariant::fromValue(json[key.toString()].toBool())));
    }

    //Get UI->qmlMap
    QQuickWidget *qmlMap = QWidget::window()->findChild<QQuickWidget *>("qmlMap");

    //Get the plane from UI->qmlMap
    QObject *plane = qmlMap->rootObject()->findChild<QObject *>(json["name"].toString() + "Plane");

    if (plane)
    {
        plane->setProperty("heading", json["heading"].toDouble());
        plane->setProperty("latitude", json["latitude"].toDouble());
        plane->setProperty("longitude", json["longitude"].toDouble());
        plane->setProperty("pilotName", json["name"].toString());
    }

    Sleeper::sleep(1);
}
