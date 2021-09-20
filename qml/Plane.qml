import QtQuick 2.4
import QtLocation 5.12
import QtPositioning 5.12

MapQuickItem {
    property double heading: 0
    property double latitude: 0
    property double longitude: 0
    property string pilotName: ""
    antialiasing: true

    anchorPoint.x: image.width / 2
    anchorPoint.y: image.height / 2

    coordinate: QtPositioning.coordinate(latitude, longitude)

    sourceItem: Grid {
        columns: 1
        Grid {
            horizontalItemAlignment: Grid.AlignHCenter
            Image {
                id: image
                rotation: heading
                source: "/image/airplane.png"
            }
            Rectangle {
                //id: bubble
                color: "lightblue"
                border.width: 1
                width: name.width * 1.3
                height: name.height * 1.3
                radius: 5
                Text {
                    id: name
                    anchors.centerIn: parent
                    text: pilotName
                }
            }
        }
    }
}
