import QtQml 2.2
import QtQuick 2.12
import QtQuick.Window 2.2
import QtQuick.Controls 2.12
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls.Material 2.12
import QtQuick.Extras 1.4
import QtQuick.Layouts 1.0

import "../ECAMStyles"

CircularGauge {
    id: elevatorTrimGauge
    property double elevatorTrim: 0
    width: 152
    height: 152
    minimumValue: -100
    maximumValue: 100
    value: elevatorTrim

    style: CircularGaugeStyle {
        minimumValueAngle: 125
        maximumValueAngle: 55
        tickmarkStepSize: 100
        tickmark: Rectangle {
            implicitWidth: outerRadius * 0.07
            implicitHeight: outerRadius * 0.2
            color: "white"
            antialiasing: true
        }
        tickmarkLabel: null
        minorTickmark: Rectangle {
            implicitWidth: outerRadius * 0.03
            implicitHeight: outerRadius * 0.1
            color: "white"
            antialiasing: true
        }
        minorTickmarkCount: 1
        needle: Rectangle {
            y: outerRadius * 0.15
            implicitWidth: outerRadius * 0.05
            implicitHeight: outerRadius * 0.95
            antialiasing: true
            color: "#e5e5e5"
        }
    }

    Text {
        id: up
        x: 135
        y: 37
        text: "UP"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
    }

    Text {
        id: down
        x: 135
        y: 100
        text: "DN"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
    }

    Text {
        id: t
        x: 94
        y: 38
        text: "T"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }
    Text {
        id: r
        x: 94
        y: 49
        text: "R"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }
    Text {
        id: i
        x: 94
        y: 59
        width: 8
        height: 15
        text: "I"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }
    Text {
        id: m
        x: 93
        y: 70
        text: "M"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: upArrow
        x: 93
        y: 91
        text: "↑"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }

    Text {
        id: downArrow
        x: 93
        y: 100
        text: "↓"
        color: "white"
        font.bold: true
        font.family: "B612"
        font.pixelSize: 12
        horizontalAlignment: Text.AlignHCenter
    }
}
