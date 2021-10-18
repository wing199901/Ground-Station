import QtQml 2.2
import QtQuick 2.12
import QtQuick.Window 2.2
import QtQuick.Controls 2.12
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls.Material 2.12
import QtQuick.Extras 1.4
import QtQuick.Layouts 1.0

import "../ECAMStyles"

Item {
    id: root
    visible: true
    width: 550
    height: 550

    Image {
        id: background
        source: "qrc:/image/ecam_background.svg"
        sourceSize.width: parent.width
        sourceSize.height: parent.height
    }

    Item {
        id: container
        width: root.width
        height: Math.min(root.width, root.height)
        anchors.centerIn: parent

        GridLayout {
            rows: 0
            columns: 3

            CircularGauge {
                id: throttleMeter
                width: height
                height: container.height * 0.25
                value: throttleLever
                property double throttleLever: 0

                style: QuadrantIndicatorStyle {
                    label: "Throttle"
                }
                objectName: "throttleMeter"
                maximumValue: 100
            }

            CircularGauge {
                id: propellerMeter
                width: height
                height: container.height * 0.25
                value: propellerLever
                style: QuadrantIndicatorStyle {
                    label: "Propeller"
                }
                objectName: "propellerMeter"
                property double propellerLever: 0

                maximumValue: 100
            }

            CircularGauge {
                id: mixtureMeter
                width: height
                height: container.height * 0.25
                value: mixtureLever
                style: QuadrantIndicatorStyle {
                    label: "Mixture"
                }
                property double mixtureLever: 0
                x: 260
                objectName: "mixtureMeter"
                maximumValue: 100
            }
        }

        ListView {
            id: warning
            x: 45
            y: 355
            width: 275
            height: 200
            anchors.bottom: parent.bottom
            antialiasing: true
            //            model: WarningModel {}
            model: LightSwitchModel {}
            delegate: Text {
                text: name
                color: __color
                font.bold: true
                font.family: "B612"
                font.pixelSize: 18
                height: __visible ? 22 : 0
                visible: __visible
            }
        }

        ListView {
            id: memo
            x: 364
            y: 350
            width: 190
            height: 200
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            antialiasing: true
            anchors.bottomMargin: 0
            model: MemoModel {}
            delegate: Text {
                text: name
                color: __color
                font.bold: true
                font.family: "B612"
                font.pixelSize: 18
                height: __visible ? 22 : 0
                visible: __visible
            }
        }

        Text {
            objectName: "fuelWeight"
            property int fuelWeight: 0
            x: 449
            y: 169
            height: 22
            color: Colors.green
            text: fuelWeight
            anchors.right: parent.right
            font.bold: true
            font.family: "B612"
            font.pixelSize: 18
            horizontalAlignment: Text.AlignRight
            anchors.rightMargin: 90
        }

        Text {
            objectName: "flaps"
            property int flaps: 0
            x: 414
            y: 280
            text: flaps
            color: Colors.green
            font.bold: true
            font.family: "B612"
            font.pixelSize: 26
            horizontalAlignment: Text.AlignHCenter
        }

        CircularGauge {
            id: elevatorTrimGauge
            objectName: "elevatorTrim"
            property double elevatorTrim: 0
            x: 379
            y: -7
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
    }

    function getMemoJsonKeys() {
        var array = new Array(0)
        for (var i = 0; i < memo.model.count; i++) {
            array.push(memo.model.get(i).josnKey)
        }

        return array
    }

    function setMemoVisible(index, visible) {
        if (memo.model.get(index).__visible !== visible) {
            memo.model.setProperty(index, "__visible", visible)
            memo.model.move(index, memo.model.count - 1, 1)
        }
    }

    function setMemoColor(index, color) {
        memo.model.setProperty(index, "__color", color)
    }

    function getWarningJsonKeys() {
        var array = new Array(0)
        for (var i = 0; i < warning.model.count; i++) {
            array.push(warning.model.get(i).josnKey)
        }

        return array
    }

    function setWarningVisible(index, visible) {
        if (warning.model.get(index).__visible !== visible) {
            warning.model.setProperty(index, "__visible", visible)
            warning.model.move(index, warning.model.count - 1, 1)
        }
    }
}
