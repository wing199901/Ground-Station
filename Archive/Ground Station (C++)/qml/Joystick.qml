import QtQuick 2.12

Item {
    id: joystick
    width: background.width
    height: background.height

    Image {
        id: background

        property real angle: 0
        property real distance: 0

        source: "qrc:/image/background.png"
        anchors.centerIn: parent

        ParallelAnimation {
            id: returnAnimation
            NumberAnimation {
                target: thumb.anchors
                property: "horizontalCenterOffset"
                to: 0
                duration: 200
                easing.type: Easing.OutSine
            }
            NumberAnimation {
                target: thumb.anchors
                property: "verticalCenterOffset"
                to: 0
                duration: 200
                easing.type: Easing.OutSine
            }
        }

        Image {
            id: thumb
            source: "qrc:/image/finger.png"
            anchors.centerIn: parent
        }
    }

    function joystickOnAction(x, y) {
        thumb.anchors.horizontalCenterOffset = x / 16384 * joystick.width / 2
        thumb.anchors.verticalCenterOffset = y / 16384 * joystick.height / 2
    }
}
