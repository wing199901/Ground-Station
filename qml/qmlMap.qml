import QtQml 2.2
import QtQuick 2.4
import QtQuick.Controls 2.4
import QtQuick.Extras 1.4
import QtLocation 5.9
import QtPositioning 5.12

Item {
    width: 500
    height: 500

    Map {
        id: map
        objectName: "map"

        anchors.centerIn: parent
        anchors.fill: parent

        plugin: Plugin {
            name: "osm" // "mapboxgl", "esri", ...
        }

        center {
            latitude: 22.3035
            longitude: 114.2021
        }

        zoomLevel: 12
        maximumZoomLevel: 14
        minimumZoomLevel: 1
        copyrightsVisible: false

        //        Plane {
        //            id: qmlPlane1
        //            objectName: "qmlPlane1"

        //            coordinate: QtPositioning.coordinate(latitude, longitude)
        //        }
    }

    function addPlane(heading, latitude, longitude, name) {
        var component = Qt.createComponent("qrc:/qml/Plane.qml")
        //if (component.status === Component.Ready) {
        var plane = component.createObject(map, {
                                               "heading": heading,
                                               "latitude": latitude,
                                               "longitude": longitude,
                                               "pilotName": name
                                           })
        plane.objectName = name
        map.addMapItem(plane)
        //return plane
        //}
    }
}
