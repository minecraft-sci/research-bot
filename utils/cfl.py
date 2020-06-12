import json
from os.path import exists

##Errors
class InvalidFilenameError(Exception):
    pass

class NotAListError(Exception):
    pass

##JSON-Conf
def getJsonData(filename):
    if not exists(filename):
        raise InvalidFilenameError(f"{filename} was not found.")
    with open(filename) as f:
        return json.load(f)

def writeJsonData(filename, json_data):
    with open(filename, 'w+') as f:
        json.dump(json_data, f)

def getConfigAttribute(attrib_name, filename):
    json_data = getJsonData(filename)
    return json_data[attrib_name]

def getConfigList(filename):
    json_data = getJsonData(filename)
    if type(json_data) != type([]):
        raise NotAListError(f"{filename} does not contain a JSON list object!")
    return json_data

def createAttributeConfig(filename):
    writeJsonData(filename, {})

def setConfigAttribute(attrib_name, attrib_value, filename):
    json_data = getJsonData(filename)
    json_data[attrib_name] = attrib_value
    writeJsonData(filename, json_data)

def setConfigList(json_list, filename):
    if type(json_list) != type([]):
        raise NotAListError(f"Data is not a JSON list object! {type(json_list)}")
    writeJsonData(filename, json_list)

def addConfigAttribute(attrib_name, attrib_value, filename):
    setConfigAttribute(attrib_name, attrib_value, filename)

def addAttributeToList(attrib, filename):
    jsd = getConfigList(filename)
    jsd.append(attrib)
    setConfigList(jsd, filename)