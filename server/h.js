const fs = require('fs')
let datapack =     JSON.parse(fs.readFileSync('datapack.json'));
let stationCodes = JSON.parse(fs.readFileSync('station_codes.json'));
let incidentData = JSON.parse(fs.readFileSync('incident_data.json'));







let newData = [];

for (let i = 0; i < datapack.length; i++) {
    const element = datapack[i];
    for (let j = 0; j < incidentData.length; j++) {
        const incidentRow = incidentData[j];
        const trainId = incidentRow.trainIdAffected.substring(2,6)

        if(element.train_id == trainId){
            element.incident = incidentRow;            
            break;
        }
    }
    newData.push(element)
}

fs.writeFileSync("new__datapack.json",JSON.stringify(newData), "utf-8")