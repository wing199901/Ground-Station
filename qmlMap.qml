import QtQuick 2.0
import QtQuick.Window 2.0
import QtLocation 5.6
import QtPositioning 5.15


Item {
    id: qmlMap

    width: 500 ; height: 500

    Map {
        anchors.fill: parent
        //center: QtPositioning.coordinate(22.3035, 114.2021)
        center: QtPositioning.coordinate(longitude, latitude)
        zoomLevel: 12
        maximumZoomLevel: 14
        minimumZoomLevel: 1
        copyrightsVisible: false
        plugin: Plugin {
            name: "osm" // "mapboxgl", "esri", ...
        }
    }
}
