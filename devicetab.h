#ifndef DEVICETAB_H
#define DEVICETAB_H

#include <QJsonObject>
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

protected:
    void timerEvent(QTimerEvent *event);

private:
    Ui::DeviceTab *ui;
    int timerId;
    QJsonObject json;

public slots:
    void recieveJson(QJsonObject);
};

#endif // DEVICETAB_H
