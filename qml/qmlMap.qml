import QtQml 2.2
import QtQuick 2.4
import QtQuick.Controls 2.4
import QtQuick.Extras 1.4
import QtLocation 5.12
import QtPositioning 5.12

Item {
    width: 500
    height: 500

    Timer {
        id: mapCenterRefreshTimer
        running: false
        interval: 500
        repeat: true
        onTriggered: {
            map.fitViewportToMapItems()
        }
    }

    Timer {
        id: trackPlaneRefreshTimer
        running: false
        interval: 500
        repeat: true
        property var plane
        onTriggered: {
            //            map.fitViewportToMapItems()
            map.center = plane.coordinate
        }
    }

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

        //gesture.enabled: true
        //gesture.acceptedGestures: MapGestureArea.PanGesture


        MouseArea {
            anchors.fill: parent

            property int lastX: -1
            property int lastY: -1

            onPressed: {
                lastX = mouse.x
                lastY = mouse.y
            }

            onPositionChanged: {
                map.pan(lastX - mouse.x, lastY - mouse.y)
                lastX = mouse.x
                lastY = mouse.y

                mapCenterRefreshTimer.stop()
                trackPlaneRefreshTimer.stop()
            }
        }


        Component.onCompleted: {
            console.log("Dimensions: ", width, height)
        }
    }





    function addPlane(name) {
        var component = Qt.createComponent("qrc:/qml/Plane.qml")
        var plane = component.createObject(map, {
                                               "pilotName": name.replace(
                                                                "Plane", "")
                                           })
        plane.objectName = name
        map.addMapItem(plane)
    }

    function addPoly(name) {
        var component = Qt.createComponent("qrc:/qml/PlanePoly.qml")
        var poly = component.createObject(map)
        poly.objectName = name
        map.addMapItem(poly)
    }

    function startTimer() {
        mapCenterRefreshTimer.start()
    }

    function stopTimer() {
        mapCenterRefreshTimer.stop()
    }

    function startTrackPlane(plane) {
        trackPlaneRefreshTimer.plane = plane
        trackPlaneRefreshTimer.start()
    }

    function stopTrackPlane() {
        trackPlaneRefreshTimer.stop()
    }
}
