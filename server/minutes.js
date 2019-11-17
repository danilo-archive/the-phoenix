const fs = require('fs')
let datapack =     JSON.parse(fs.readFileSync('beauty.json'));

let newData = []
const f = datapack[1]
var incidentStartTime =Date.parse(`${f.main_ssd} 10:30:00`)
var peakTimes = [Date.parse(`${f.main_ssd} 08:00:00`), Date.parse(`${f.main_ssd} 05:30:00`)]
var peakRange = 45 * 60 * 1000 //45 minutes
for (let i = 0; i < datapack.length; i++) {
    const e = datapack[i];

    var seconds = 0;

    var wtaDate = Date.parse(`${e.main_ssd} ${e.wta}`)
    var ptaDate = Date.parse(`${e.main_ssd} ${e.pta}`)

    //console.log(wtaDate, ptaDate)
    if(wtaDate && ptaDate){       
       seconds += (wtaDate - ptaDate) / 1000
    }
    var wtdDate = Date.parse(`${e.main_ssd} ${e.wtd}`)
    var ptdDate = Date.parse(`${e.main_ssd} ${e.ptd}`)
    if(wtdDate && ptdDate){
        seconds += (wtdDate - ptdDate) /  1000
    
        if (e.tpl == "LEEDS" || e.tpl =="MCKLFLD" || e.tpl =="GARFRTH" || e.tpl == "YORK" || e.tpl == "CSGT"){
            var timeafterstart = ((wtaDate - incidentStartTime)/1000) -3600
            if (timeafterstart >0){
                var addeddelay =  1800*Math.exp(-Math.random()* timeafterstart/2400)
                
                for (peak of peakTimes){
                    if (Math.abs(wtdDate - peak) < peakRange) {
                        addeddelay =addeddelay * 1.5
                    }
                }
                seconds +=Math.floor(addeddelay)
                //console.log(seconds)
            }
        }
    }
   
    e.delaySeconds = seconds
    if(wtaDate){
        var d = wtaDate + seconds
        var date = new Date(d);
        var minutes = date.getMinutes();
        var hour = date.getHours();

        e.wta = `${hour}${minutes}`
        }
    newData.push(e)
}


fs.writeFileSync("tweak_data.json",JSON.stringify(newData), "utf-8")