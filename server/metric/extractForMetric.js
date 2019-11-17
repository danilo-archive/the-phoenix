const fs = require('fs')
let data = JSON.parse(fs.readFileSync('../../tweak_data.json'));

location = "CSGT"


times = {'0000': 0,'0030': 0,'0100': 0,'0130': 0,'0200': 0,'0230': 0,
'0300': 0,'0330': 0,'0400': 0,'0430': 0,'0500': 0,'0530': 0,'0600': 0,
'0630': 0,'0700': 0,'0730': 0,'0800': 0,'0830': 0,'0900': 0,'0930': 0,'1000': 0,
'1030': 0,'1100': 0,'1130': 0,'1200': 0,'1230': 0,'1300': 0,'1330': 0,'1400': 0,
'1430': 0,'1500': 0,'1530': 0,'1600': 0,'1630': 0,'1700': 0,'1730': 0,'1800': 0,
'1830': 0,'1900': 0,'1930': 0,'2000': 0,'2030': 0,'2100': 0,'2130': 0,'2200': 0,
'2230': 0,'2300': 0,'2330': 0};

allTrains = 0
ppmLateTrains = 0

function getTimeGroup(timestamp) {
    timestamp.replace(":", "")
    hour = timestamp.substring(0,2);
    minute = timestamp.substring(2,4)

    if (minute > 30) {
        minute = 30;
    }
    else {
        minute = 0;
    }

    return hour.toString().padStart(2, '0') + minute.toString().padStart(2, '0')    
}


data.forEach(elem => {
    if (elem.tpl != location) {
        return;
    }

    delay = elem.delaySeconds;
    ppmLateTrains += elem.ppmPassed
    allTrains -= -1

    if (delay <= 0) {
        return;
    }

    timeGroup = getTimeGroup(elem.wta)
    times[timeGroup] += delay / 60

    
});

feedToMetric = {
    incident: {
        ppmFailures: (1 - (ppmLateTrains / allTrains)) * 100, // %
        time: "1130",
        expectedRecovery: 120 // minutes  
    },
    slices: []
}

for (let key in times) {
    feedToMetric.slices.push({
        time: key,
        primary: 0,
        reactOther: times[key],
        reactLateStart: 0,
        fullCanc: 0, 
        partCanc: 0
    })
}

fs.writeFileSync(location + "ForMetric.json",
 JSON.stringify(feedToMetric), "utf-8")