import re
from network import getVideoUrl

def namer(name, num='k'):
    forbid = re.compile('[\\/:\*\?\"<>\|]')
    legal_name = ''
    for each in name:
        if forbid.match(each):
            pass
        else:
            legal_name+=each
    if num=='k':
        return legal_name
    elif num<10:
        return '00'+str(num)+legal_name
    elif num<100:
        return '0'+str(num)+legal_name
    else:
        return str(num)+legal_name

def getchId(line):
    chPat = re.compile('chapterId=\d+')
    chId = chPat.search(line)
    if chId:
        return chId.group()[10:]
    else:
        return None

def getcoId(line):
    ciPat = re.compile('contentId=\d+')
    coId = ciPat.search(line)
    if coId:
        return coId.group()[10:]
    else:
        return None

def getId(line):
    idPat = re.compile('id=\d+')
    iD = idPat.search(line)
    if iD:
        return iD.group()[3:]
    else:
        return None

def getcoType(line):
    ctPat = re.compile('contentType=\d+')
    coType = ctPat.search(line)
    if coType:
        return coType.group()[12:]
    else:
        return None

def getName(line):
    nPat = re.compile('name=\".+\"')
    name = nPat.search(line)
    if name:
        return name.group()[6:-1]
    else:
        return None

def parser(courseList:str, courseUrl)->dict:
    courseDict = {}
    '''
    一级目录 无chapterId 无contentId contentType=1
    二级目录 有chapterId 无contentId contentType=1
    视频文件 有chapterId 有contentId contentType=1
    '''
    courseList = courseList.split('\n')
    for line in courseList:
        # ~ print('--*---------*--')
        # ~ print(getchId(line))
        # ~ print(getcoId(line))
        # ~ print(getcoType(line))
        # ~ print(getName(line))
        if (getchId(line)==None and getcoId(line)==None and getcoType(line)=='1'):
            # ~ print('一级目录')
            temp = courseDict
            courseDict[namer(getName(line))]={}
            temp = courseDict[namer(getName(line))]
        elif (getchId(line) and getcoId(line)==None and getcoType(line)=='1'):
            # ~ print('二级目录')
            temp2 = temp
            temp2[namer(getName(line))]={}
            temp2 = temp2[namer(getName(line))]
            cc=0
        elif (getchId(line) and getcoId(line) and getcoType(line)=='1'):
            # ~ print('视频文件')
            yes = getVideoUrl(getName(line), getcoId(line), getId(line), courseUrl)
            if yes[1]=='hls':
                yes[1]='m3u8'
            temp2[namer(getName(line), cc)]={
                # ~ 'contentId':getcoId(line),
                # ~ 'id':getId(line),
                'url':yes[0],
                'format':yes[1]
            }
            cc+=1
    return courseDict

