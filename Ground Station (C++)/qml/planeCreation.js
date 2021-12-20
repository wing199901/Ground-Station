function createPlaneObjects(map, heading, latitude, longitude, name) {
    var component = Qt.createComponent("../qml/Plane.qml")
    var sprite = component.createObject(map, {
                                            "heading": heading,
                                            "latitude": latitude,
                                            "longitude": longitude,
                                            "pilotName": name
                                        })

    if (sprite === null) {
        // Error Handling
        console.log("Error creating object")
    }
    return sprite
}
