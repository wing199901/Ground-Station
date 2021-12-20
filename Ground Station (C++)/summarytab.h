#ifndef SUMMARYTAB_H
#define SUMMARYTAB_H

#include <QWidget>

namespace Ui {
class SummaryTab;
}

class SummaryTab : public QWidget
{
    Q_OBJECT

public:
    explicit SummaryTab(QWidget *parent = nullptr);
    ~SummaryTab();

private:
    Ui::SummaryTab *ui;
};

#endif // SUMMARYTAB_H
