

# PDF with colourful graphs, 24 Oct 2019, 19:44, MD BELOW SBAR,
data = {
    "incident": {
        "ppmFailures": 11,
        "type": "MD",
        "date": "20191024",
        "time": "1944",
        "expectedRecovery": 60, #minutes; duration
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

cfg = { # Must be >= 1
    "primary": 1,
    "reactOther": 1.5,
    "reactLateStart": 1.5,
    "fullCanc": 2,
    "partCanc": 1.6 # Say better than full cancellation but still worse than just a delay.

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
    """Calculate the metric of one slice, sum of weighted products, taking into account expected recovery time."""

    metric = slice["primary"] * cfg["primary"] + \
             slice["reactOther"] * cfg["reactOther"] + \
             slice["reactLateStart"] * cfg["reactLateStart"] + \
             slice["fullCanc"] * cfg["fullCanc"] + \
             slice["partCanc"] * cfg["partCanc"]   

    sliceNo = sliceNoFromIncident(incidentData["time"], slice["time"])
    if sliceNo is None:# occurred before the accident
        return 0

    # plus 29 so that it rounds it up to the next slice
    expectedTimeOfRecovery = calculateRecoveryTime(incidentData["time"], incidentData["expectedRecovery"] + 29)

    expectedSliceNo = sliceNoFromIncident(incidentData["time"], expectedTimeOfRecovery)

    if sliceNo > expectedSliceNo:
        metric *= timeCost(sliceNo, True)
    else:
        metric *= timeCost(sliceNo, False)

    return metric

def countAllDelays(slide):
    return slice["primary"] + \
        slice["reactOther"] + \
        slice["reactLateStart"] + \
        slice["fullCanc"] + \
        slice["partCanc"]

slices = []
delays = []
metrics = []
for slice in data["slices"]:
    slices.append(slice["time"])
    delays.append(countAllDelays(slice))
    metrics.append(calculateSliceMetric(slice, data["incident"]))


import plotMetric 

plotMetric.plot(slices, delays, metrics)