import os
import pickle
import network
from multiprocessing import Pool

def creater(courseName, courseDict):
    p = Pool(4)
    try:
        os.mkdir(courseName)
    except:
        pass
    for week, sections in courseDict.items():
        try:
            os.mkdir(courseName+'\\'+week)
        except:
            pass
        for section, videos in sections.items():
            try:
                os.mkdir(courseName+'\\'+week+'\\'+section)
            except:
                pass
            for video, info in videos.items():
                fileName = video+'.'+info['format']
                url = info['url']
                path = courseName+'\\'+week+'\\'+section
                #network.ariaDown(url, fileName, path)
                p.apply_async(network.ariaDown, args=(url, fileName, path))
    p.close()
    p.join()
'''
with open('tempDict.pck', 'rb') as f:
    courseDict = pickle.load(f)
creater('fuck', courseDict)
'''
