import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Rectangle {
    id: root
    visible: true
    width: 500
    height: 500

    color: "black"

    Item {
        id: container
        width: root.width
        height: Math.min(root.width, root.height)
        anchors.centerIn: parent

        Grid {
            id: gaugeGrid
            columns: 0
            rows: 2
            spacing: container.width * 0.02

            CircularGauge {
                id: throttleMeter
                objectName: "throttleMeter"
                property double throttleLever
                value: throttleLever
                maximumValue: 100
                width: height
                height: container.height * 0.3

                style: DashboardGaugeStyle {
                    label: "Throttle"
                }
            }

            CircularGauge {
                id: propellerMeter
                objectName: "propellerMeter"
                property double propellerLever
                value: propellerLever
                maximumValue: 100
                width: height
                height: container.height * 0.3

                style: DashboardGaugeStyle {
                    label: "Propeller"
                }
            }

            CircularGauge {
                id: mixtureMeter
                objectName: "mixtureMeter"
                property double mixtureLever
                value: mixtureLever
                maximumValue: 100
                width: height
                height: container.height * 0.3

                style: DashboardGaugeStyle {
                    label: "Mixture"
                }
            }
        }
    }
}
