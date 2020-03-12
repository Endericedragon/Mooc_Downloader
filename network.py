import requests
import os
import re
import json
import urllib.request

urlList = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr'
urlSig = 'http://www.icourse163.org/web/j/resourceRpcBean.getResourceToken.rpc?csrfKey='
hd = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'}

def https2http(url:str)->str:
    if re.match('^https://.+', url):
        url = re.sub('https', 'http', url)
    return url

def getCourseName(courseUrl:str)->str:
    try:
        r = requests.get(courseUrl, headers = hd)
        r.raise_for_status()
    except:
        print('课程名获取失败')
        return ''
    webText = r.text
    name_pat = re.compile('<title>.+</title>')
    name = name_pat.search(webText)
    if name:
        name = name.group()[7:-8]
        print('=============='+name+'==============')
        return name

def getTid(courseUrl:str)->str:
    if re.search('tid=\d+', courseUrl):
        return re.search('tid=\d+', courseUrl).group()[4:]
    try:
        r = requests.get(courseUrl, headers = hd)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print('Network error.')
        return ''
    #termId : "1207386214"
    tid_pat = re.compile('termId.:.\"\d+\"')
    print((r.text).find('termId'))
    tid = tid_pat.search(r.text)
    if tid:
        tid = tid.group()[10:-1]
    return tid
    
def getList(tid:str)->str:
    listData = {
        'callCount': '1', 
        'scriptSessionId': '${scriptSessionId}190', 
        'httpSessionId': '', 
        'c0-scriptName': 'CourseBean', 
        'c0-methodName': 'getMocTermDto', 
        'c0-id': '0', 
        'c0-param0': 'number:'+tid, #tid
        'c0-param1': 'number:0', 
        'c0-param2': 'boolean:true', 
        'batchId': '1582379864851'
    }
    try:
        r = requests.post(urlList, data = listData, headers = hd)
        r.raise_for_status()
    except:
        print('An error occurred while getting course list.')
        return ''
    webText = r.text.encode('utf-8').decode('unicode_escape')
    return webText

def getVideoUrl(name, contentId, iD, courseUrl):
    s = requests.Session()
    print('-*------'+name+'------*-')
    print('获取Key...')
    for i in range(5):
        try:
            r = s.get(courseUrl, headers = hd, timeout = 2)
            break
        except:
            print('正在重试获取Key...')
    key = r.cookies['NTESSTUDYSI']
    bizData = {'bizId':iD,'contentType':'1','bizType':'1'}
    print('发送Key...')
    for i in range(5):
        try:
            t = s.post(urlSig+key, headers = hd, data = bizData, timeout = 2)
            break
        except:
            print('正在重试发送Key...')
    false = False
    true = True
    null = None
    tempDict = eval(t.text)
    if tempDict:
        tempDict = tempDict['result']['videoSignDto']
    videoId = tempDict['videoId']
    fckSig = tempDict['signature']
    videoUrl = 'http://vod.study.163.com/eds/api/v1/vod/video?videoId={0}&signature={1}&clientType=1'.format(videoId, fckSig)
    print('获取视频下载链接...')
    for i in range(5):
        try:
            r = s.get(videoUrl, headers = hd, timeout = 2)
            break
        except:
            print('尝试重新获取链接...')
    videoLink = r.json()['result']['videos'][-1]['videoUrl'] #这里可以调节清晰度
    fmt = r.json()['result']['videos'][-1]['format']
    return [videoLink,fmt]
    
def ariaDown(url, file_name, path):
    if (os.path.exists(path+'\\'+file_name) or os.path.exists(path+'\\'+file_name) or os.path.exists(path+'\\'+file_name)):
        print('File exists.{0} won\'t be downloaded.'.format(file_name))
    else:
        os.system('aria2\\aria2c --split=16 --dir \"{dire}\" --out \"{x}\" {y}'.format(dire=path, x=file_name, y=url))

def urllibDown(url, fileName, path):
    if (os.path.exists(path+'\\'+fileName) or os.path.exists(path+'\\'+fileName) or os.path.exists(path+'\\'+fileName)):
        print('File exists.{0} won\'t be downloaded.'.format(fileName))
        return 0
    for i in range(1,6):
        try:
            print('正在下载'+fileName+'...')
            r = requests.get(url, headers = hd, timeout = 2)
            break
        except:
            print('重试...第%d次' % (i))
    with open(path+'\\'+fileName, 'wb') as f:
        f.write(r.content)
    print(fileName, '下载完成。')

def getPdfUrl(name, conId, Id):
    pdfUrl = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
    pdfData = {
        'callCount':'1',
        'scriptSessionId':'${scriptSessionId}190',
        'httpSessionId':'0397251039424db2b1659352f45d1540',
        'c0-scriptName':'CourseBean',
        'c0-methodName':'getLessonUnitLearnVo',
        'c0-id':'0',
        'c0-param0':'number:'+conId, #(contentId)
        'c0-param1':'number:3',
        'c0-param2':'number:0',
        'c0-param3':'number:'+Id, #(id)
        'batchId':'1584017274511'
    }
    try:
        r = requests.post(pdfUrl, headers = hd, data = pdfData)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
    except:
        return ''
    gotIt = r.text
    pdfGet = re.search('textOrigUrl:\".+?\"', gotIt)
    if pdfGet:
        pdfGet = pdfGet.group()[13:-1]
    else:
        pdfGet = ''
    return pdfGet
def test():
    getPdfUrl('wow', '1003316105', '1214227359')
if __name__ == '__main__':
    test()