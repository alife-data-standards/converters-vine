import json
import csv
import os

import argparse
parser = argparse.ArgumentParser(description='Converts a JSON file in ALDS format to directories and files reuired for vine.')
parser.add_argument('-path', type=str, metavar='PATH', default = '',  help='path to files - default : none (will read files in current directory)', required=False)
parser.add_argument('-file', type=str, metavar='FILE NAME', default = 'lineageData.csv',  help='name of data file !! MUST BE IN JSON FORMAT !! default : lineage.json', required=False)
parser.add_argument('-verbose', action='store_true', default = False, help='adding this flag will provide more text output while running (useful if you are working with a lot of data to make sure that you are not hanging) - default (if not set) : OFF', required=False)

parser.add_argument('-parentMethod', type=str, metavar='METHOD', default = 'MAX',  help='method used to determine parents. options are: LOD (attempts to establish LOD, and uses these as parents), MAX(use org with max parentTrait on each update)', required=False)
parser.add_argument('-parentTrait', type=str, metavar='DATA NAME', default = '',  help='name of data to be used to determine parent', required=True)
parser.add_argument('-traits', type=str, metavar='DATA NAME', default = [''],  help='column names of data, first two values will be x and y in cloud view, third will be shown as score. others will be ignored)',nargs='+', required=True)
parser.add_argument('-updateColumnName', type=str, metavar='DATA NAME', default = 'origin_time',  help='name of column in source data to use for "update" in vine (i.e. time)', required=False)

args = parser.parse_args()

filePath = args.path
filename = args.file
fileName = filePath + filename

print("loading data...",flush=True)

with open(filePath+filename, 'r') as fp:
    data = json.load(fp)


# with data loaded we now have dict ID: (org data)
# check the user specified columns exist

# this gives access to first element. we assume all others are the same
randomOrg = next(iter(data.values()))
if (args.parentTrait not in randomOrg):
    print('parentTrait was not found in the supplied data. exiting...')
    exit(1)
	
for trait in args.traits:
    if trait not in randomOrg:
        print('trait "'+trait+'" was not found in the supplied data. exiting...')
        exit(1)
        
if args.updateColumnName not in randomOrg:
    print('updateColumnName "'+args.updateColumnName+'" was not found in the supplied data. exiting...')
    exit(1)
    
# convert data so that all trait data is float
# also get lastTime (last time we find in the update field
largestUpdate = -1
for orgID in data:
    data[orgID][args.parentTrait] = float(data[orgID][args.parentTrait])
    data[orgID][args.updateColumnName] = float(data[orgID][args.updateColumnName])
    for trait in args.traits:
        data[orgID][trait] = float(data[orgID][trait])
    largestUpdate = max(data[orgID][args.updateColumnName],largestUpdate)

# if parentMethod is LOD, construct LOD or sex is found, exit if there is sex
# step one, get largest update values
parentsIDs = []

if (args.parentMethod == 'LOD'):
    print('generating LOD parents list...')
    lastGeneration = []
    for orgID in data:
        if len(data[orgID]['ancestor_list']) > 1:
            print('parent method is set to LOD, but organism with ID',orgID,'has more then 1 parent. please use MAX or AVE parentMethod. exiting...')
            exit(1)
        if int(data[orgID][args.updateColumnName]) == largestUpdate: # if this org is as old as largestUpdate, add to lastGeneration
            lastGeneration.append(orgID)
    
    lastLOD_ID = lastGeneration[0] # assume first in lastGeneration is best
    for orgID in lastGeneration: # for each org in last generation, see if they are better
        if data[orgID][args.parentTrait] > data[lastLOD_ID][args.parentTrait]:
            lastLOD_ID = orgID
    
    print('    found last org on LOD with ID:',lastLOD_ID,'at time',largestUpdate)
    
    LOD_trace_ID = lastLOD_ID
    while LOD_trace_ID != '-1':
        parentsIDs.append(LOD_trace_ID)
        LOD_trace_ID = str(data[LOD_trace_ID]['ancestor_list'][0])
    parentsIDs.reverse()
    if args.verbose:
        print('identified LOD parents (list of orgIDs):',parentsIDs)
        
