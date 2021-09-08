import QtQuick 2.4
import QtLocation 5.6

MapQuickItem {
    //id: plane

    property double heading
    property double latitude
    property double longitude
    property string pilotName
    antialiasing: true

    anchorPoint.x: image.width / 2
    anchorPoint.y: image.height / 2

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
