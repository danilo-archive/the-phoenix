const fs = require('fs')
let datapack =     JSON.parse(fs.readFileSync('tweak_data.json'));
value = 0;
total = 0;
delay = 0;
datapack.forEach(element => {
    if(element.tpl == "MNCRPIC"){
        console.log(element.delaySeconds,
            element.tpl, element.wta, element.ppmPassed)
        total++;
        value += element.ppmPassed
        delay += element.delaySeconds
    }
});
console.log(1 - value/total, delay/60)