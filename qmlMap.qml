import QtQuick 2.0
import QtQuick.Window 2.0
import QtLocation 5.6
import QtPositioning 5.15

Item {
    id: qmlMap

    width: 500 ; height: 500

    Plugin {
        id: mapPlugin
        name: "osm"
    }

    Map {
        anchors.fill: parent
        plugin: mapPlugin
        center: QtPositioning.coordinate(22.3035, 114.2021)
        //center: center
        zoomLevel: 12
        copyrightsVisible: false
    }
}
