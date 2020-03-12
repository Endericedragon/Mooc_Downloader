import re
import os
import pickle
import network
from multiprocessing import Pool

def namer(num):
    if num<10:
        return '000'+str(num)
    elif num<100:
        return '00'+str(num)
    elif num<1000:
        return '0'+str(num)
    else:
        return str(num)

def m3u8Process(courseName, courseDict):
    rawPat = re.compile('^https?://.+/\d{4}/\d{2}/\d{2}/')
    for week, sections in courseDict.items():
        for section, vidInfo in sections.items():
            path = courseName+'\\'+week+'\\'+section
            #文件路径
            for vidName, detail in vidInfo.items(): #vidName没有后缀名
                if detail['format']!='m3u8':
                    continue
                elif os.path.exists(path+'\\'+vidName+'.ts'):
                    continue
                for vid in os.listdir(path): #vid带有后缀名
                    if re.search(vidName, vid) and 'mp4' not in vid:
                        fg = 'ffmpeg\\bin\\ffmpeg.exe'
                        cc = 0
                        rawUrl = vidInfo[vidName]['url']
                        url = rawPat.match(rawUrl).group()
                        # ~ print(vid)
                        with open(path+'\\'+vid, 'r') as f:
                            tsInfo = f.readlines()
                        p = Pool(4)
                        for each in tsInfo:
                            each = each.strip()
                            if each[0]!='#':
                                # ~ p.apply_async(os.system, args = ('{0} -n -i \"{1}\" \"{2}\\{3}.ts\"'.format(fg, url+each, path, namer(cc)),))
                                p.apply_async(network.urllibDown, args = (url+each, namer(cc)+'.ts', path))
                                cc+=1
                        p.close()
                        p.join()
                        print(vidName, '的分片文件全部下载完成')
                        files = 'concat:'
                        for i in range(cc):
                            files+=(path+'\\'+namer(i)+'.ts|')
                        files = files[:-1]
                        os.system('{0} -n -i \"{1}\" \"{2}\\{3}.mp4\"'.format(fg, files, path, vidName))
                        os.remove(path+'\\'+vid)
                        for ck in range(cc):
                            os.system('del \"{0}\\{1}.ts\"'.format(path, namer(ck)))
