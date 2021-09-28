#ifndef DEVICETAB_H
#define DEVICETAB_H

#include <QJsonObject>
#include <QQuickWidget>
#include <QWidget>

namespace Ui
{
class DeviceTab;
}

class DeviceTab : public QWidget
{
    Q_OBJECT

public:
    explicit DeviceTab(QWidget *parent = nullptr);
    ~DeviceTab();

public slots:
    void createPlaneSlot();
    void recieveJson(QJsonObject);

protected:
    void timerEvent(QTimerEvent *event);

private:
    Ui::DeviceTab *ui;
    int timerId;
    QJsonObject json;
    QQuickWidget *qmlMap;
    QObject *plane;
    QObject *planePoly;
};

#endif // DEVICETAB_H
