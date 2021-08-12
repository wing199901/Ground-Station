import QtQuick 2.2
import QtQuick.Controls.Styles 1.4

CircularGaugeStyle {
    tickmarkInset: toPixels(0.04)
    minorTickmarkInset: tickmarkInset
    labelStepSize: 20
    labelInset: toPixels(0.23)

    maximumValueAngle: 70
    minimumValueAngle: -115

    property real xCenter: outerRadius
    property real yCenter: outerRadius
    property real needleLength: outerRadius - tickmarkInset * 1.5
    property real needleTipWidth: toPixels(0.04)
    property real needleBaseWidth: toPixels(0.04)
    property bool halfGauge: false
    property string label

    function toPixels(percentage) {
        return percentage * outerRadius
    }

    function degToRad(degrees) {
        return degrees * (Math.PI / 180)
    }

    function radToDeg(radians) {
        return radians * (180 / Math.PI)
    }

    function paintBackground(ctx) {
        if (halfGauge) {
            ctx.beginPath()
            ctx.rect(0, 0, ctx.canvas.width, ctx.canvas.height / 2)
            ctx.clip()
        }

        ctx.beginPath()
        ctx.fillStyle = "black"
        ctx.ellipse(0, 0, ctx.canvas.width, ctx.canvas.height)
        ctx.fill()

        ctx.beginPath()
        ctx.lineWidth = tickmarkInset
        ctx.strokeStyle = "white"
        ctx.arc(xCenter, yCenter, outerRadius - ctx.lineWidth / 2, degToRad(
                    valueToAngle(-5) - 90), degToRad(valueToAngle(105) - 90))
        ctx.stroke()
    }

    background: Canvas {
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            paintBackground(ctx)
        }

        Text {
            id: speedText
            font.family: "B612"
            font.pixelSize: toPixels(0.3)
            text: value + "%"
            color: "green"
            horizontalAlignment: Text.AlignRight
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.verticalCenter
            anchors.topMargin: toPixels(0.15)

            readonly property int value: control.value
        }
        Text {
            text: label
            color: "white"
            font.family: "B612"
            font.pixelSize: toPixels(0.15)
            anchors.top: speedText.bottom
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    tickmark: Rectangle {
        implicitWidth: outerRadius * 0.03
        implicitHeight: outerRadius * 0.1
        color: "white"
        antialiasing: true
    }

    minorTickmark: Rectangle {

        /*
        implicitWidth: outerRadius * 0.03
        implicitHeight: outerRadius * 0.1
        color: "white"
        antialiasing: true
        */
        visible: false
    }

    tickmarkLabel: Text {
        font.family: "B612"
        font.pixelSize: toPixels(0.25)
        text: styleData.value / 10
        color: "white"
        antialiasing: true
    }

    needle: Canvas {
        y: -outerRadius * 0.1
        implicitWidth: needleBaseWidth
        implicitHeight: needleLength
        antialiasing: true

        property real xCenter: width / 2
        property real yCenter: height / 2

        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()

            ctx.beginPath()
            ctx.moveTo(xCenter, height)
            ctx.lineTo(xCenter - needleBaseWidth / 2,
                       height - needleBaseWidth / 2)
            ctx.lineTo(xCenter - needleTipWidth / 2, 0)
            ctx.lineTo(xCenter, yCenter - needleLength)
            ctx.lineTo(xCenter, 0)
            ctx.closePath()
            ctx.fillStyle = Qt.rgba(0, 1, 0, 0.66)
            ctx.fill()

            ctx.beginPath()
            ctx.moveTo(xCenter, height)
            ctx.lineTo(width, height - needleBaseWidth / 2)
            ctx.lineTo(xCenter + needleTipWidth / 2, 0)
            ctx.lineTo(xCenter, 0)
            ctx.closePath()
            ctx.fillStyle = Qt.lighter(Qt.rgba(0, 1, 0, 0.66))
            ctx.fill()
        }
    }

    foreground: Item {}
}
