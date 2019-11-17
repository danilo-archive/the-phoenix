import json

cfg = { # Must be >= 1
    "primary": 1,
    "reactOther": 1.5,
    "reactLateStart": 1.5,
    "fullCanc": 2,
    "partCanc": 1.6, # Say better than full cancellation but still worse than just a delay.
    "ppmFailures": 5 # will be parsed to int()
}

def roundDownMin(min):
    if min >= 30:
        return 30
    return 0  

def sliceNoFromIncident(incidentTime, time):
    """Calculate distance from the incident in terms of 30min time slices."""

    # Round incident time down to closest 30minutes
    incHour = int(incidentTime[:2])
    incMinute = roundDownMin(int(incidentTime[2:]))

    hour = int(time[:2])
    min = roundDownMin(int(time[2:]))

    if hour < incHour or \
        (hour == incHour and min < incMinute):
        # Slice before the incident has happened. TODO: not resulted from the incident?
        return None 

    minSlice = (min - incMinute) / 30 # either 0 or 1
    return (hour - incHour) * 2 + minSlice + 1

def timeCost(sliceNo, penalise):
    """How to penalise later events. Penalise for slices outside the expected range."""
    if penalise:
        return 1 + (sliceNo / 24.0) * 2
    return 1 + sliceNo / 24.0

def calculateRecoveryTime(incTime, expRecDuration):
    """Transforms expected recovery duration into a time."""
    hour = int(incTime[:2])
    min = int(incTime[2:]) + expRecDuration

    hoursToAdd = min / 60
    minLeft = min - hoursToAdd * 60
    hour += hoursToAdd

    return str(hour).zfill(2) + str(minLeft).zfill(2)

def calculateSliceMetric(slice, incidentData):
    """Calculate the metric of one slice, sum of weighted products, WITHOUT recovery time."""

    metric = slice["primary"] * cfg["primary"] + \
             slice["reactOther"] * cfg["reactOther"] + \
             slice["reactLateStart"] * cfg["reactLateStart"] + \
             slice["fullCanc"] * cfg["fullCanc"] + \
             slice["partCanc"] * cfg["partCanc"]   

    return metric

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def countAllDelays(slice):
    return slice["primary"] + \
        slice["reactOther"] + \
        slice["reactLateStart"] + \
        slice["fullCanc"] + \
        slice["partCanc"]

def calculateDayMetric(data):
    """
    Returns: {
        slicesTags: [...],
        delays: [...],
        metrics: [...],
        total: float # final metric value for the day
    }
    """
    allSlicesTags = []
    allMetrics = []
    allDelays = []
    
    metricsOnTime = []
    metricsLate = []

    for slice in data["slices"]:
        allSlicesTags.append(slice["time"])
        allDelays.append(countAllDelays(slice))

        sliceMetric = calculateSliceMetric(slice, data["incident"])

        expectedTimeOfRecovery = calculateRecoveryTime(data["incident"]["time"], data["incident"]["expectedRecovery"] )

        expectedSliceNo = sliceNoFromIncident(data["incident"]["time"], expectedTimeOfRecovery)

        sliceNo = sliceNoFromIncident(data["incident"]["time"], slice["time"])
        if sliceNo is None:# occurred before the accident
            metricsOnTime.append(0)
            allMetrics.append(0)
        elif sliceNo > expectedSliceNo:
            sliceMetric *= timeCost(sliceNo, True)
            metricsLate.append(sliceMetric)
            allMetrics.append(sliceMetric)
        else:
            sliceMetric *= timeCost(sliceNo, False)
            metricsOnTime.append(sliceMetric)
            allMetrics.append(sliceMetric)

    meanRatio = sum(metricsLate)
    if meanRatio == 0:
        meanRatio = 1
    meanRatio = sum(metricsOnTime) / meanRatio


    for i in range(int(cfg["ppmFailures"])):
        meanRatio = meanRatio - (meanRatio * data["incident"]["ppmFailures"] / 100) # divide by 100 because in % not in ration
    

    return {
        "slicesTags": allSlicesTags,
        "delays": allDelays,
        "metrics": allMetrics,
        "total": meanRatio
    }
    
file = "CSGTForMetric"
with open(file + '.json', 'r') as f:
    data = json.load(f)

result = calculateDayMetric(data)

res = open(file + "_metric.json", "w")

jsonToBe = {
    "dailyMetric": result["total"],
    "slices": []
}
for i in range(len(result["slicesTags"])):
    jsonToBe["slices"].append({
        "slice": result["slicesTags"][i][:2] + ":" + result["slicesTags"][i][2:],
        "delays": result["delays"][i],
        "metrics": result["metrics"][i]/2,
    })

res.write(json.dumps(jsonToBe))

import plotMetric

plotMetric.plot(result["slicesTags"], result["delays"], result["metrics"], result["total"])