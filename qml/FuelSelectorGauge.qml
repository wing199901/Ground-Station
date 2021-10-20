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
    id: fuelSelectorGauge
    property double fuelSelector: 0
    width: height
    height: container.height * 0.25

    minimumValue: 0
    maximumValue: 3
    value: fuelSelector

    style: CircularGaugeStyle {
        id: circularGaugeStyle
        minimumValueAngle: -180
        maximumValueAngle: 90
        labelStepSize: 1

        background: Image {
            source: "qrc:/image/fuelselector-dial-bg.svg"
            antialiasing: true
        }

        needle: Image {
            height: outerRadius
            width: outerRadius
            y: outerRadius / 2
            source: "qrc:/image/fuelselector-needle.svg"
            antialiasing: true
            fillMode: Image.PreserveAspectFit
        }

        tickmark: null
        tickmarkLabel: null
        minorTickmark: null
    }

    Behavior on value {
        NumberAnimation {
            duration: 1000
        }
    }
}
