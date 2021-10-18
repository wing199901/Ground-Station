#include "devicetab.h"

#include <QQuickItem>
#include <QThread>

#include "ui_devicetab.h"

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

void DeviceTab::createPlaneSlot()
{
    // Get qmlMap
    qmlMap = QWidget::window()->findChild<QQuickWidget *>("qmlMap");

    plane = qmlMap->rootObject()->findChild<QObject *>(objectName() + "Plane");

    if (!plane)
    {
        // Create plane to qmlMap
        QMetaObject::invokeMethod(
            qmlMap->rootObject(),
            "addPlane",
            Q_ARG(QVariant, QVariant::fromValue(objectName() + "Plane")));

        // Get plane from qmlMap
        plane = qmlMap->rootObject()->findChild<QObject *>(objectName() + "Plane");

        // Create plane poly to qmlMap
        QMetaObject::invokeMethod(
            qmlMap->rootObject(),
            "addPoly",
            Q_ARG(QVariant, QVariant::fromValue(objectName() + "Poly")));

        // Get poly form qmlMap
        planePoly = qmlMap->rootObject()->findChild<QObject *>(objectName() + "Poly");
    }
}

void DeviceTab::recieveJson(QJsonObject m_Json)
{
    if (m_Json["name"] == objectName())
    {
        json = m_Json;
    }

    // EADI
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

    // ECAM

    // Engine 1
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

    // MEMO
    QVariant memoKeys;
    QMetaObject::invokeMethod(
        ui->qmlGauge->rootObject(),
        "getMemoJsonKeys",
        Q_RETURN_ARG(QVariant, memoKeys));

    //    qDebug() << keys.toList();

    for (int i = 0; i < memoKeys.toList().count(); i++)
    {
        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "getMemoJsonKeys",
            Q_RETURN_ARG(QVariant, memoKeys));

        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "setMemoVisible",
            Q_ARG(QVariant, QVariant::fromValue(i)),
            Q_ARG(QVariant, QVariant::fromValue(json[memoKeys.toList()[i].toString()].toBool())));
    }

    // Lights
    QJsonValue lightsValue = json.value("lights");
    QJsonObject lights = lightsValue.toObject();

    QVariant lightKeys;
    QMetaObject::invokeMethod(
        ui->qmlGauge->rootObject(),
        "getWarningJsonKeys",
        Q_RETURN_ARG(QVariant, lightKeys));

    qDebug() << lightKeys.toList();

    for (int i = 0; i < lightKeys.toList().count(); i++)
    {
        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "getWarningJsonKeys",
            Q_RETURN_ARG(QVariant, lightKeys));

        QMetaObject::invokeMethod(
            ui->qmlGauge->rootObject(),
            "setWarningVisible",
            Q_ARG(QVariant, QVariant::fromValue(i)),
            Q_ARG(QVariant, QVariant::fromValue(lights[lightKeys.toList()[i].toString()].toBool())));
    }

    // Plane
    plane->setProperty("heading", json["heading"].toDouble());
    plane->setProperty("latitude", json["latitude"].toDouble());
    plane->setProperty("longitude", json["longitude"].toDouble());

    // Plane poly
    QMetaObject::invokeMethod(
        planePoly,
        "addPolyPoint",
        Q_ARG(QVariant, QVariant::fromValue(json["latitude"].toDouble())),
        Q_ARG(QVariant, QVariant::fromValue(json["longitude"].toDouble())));

    if (json["reset"].toBool())
    {
        QMetaObject::invokeMethod(
            planePoly,
            "removePoly");
    }
}

void DeviceTab::tabSelected(QString tabName)
{
    // self equals tab current widget
    if (this->objectName() == tabName)
    {
        QMetaObject::invokeMethod(
            qmlMap->rootObject(),
            "startTrackPlane",
            Q_ARG(QVariant, QVariant::fromValue(plane)));
    }
}

bool DeviceTab::isPaused()
{
    return json["pause"].toBool();
}
