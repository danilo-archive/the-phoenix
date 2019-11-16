const express = require('express')
const fs = require('fs');
const app = express()
const port = 3000

app.get('/', (req, res) => res.sendFile(__dirname + '/public/index.html'))
app.use(express.static('public'))
app.listen(port, () => console.log(`Listening on :${port}!`))
var processedData;


const processCsvDataRail = function(data){

    var output = []
    var array  = data.split("\n");
    var a;
    array.forEach(element => {   

        a = element.split(',');
        let stationName1 = a[8].replace(/ /g, '').trim().toLowerCase()
        let crs8 = undefined;
        let tiploc8 = undefined;    
        for(var i = 0; i < codes.length; ++i){
            let station1 = codes[i]
            let str = station1.name
            stationName1 = stationName1.replace('station', '')


            if(stationName1.includes(str) || str.includes(stationName1)){
                crs8 = station1.crs ;
                tiploc8 = station1.tiploc ;
                break;
            }
        }  


         let stationName = a[9].replace(/ /g, '').trim().toLowerCase()
        let crs9 = undefined;
        let tiploc9 = undefined;    
        for(var i = 0; i < codes.length; ++i){
            let station = codes[i]
            let str = station.name

            stationName = stationName.replace('station', '')
            if(stationName.includes(str) || str.includes(stationName)){
                crs9 = station.crs ;
                tiploc9 = station.tiploc ;
                break;
            }
        }

                
   try{ 
       output.push(
        {
            date : a[0],
            incidentNumber : a[1],
            incidentReason : a[2],
            incidentReasonDescription: a[3],
            sectionName : a[4],
            operatorAffected: a[5],
            operatorNameAffected : a[6],
            trainIdAffected: a[7],
            plannedOriginName: a[8],
            plannedOriginCRS: crs8,
            plannedOriginTiploc: tiploc8,
            plannedDestinationName: a[9],
            plannedDestinationCRS: crs9,
            plannedDestinationTiploc: tiploc9,
            performanceEventCode : a[10],
            reactionaryCategoryCode : a[11],
            reactionaryCategoryDescription : a[12],
            startStanoxDescription: a[13],
            eventCount : a[13],
            PfPIMinutes: a[14]
        });
    }catch(error){
        console.error(error)
    }
    });
    //console.log(output)
        return output;
}

const getStationCRS = function(stationName){

}
const getStationTiploc = function(stationName){
    let str = stationName.replace(/ /g, '').trim().toLowerCase()
        codes.forEach((station)=>{
            let stationName = station.name.replace('station', '')
     
            
            if(stationName.includes(str) || str.includes(stationName)){
                return station.tiploc
            }
        })    
    }


const crsCode = function(c){
    try {
        return c.replace('\r', '')
      }
      catch(error) {
       return c
      }
      
}

let rawdata = fs.readFileSync('station_codes.json');
let codes = JSON.parse(rawdata);
var data = fs.readFileSync("server/15062019.csv", "utf8");

var processedData = processCsvDataRail(data)
var data1 = fs.readFileSync("server/05072019.csv", "utf8");
processedData.push(...processCsvDataRail(data1))
console.log(processedData)
fs.writeFile("values.json", JSON.stringify(processedData), "utf8", (err)=>console.error(err))


