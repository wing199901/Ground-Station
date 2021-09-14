#include "devicetab.h"

#include "ui_devicetab.h"

DeviceTab::DeviceTab(QWidget *parent)
    : QWidget(parent), ui(new Ui::DeviceTab)
{
    ui->setupUi(this);

    auto gauge = ui->qmlGauge;
    gauge->setAttribute(Qt::WA_AlwaysStackOnTop);
    gauge->setAttribute(Qt::WA_TranslucentBackground);
    gauge->setClearColor(Qt::transparent);
    gauge->setSource(QUrl("qrc:/qml/qmlGauge.qml"));
}

DeviceTab::~DeviceTab()
{
    delete ui;
}
