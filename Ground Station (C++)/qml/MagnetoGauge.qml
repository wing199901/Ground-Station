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
    id: magnetoGauge
    property double magneto: 0
    width: height
    height: container.height * 0.25

    minimumValue: 0
    maximumValue: 4
    value: magneto

    style: CircularGaugeStyle {
        id: circularGaugeStyle
        minimumValueAngle: -60
        maximumValueAngle: 60
        labelStepSize: 1

        background: Image {
            source: "qrc:/image/magneto-markings.svg"
            antialiasing: true
        }

        needle: Rectangle {
            //y: outerRadius * 0.15
            implicitWidth: outerRadius * 0.05
            implicitHeight: outerRadius * 0.4
            antialiasing: true
            color: "white"
        }

        foreground: null
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

/*##^##
Designer {
    D{i:0;formeditorZoom:1.5;height:300;width:300}
}
##^##*/

