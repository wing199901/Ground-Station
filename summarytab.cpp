#include "summarytab.h"
#include "ui_summarytab.h"

SummaryTab::SummaryTab(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::SummaryTab)
{
    ui->setupUi(this);
}

SummaryTab::~SummaryTab()
{
    delete ui;
}
