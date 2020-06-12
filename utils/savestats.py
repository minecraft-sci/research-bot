import utils.cfl as cfl
import utils.files as files

def isStat(statname):
    return files.exists(f"data/stats/{statname}.json")

def newStat(statname, initialValue):
    files.createFolderIfNotExist("data/stats/")
    cfl.createAttributeConfig(f"data/stats/{statname}.json")
    cfl.setConfigAttribute(statname, initialValue, f"data/stats/{statname}.json")

def getStat(statname):
    return cfl.getConfigAttribute(statname, f"data/stats/{statname}.json")

def setStat(statname, statvalue):
    if not files.exists(f"data/stats/{statname}.json"):
        newStat(statname, statvalue)
    else:
        cfl.setConfigAttribute(statname, statvalue, f"data/stats/{statname}.json")

def numericUpdate(statname, increment=1, start=1):
    if not isStat(statname):
        newStat(statname, start)
    else:
        stat = getStat(statname)
        stat += increment
        setStat(statname, stat)