import re
from network import getVideoUrl
from network import getPdfUrl

def char2int(n):
    indexDict = {
        '一':1,
        '二':2,
        '三':3,
        '四':4,
        '五':5,
        '六':6,
        '七':7,
        '八':8,
        '九':9,
        '十':10
    }
    if len(n)==1:
        return str(indexDict[n])
    elif len(n)==2 and n[0]=='十':
        return str(10+indexDict[n[1]])
    elif len(n)==2 and n[1]=='十':
        return str(indexDict[n[0]]*10)
    elif len(n)==2:
        return str(indexDict[n[0]]*10+indexDict[n[1]])
    else:
        return str(indexDict[n[0]]*10+indexDict[n[2]])

def reName(name):
    if re.search('第[一二三四五六七八九十]{3}', name):
        get = list(re.search('第[一二三四五六七八九十]{3}', name).span())
        temp = ''
        for i in range(len(name)):
            if (i>get[0] and i<get[1]):
                temp+=name[i]
        temp = '第'+'0'+char2int(temp)
        name = re.sub('第[一二三四五六七八九十]{3}', temp, name)
    elif re.search('第[一二三四五六七八九十]{2}', name):
        get = list(re.search('第[一二三四五六七八九十]{2}', name).span())
        temp = ''
        for i in range(len(name)):
            if (i>get[0] and i<get[1]):
                temp+=name[i]
        temp = '第'+'0'+char2int(temp)
        name = re.sub('第[一二三四五六七八九十]{2}', temp, name)
    elif re.search('第[一二三四五六七八九十]', name):
        get = list(re.search('第[一二三四五六七八九十]', name).span())
        temp = ''
        for i in range(len(name)):
            if (i>get[0] and i<get[1]):
                temp+=name[i]
        temp = '第'+'00'+char2int(temp)
        name = re.sub('第[一二三四五六七八九十]', temp, name)
    return name

def namer(name, num='k'):
    name = reName(name)
    forbid = re.compile('[\\/:\*\?\"<>\|\s]')
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

def notTest(line):
    testPat = re.compile('s\d+\.test=s\d+')
    if testPat.search(line):
        return False
    else:
        return True

def parser(courseList:str, courseUrl)->dict:
    courseDict = {}
    '''
    一级目录 无chapterId 无contentId contentType=1
    二级目录 有chapterId 无contentId contentType=1
    视频文件 有chapterId 有contentId contentType=1
    pdf文件 有chapterId 有contentId contentType=3
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
            #print('\n\n{0}\n{1}\n\n'.format(getName(line), namer(getName(line))))
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
        elif (getchId(line) and getcoId(line) and getcoType(line)=='3' and notTest(line)):
            # ~ print('pdf课件')
            ok = getPdfUrl(getName(line), getcoId(line), getId(line))
            temp2[namer(getName(line))]={
                'url':ok,
                'format':'pdf'
            }
    return courseDict
