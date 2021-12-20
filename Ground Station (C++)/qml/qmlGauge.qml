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

            LeverGauge {
                id: throttleLeverGauge
                objectName: "throttleLeverGauge"
                label: "Throttle"
            }

            LeverGauge {
                id: propellerLeverGauge
                objectName: "propellerLeverGauge"
                label: "Propeller"
            }

            LeverGauge {
                id: mixtureLeverGauge
                objectName: "mixtureLeverGauge"
                label: "Mixture"
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
            id: fuelWeightText
            objectName: "fuelWeight" // @disable-check M16
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
            id: flapsText
            objectName: "flaps" // @disable-check M16
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

        ElevatorTrimGauge {
            id: elevatorTrimGauge
            objectName: "elevatorTrimGauge"

            x: 379
            y: -7
        }

        FuelSelectorGauge {
            id: fuelSelectorGauge
            objectName: "fuelSelectorGauge"

            x: 39
            y: 161
            width: 138
            height: 138
        }

        MagnetoGauge {
            id: magnetoGauge
            objectName: "magnetoGauge"

            x: 196
            y: 167
            width: 138
            height: 138
        }

        Joystick {
            id: joystick
            objectName: "joystick" // @disable-check M16

            x: 172
            y: 381
            width: 138
            height: 138
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

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/