elif (args.parentMethod == 'MAX'):
    print('generating MAX parents list...')
    parentsMap = {} # map format is time:[orgID,parentTraitValue] where orgID has highest parentTrait for that time
    for orgID in data:
        # check if parentsMap has this orgID
        if data[orgID][args.updateColumnName] not in parentsMap.keys(): # if this time is not in parentsMap, add this org and their parentTrait value
            parentsMap[data[orgID][args.updateColumnName]]=[orgID,float(data[orgID][args.parentTrait])]
        elif float(data[orgID][args.parentTrait]) > parentsMap[data[orgID][args.updateColumnName]][1]: # else if this orgs parentTrait > the parentTrait value currently in parentsMap for this time
            parentsMap[data[orgID][args.updateColumnName]]=[orgID,float(data[orgID][args.parentTrait])] # overwrite value in parentsMap
            
    sortedKeys = sorted([int(x) for x in list(parentsMap.keys())])
    for k in sorted([int(x) for x in list(parentsMap.keys())]): # in order starting with the smallest key, create parents list
       parentsIDs.append( parentsMap[k][0] ) # append the orgID (in position 0) for time k

    if args.verbose:
        print('identified MAX parents (list of orgIDs):',parentsIDs)

else:
    print('the parentMethod provided "'+args.parentMethod+'" was not found in the supplied data. exiting...')
    exit(1)

# now parentsMap contains the parents in sorted order. now we need to start at snapshot 0 and output all
# orgs with update >= parent and < next parent
currentParentIndex = 0

print('processing output...')

while currentParentIndex < len(parentsIDs):
    offspringCollection = []
    currentParentID = parentsIDs[currentParentIndex]
    currentParentTime = data[currentParentID][args.updateColumnName]
    if currentParentIndex < len(parentsIDs) - 1:
        nextParentTime = data[parentsIDs[currentParentIndex+1]][args.updateColumnName]
    else:
        nextParentTime = largestUpdate+1
    for orgID in data:
        if currentParentTime <= data[orgID][args.updateColumnName] < nextParentTime:
            offspringCollection.append(data[orgID])
            if args.verbose:
                print('at step:',currentParentIndex,'time:',currentParentTime,'parent:',currentParentID,'adding:',orgID)
    
    # save parent to parent file and offspring to offspring file
    outPath = 'vineData/snapshots/snapshot_gen_'+str(currentParentIndex).zfill(4)
    parentOutFile = 'snapshot_parent_'+str(currentParentIndex).zfill(4)+'.dat'
    offspringOutFile = 'snapshot_offspring_'+str(currentParentIndex).zfill(4)+'.dat'
    os.makedirs(outPath, exist_ok=True)
    with open(outPath + '/' + parentOutFile, 'w') as file:
        outLine = ""
        for trait in args.traits:
            outLine += str(data[currentParentID][trait]) + ' '
        file.write(outLine[:-1])
    with open(outPath + '/' + offspringOutFile, 'w') as file:
        for offspring in offspringCollection:
            outLine = ""
            for trait in args.traits:
                outLine += str(offspring[trait]) + ' '
            file.write(outLine[:-1]+'\n')
       
    currentParentIndex+=1

print('...output has been saved into vineData/...')

exit(1) 













	
parentData = {}
birthData = {}
lastBirthDate = -1

lineNumber = 0

for key in data:
    if lineNumber%10000 == 0:
        print('.',end='',flush=True)
    lineNumber += 1
    print("\n"+key)
    print(data[key]['ancestor_list'])
    # make sure data[key]['ancestor_list'] is a list
    if type(data[key]['ancestor_list']) == int:
        data[key]['ancestor_list'] = [data[key]['ancestor_list']]
    parentData[int(key)] = [int(p) for p in list(data[key]['ancestor_list'])]
    parentData[int(key)].sort()
    birthData[int(key)] = int(data[key]['origin_time'])
    lastBirthDate = max(lastBirthDate,birthData[int(key)])

print() # newline after all data has been loaded
print('last orgs were born at time',lastBirthDate,flush=True)

lastGenerationancestor_list = {}
for ID in birthData:
    if birthData[ID] == lastBirthDate:
        lastGenerationancestor_list[ID] = parentData[ID]
        
parentList = []

for ID in lastGenerationancestor_list:
    parentList.append(ID);

while 1:
    if(args.verbose):
        print("at time",birthData[parentList[0]],"... considering",len(parentList),"orgs.",parentList,flush = True)
    newParentList = []
    foundUnique = False # we have not found any unique parents lists
    first = True
    firstParentsList = []
    for ID in parentList:
        if first:
            firstParentsList = parentData[ID]
            first = False
        else:
            if parentData[ID] != firstParentsList:
                foundUnique = True # we are not done
        for parent in parentData[ID]:
            if parent not in newParentList:
                newParentList.append(parent)
    parentList = newParentList;
    if(birthData[parentList[0]] == -1):
        print('reached organism with time of birth -1. There is no MRCA(s)')
        exit(1)
    if not foundUnique: # all orgs do have the same parents list
        oldestBirth = min([birthData[x] for x in parentList])
        print('\nCoalescence found at time', oldestBirth, '\n ', lastBirthDate - oldestBirth,'time steps before oldest organism was born.\nMRCA(s) has ID(s):',parentList)
        exit(1)
