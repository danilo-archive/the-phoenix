from metricCalculator import calculateDayMetric 
import json

# PDF with colourful graphs, 24 Oct 2019, 19:44, MD BELOW SBAR,
example = {
    "incident": {
        "ppmFailures": 0.19, # %; percentage
        "type": "MD",
        "date": "20191024",
        "time": "1944",
        "expectedRecovery": 60, #minutes; duration
        # below not currently needed
        "totalDelays": 150,
        "fullCanc": { # at origin
            "numOfTrains": 1,
            "delay": 45
        }   
    },
    "slices": [
        {
            "time": "1830",
            "primary": 0,
            "reactOther": 0,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        { 
            "time": "1900",
            "primary": 0,
            "reactOther": 15,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "1930",
            "primary": 30,
            "reactOther": 0,
            "reactLateStart": 15,
            "fullCanc": 45, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2000",
            "primary": 0,
            "reactOther": 30,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2030",
            "primary": 0,
            "reactOther": 18,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2100",
            "primary": 0,
            "reactOther": 5,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2130",
            "primary": 0,
            "reactOther": 40,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2200",
            "primary": 0,
            "reactOther": 0,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2230",
            "primary": 0,
            "reactOther": 0,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2300",
            "primary": 0,
            "reactOther": 20,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        },
        {
            "time": "2330",
            "primary": 0,
            "reactOther": 18,
            "reactLateStart": 0,
            "fullCanc": 0, # mins; delays caused by full cancellation
            "partCanc": 0
        }
    ]
}

times = []

time = "0000"
times.append(time)
while True:
    h = int(time[:2])
    m = int(time[2:])

    m += 30
    if 


result = calculateDayMetric(example)

jsonToBe = []
for i in range(len(result["slicesTags"])):
    jsonToBe.append({
        "slice": result["slicesTags"][i][:2] + ":" + result["slicesTags"][i][2:],
        "delays": result["delays"][i],
        "metrics": result["metrics"][i]/2,
    })

f = open("./exampleMetric.json", "w")

f.write(json.dumps(jsonToBe))

f.close() 
