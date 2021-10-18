import QtQuick 2.12
import "../ECAMStyles"

ListModel {
    id: lightSwitchModel
    property bool completed: false
    Component.onCompleted: {
        append({
                   "name": "NAV",
                   "josnKey": "navigation",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "BEACON",
                   "josnKey": "beacon",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "LAND",
                   "josnKey": "landing",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "TAXI",
                   "josnKey": "taxi",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "STROBE",
                   "josnKey": "strobes",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "INT",
                   "josnKey": "instruments",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "LDG",
                   "josnKey": "recognition",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "WING",
                   "josnKey": "wing",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "LOGO",
                   "josnKey": "logo",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        append({
                   "name": "CABIN",
                   "josnKey": "cabin",
                   "__color": String(Colors.green),
                   "__visible": false
               })
        completed = true
    }
}
