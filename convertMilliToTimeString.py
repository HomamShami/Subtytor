import datetime

def convertMillisecsToTimeString(milli):
    milli = milli/1000
    timeString = str(datetime.timedelta(seconds=milli))

    if(timeString.startswith("0:") or timeString.startswith("1:")or
            timeString.startswith("2:")or timeString.startswith("3:")or
            timeString.startswith("4:")or timeString.startswith("5:")or
            timeString.startswith("6:")or timeString.startswith("7:")or
            timeString.startswith("8:")or timeString.startswith("9:")):
        timeString = "0" + timeString

    if(len(timeString) >= 13):
        howMuchExtra = len(timeString) - 12
        timeString = timeString[:-howMuchExtra]

    # print(timeString)
    return timeString

def makeBetterEndingTime(lastFirst, firstLast):
    subtraction = firstLast - lastFirst
    if(subtraction >= 2000):
        result = lastFirst + 999
        return convertMillisecsToTimeString(result)
    elif(subtraction < 2000):
        result = subtraction * 0.95
        result = result + lastFirst
        return convertMillisecsToTimeString(result)
    else:
        return convertMillisecsToTimeString(lastFirst)

# convertMillisecsToTimeString(3600000)