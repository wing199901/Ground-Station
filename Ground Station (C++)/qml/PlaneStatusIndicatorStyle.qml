import QtQuick 2.2
import QtQuick.Controls.Styles 1.4

StatusIndicatorStyle {
    property string label
    property bool rlyActive: false
    color: rlyActive ? "green" : "white"

    Text {
        color: "#ffffff"
        text: label
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.right
        font.pixelSize: 14
        font.family: "B612"
        anchors.leftMargin: 10
        antialiasing: true
    }
}
