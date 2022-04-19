import QtQuick 2.12
import "../ECAMStyles"

ListModel {
    id: memoModel
    property bool completed: false
    Component.onCompleted: {
        append({
                   "name": "ALT",
                   "josnKey": "alternator",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "BAT",
                   "josnKey": "battery",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "AVIONICS",
                   "josnKey": "avionics",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "FUEL PUMP",
                   "josnKey": "fuelPump",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "PARK BRK",
                   "josnKey": "parkingBrake",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "PITOT HEAT",
                   "josnKey": "pitot",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "LDG",
                   "josnKey": "landingGear",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "STROBE LT",
                   "josnKey": "strobe",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        completed = true
    }

    //    ListElement {
    //        name: "ALT"
    //        __color: Colors.green
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "BAT"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "AVIONICS"
    //        __color: "red"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "FUEL PUMP"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "PARK BRK"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "PITOT HEAT"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "LDG LT"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
    //    ListElement {
    //        name: "STROBE LT OFF"
    //        __color: "#26ff00"
    //        __visible: true
    //    }
}
