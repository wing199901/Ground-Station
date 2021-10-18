import QtQuick 2.12
import QtLocation 5.12
import QtPositioning 5.12

MapPolyline {
    id: poly
    antialiasing: true
    line.width: 3
    line.color: Qt.rgba(Math.random(), Math.random(), Math.random(), 1)

    function addPolyPoint(latitude, longitude) {
        if (latitude !== 0 || longitude !== 0) {
            poly.addCoordinate(QtPositioning.coordinate(latitude, longitude))
        }
    }

    function removePoly() {
        var emptyLines = []
        poly.path = emptyLines
    }
}
