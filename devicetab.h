#ifndef DEVICETAB_H
#define DEVICETAB_H

#include <QWidget>

namespace Ui {
class DeviceTab;
}

class DeviceTab : public QWidget
{
    Q_OBJECT

public:
    explicit DeviceTab(QWidget *parent = nullptr);
    ~DeviceTab();

private:
    Ui::DeviceTab *ui;
};

#endif // DEVICETAB_H
