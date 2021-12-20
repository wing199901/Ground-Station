QT       += core gui mqtt network svg quickwidgets positioning location location-private

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11 sdk_no_version_check

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    devicetab.cpp \
    main.cpp \
    mainwindow.cpp \
    summarytab.cpp

HEADERS += \
    devicetab.h \
    mainwindow.h \
    summarytab.h

FORMS += \
    devicetab.ui \
    mainwindow.ui \
    mainwindow_copy.ui \
    summarytab.ui

include(qfi/qfi.pri)

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

DISTFILES +=

RESOURCES += \
    qml.qrc
