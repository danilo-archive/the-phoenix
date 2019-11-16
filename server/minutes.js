const fs = require('fs')
let datapack =     JSON.parse(fs.readFileSync('beauty.json'));

let newData = []

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
    }
    if(seconds > 60){
        e.delaySeconds = seconds
        console.log(seconds)
    }else{//console.log(seconds)
    }
    newData.push(e)
}




